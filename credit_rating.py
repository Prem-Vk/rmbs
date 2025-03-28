import ijson
import json
import argparse
from pydantic import BaseModel, computed_field, StrictInt, model_validator, ValidationError
from enum import Enum

ROOT_KEY = 'mortgages'
# LOAN_TYPE_CHOICES = Literal['fixed', 'adjustable']
# PROPERTY_TYPE_CHOICES = Literal['single_family', 'condo']

parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='Name of the file for parsing')
parser.add_argument('--rawjsondata', help='Raw json data to parse')
args = parser.parse_args()



# Risk Factors
LOAN_TYPE_RISK_FACTOR = {'fixed': -1, 'adjustable': 1}
PROPERTY_TYPE_RISK_FACTOR = {'single_family': 0, 'condo': 1}

class LoanType(str, Enum):
    Fixed = 'fixed'
    Adjustable = 'adjustable'


class PropertyType(str, Enum):
    Single_family = 'single_family'
    Condo = 'condo'


class MyModel(BaseModel):
    credit_score: StrictInt
    loan_amount: StrictInt
    property_value: StrictInt
    annual_income: StrictInt
    debt_amount: StrictInt
    loan_type: LoanType
    property_type: PropertyType


    @computed_field
    @property
    def loan_to_poperty_value_ratio_risk_factor(self) -> float:
        ltv = float(f'{(self.loan_amount/self.property_value)*100:.2f}')
        if ltv > 90.00:
            return 2
        elif ltv > 80.00:
            return 1
        return 0


    @computed_field
    @property
    def debt_to_income_ratio_risk_factor(self) -> float:
        dti = float(f'{(self.debt_amount/self.annual_income)*100:.2f}')
        if dti > 50.00:
            return 2
        elif dti > 40.00:
            return 1
        return 0

    @computed_field
    @property
    def credit_score_risk_factor(self) -> int:
        if self.credit_score >= 700:
            return -1
        elif 700 > self.credit_score >= 650:
            return 0
        return 1

    @model_validator(mode='after')
    def check_loan_amount_against_property_value(self):
        if self.loan_amount > self.property_value:
            raise ValidationError('Loan amount can only be lesser than property value')
        return self


final_risk_factor = []
credit_score_total = {'total': 0, 'frequency': 0}

def calculate_avg_credit_score_risk_factor(average_credit_score):
    if average_credit_score >= 700:
        return -1
    elif average_credit_score < 650:
        return 1
    return 0

def get_credit_rating(risk_factors):
    credit_ratings = []
    for risk_factor in risk_factors:
        if risk_factor == float("inf"):
            credit_ratings.append("Invalid Data")
        elif risk_factor <= 2:
            credit_ratings.append("AAA")
        elif 3 <= risk_factor <= 5:
            credit_ratings.append("BBB")
        else:
            credit_ratings.append("C")
    return credit_ratings

def calculate_credit_rating(data):
    data = ijson.items(data, f"{ROOT_KEY}.item")
    risk_factors = []
    for mortage in data:
        risk_factor = 0
        try:
            cleaned_data = MyModel(**mortage)
            credit_score_total["total"] += cleaned_data.credit_score
            credit_score_total["frequency"] += 1
            risk_factor = (
                cleaned_data.loan_to_poperty_value_ratio_risk_factor
                + cleaned_data.debt_to_income_ratio_risk_factor
                + cleaned_data.credit_score_risk_factor
                + LOAN_TYPE_RISK_FACTOR[cleaned_data.loan_type]
                + PROPERTY_TYPE_RISK_FACTOR[cleaned_data.property_type]
            )
            risk_factors.append(risk_factor)
        except (ValueError, ValidationError) as e:
            risk_factors.append(float("inf"))

    average_credit_score = credit_score_total["total"] / credit_score_total["frequency"]
    avg_credit_score_risk_factor = calculate_avg_credit_score_risk_factor(
        average_credit_score
    )
    map(lambda x: x + avg_credit_score_risk_factor, risk_factors)
    return get_credit_rating(risk_factors)

#  Passing data in chunk
# def parse_data_in_chunks(data):
#     data_objects = ijson.items(data, f'{ROOT_KEY}.item')
#     try:
#         while (next_data := next(data_objects)) is not None:
#             data_chunk = []
#             data_chunk.append(next_data)
#             data_chunk.extend(itertools.islice(data_objects, 20))
#             calculate_credit_rating(data=data_chunk)
#     except StopIteration:
#         pass


def main():
    if args.filename and args.rawjsondata:
        return "Please Provide single source of data."
    elif args.filename:
        load_data = open(args.filename)
    else:
        load_data = json.dumps(args.rawjsondata)

    print(calculate_credit_rating(load_data))


if __name__ == "__main__":
    main()