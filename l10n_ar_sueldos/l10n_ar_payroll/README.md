# l10n_ar_payroll/README.md

# l10n_ar_payroll

This project is a localization module for payroll management in Argentina, designed to handle various payroll calculations, tax rates, and social security contributions.

## Project Structure

```
l10n_ar_payroll
├── src
│   ├── models
│   │   ├── employee.py
│   │   └── payroll.py
│   ├── data
│   │   ├── tax_tables.py
│   │   └── social_security.py
│   └── utils
│       └── calculations.py
├── tests
│   └── test_payroll.py
├── __init__.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd l10n_ar_payroll
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

- The `Employee` class in `src/models/employee.py` allows you to create employee instances with properties like name, ID, and salary.
- The `Payroll` class in `src/models/payroll.py` manages payroll processing, including methods to calculate payroll and generate pay slips.
- Utility functions for calculations can be found in `src/utils/calculations.py`.

## Running Tests

To run the unit tests for the payroll calculations, execute:
```
pytest tests/test_payroll.py
```

## License

This project is licensed under the MIT License.