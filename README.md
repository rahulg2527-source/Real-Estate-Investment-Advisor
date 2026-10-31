# Real Estate Investment Advisor

A Python-based real estate analysis project for exploring housing data, comparing properties, and evaluating potential property investments.

## Project Overview

The Real Estate Investment Advisor combines exploratory data analysis with financial calculation tools to help users examine property information and understand potential investment scenarios.

## Features

- **Data Analysis:** Explore housing data through statistical analysis and visualizations.
- **Data Cleaning:** Perform data cleaning and feature engineering.
- **Property Comparison:** Compare multiple properties using selected attributes.
- **Investment Calculator:** Calculate rental yield, expenses, and estimated cash flow.
- **Appreciation Scenarios:** Compare hypothetical property values under different annual appreciation assumptions.
- **Interactive Dashboard:** Explore housing dataset statistics through a Streamlit application.

## Technology Stack

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- XGBoost
- Streamlit
- Plotly
- Jupyter Notebook
- Pytest

## Project Structure

```text
Real-Estate-Investment-Advisor/
|
+-- data/
|   +-- raw/
|   +-- processed/
|
+-- models/
|
+-- notebooks/
|   +-- 01_Real_Estate_Investment_Advisor.ipynb
|   +-- 02_Data_Cleaning.ipynb
|   +-- 03_Feature_Engineering.ipynb
|   +-- 04_Exploratory_Data_Analysis.ipynb
|
+-- reports/
|
+-- src/
|   +-- investment_calculator.py
|   +-- property_comparison.py
|
+-- tests/
|   +-- test_investment_calculator.py
|   +-- test_property_comparison.py
|
+-- app.py
+-- requirements.txt
+-- .gitignore
+-- README.md
```

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/rahulg2527-source/Real-Estate-Investment-Advisor.git
```

### 2. Navigate to the project directory

```powershell
cd Real-Estate-Investment-Advisor
```

### 3. Create a virtual environment

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

Start the Streamlit dashboard:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## Run Tests

Execute the test suite using:

```powershell
python -m pytest -v
```

The current test suite contains 30 tests covering investment calculations, appreciation scenarios, and property comparison functionality.

## Dataset Notes

The project uses a housing dataset containing 250,000 records and 23 columns.

The dataset is used for analysis and experimentation. Its statistical patterns should not automatically be interpreted as representative of actual Indian real estate market conditions.

The investment calculator uses user-provided assumptions. Appreciation scenarios are hypothetical estimates, not guaranteed future property values.

## Project Limitations

- The dataset has limited predictive relationships between property features and prices.
- Investment calculations depend on the accuracy of user-provided financial inputs.
- The current Streamlit interface primarily provides dashboard functionality.
- Property comparison and investment calculation are implemented as Python modules.

## Future Improvements

- Integrate property comparison into the Streamlit interface.
- Add an interactive investment calculator page.
- Integrate reliable real estate market data.
- Improve investment analysis with rental and expense datasets.
- Expand automated testing and application functionality.

## Disclaimer

This project is developed for educational and analytical purposes. Its calculations and scenarios should not be considered professional financial or real estate investment advice.

## Author

**Rahul Gupta**

GitHub: [rahulg2527-source](https://github.com/rahulg2527-source)

LinkedIn: [Rahul Gupta](https://linkedin.com/in/rahul-gupta-65a763220)
