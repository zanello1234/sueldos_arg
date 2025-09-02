# Constants for social security contributions
SOCIAL_SECURITY_RATE = 0.11  # Example rate for social security contributions

def calculate_social_security_contribution(salary):
    """
    Calculate the social security contribution based on the salary.
    
    Args:
        salary (float): The salary of the employee.
        
    Returns:
        float: The calculated social security contribution.
    """
    return salary * SOCIAL_SECURITY_RATE