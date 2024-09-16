"""
This file contains utility functions for calculating decline factors in ecommerce analytics.
The functions included in this file are:
- exponential_decline: Calculates the exponential decline factor for a given month, churn month, and decay rate.
- logarithmic_decline: Calculates the logarithmic decline factor for a given month, churn month, and base.
- stepwise_decline: Calculates the step-wise decline factor for a given month, churn month, and step size.
"""

# Define the functions

# Exponential decline
def exponential_decline(month, churn_month, decay_rate=0.2):
    """
    Calculates the exponential decline factor for a given month, churn month, and decay rate.
    Parameters:
    - month (int): The current month.
    - churn_month (int): The month when the decline starts.
    - decay_rate (float): The rate at which the decline occurs. Default is 0.2.
    Returns:
    - float: The exponential decline factor for the given month.
    """
    
    if month < churn_month:
        return 1 # No decline before churn
    else:
        time_since_churn = month - churn_month + 1
        return np.exp(-decay_rate * time_since_churn)
    
# Logarithmic decline
def logarithmic_decline(month, churn_month, base=2):
    """
    Calculates the logarithmic decline factor for a given month, churn month, and base.
    Parameters:
    - month (int): The current month.
    - churn_month (int): The month when the decline starts.
    - base (int): The base of the logarithm. Default is 2.
    Returns:
    - float: The logarithmic decline factor for the given month.
    """
    
    if month < churn_month:
        return 1 # No decline before churn
    else:
        time_since_churn = month - churn_month + 1
        return 1 / np.log2(base * time_since_churn)
    
# Step wise decline
def stepwise_decline(month, churn_month, step_size=3):
    """
    Calculates the step-wise decline factor for a given month, churn month, and step size.
    Parameters:
    - month (int): The current month.
    - churn_month (int): The month when the decline starts.
    - step_size (int): The number of months between steps. Default is 3.
    Returns:
    - float: The step-wise decline factor for the given month.
    """
    
    if month < churn_month:
        return 1 # No decline before churn
    else:
       steps_since_churn = (month - churn_month) // step_size
       return decline_factor ** steps_since_churn