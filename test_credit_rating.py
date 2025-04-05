from unittest import TestCase
from credit_rating import calculate_credit_rating
import json


valid_data = {
    "mortgages": [
        {
            "credit_score": 750,
            "loan_amount": 200000,
            "property_value": 250000,
            "annual_income": 60000,
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "single_family",
        },
        {
            "credit_score": 675,
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "adjustable",
            "property_type": "condo",
        },
        {
            "credit_score": 500,
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "fixed",
            "property_type": "condo",
        },
        {
            "credit_score": 800,
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "adjustable",
            "property_type": "single_family",
        },
        {
            "credit_score": 600,
            "loan_amount": 170000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 30000,
            "loan_type": "adjustable",
            "property_type": "single_family",
        },
    ]
}

invalid_data = {
    "mortgages": [
        {
            "credit_score": 750,
            "loan_amount": 300000,  # Loan aount greater than property amount : Edge case
            "property_value": 250000,
            "annual_income": 60000,
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "single_family",
        },
        {
            "credit_score": "750",  # Credit score as string
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "adjustable",
            "property_type": "condo",
        },
        {
            "credit_score": 500,
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "variable",  # invalid loan type
            "property_type": "condo",
        },
        {
            "credit_score": 800,
            "loan_amount": 150000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 10000,
            "loan_type": "adjustable",
            "property_type": "married",  #  Invalid property Type
        },
        {
            "credit_score": "",  # Empty Credit score
            "loan_amount": 170000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 30000,
            "loan_type": "adjustable",
            "property_type": "single_family",
        },
        {
            "credit_score": 800,  # Accurate data
            "loan_amount": 170000,
            "property_value": 175000,
            "annual_income": 45000,
            "debt_amount": 30000,
            "loan_type": "adjustable",
            "property_type": "single_family",
        },
    ]
}


class TestCalculateCreditRating(TestCase):

    def test_credit_rating_with_valid_data(self):
        self.assertEqual(
            calculate_credit_rating(json.dumps(valid_data)),
            ["AAA", "BBB", "AAA", "AAA", "C"],
        )

    def test_credit_rating_with_invalid_data(self):
        #  As we log errors for invalid_data it won't show in output.
        self.assertEqual(calculate_credit_rating(json.dumps(invalid_data)), ["BBB"])
