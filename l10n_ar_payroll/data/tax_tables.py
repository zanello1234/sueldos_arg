# Tax rate constants
INCOME_TAX_BRACKETS = [
    (0, 10000, 0.0),    # No tax for income up to 10,000
    (10001, 30000, 0.1), # 10% for income between 10,001 and 30,000
    (30001, 70000, 0.2), # 20% for income between 30,001 and 70,000
    (70001, float('inf'), 0.3) # 30% for income above 70,000
]

def get_tax_rate(income):
    """Retrieve the tax rate based on the income."""
    for lower, upper, rate in INCOME_TAX_BRACKETS:
        if lower <= income <= upper:
            return rate
    return 0.0