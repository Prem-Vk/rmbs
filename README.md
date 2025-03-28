
# Credit Rating Agency - Residential Mortgage Securities (RMBS)

The task is to implement the credit rating calculation logic for residential mortgage-backed
securities (RMBS).

## Requirements:
1. python3.6+ (As we have used pydantic v2 for data validation).
2. git

### To setup the repository please follow below steps:
1. Clone the repository.
```
git clone https://github.com/Prem-Vk/rmbs.git
```
2. Create Virtual environment.
```
python3.12 -m venv venv
```
3. Install Requirements
```
pip install -r requirements.txt
```

### Commands to run the code
1. If you have raw json data:
```
python credit_rating.py --rawjsondata '<rawjsondata>'
```
2. If you have json data in a file:
```
python credit_rating.py --filename test.json
```

## Key decisions

1. Used `ijson` package for better memory performance. As it gives data in a generator form. Hence only that data in load in memory which is required, instead of whole file.
2. `pydantic` validation for error handling and fast & custom validation.