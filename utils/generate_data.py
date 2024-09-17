"""
This script generates fake customer data using the Faker library and saves it to a CSV file.

The generated customer data includes the following fields:
- id: Unique identifier for each customer.
- name: First name of the customer.
- last_name: Last name of the customer.
- email: Email address of the customer.
- registration_date: Date of customer registration.
- birth_date: Date of birth of the customer.
- street_address: Street address of the customer.
- city: City of the customer.
- state: State of the customer.
- prefered_device: Preferred device of the customer (Mobile, Desktop, or Tablet).
- email_opt_in: Boolean value indicating whether the customer has opted in for email communication.
- prefered_payment_methods: Preferred payment method of the customer (Credit Card, Paypal, Apple Pay, or Google Pay).
- gender: Gender of the customer (male or female).

Note: The Faker library is used to generate realistic fake data for testing and demonstration purposes.
"""

# Imports
import pandas as pd
from faker import Faker
import numpy as np 
import random
from functions import exponential_decline, logarithmic_decline, stepwise_decline

# Create a Faker object
fake = Faker(use_weighting=True, locale='en_US', include_private=False)

# Set the seed
Faker.seed(4242)

# Set weights for 

# Generate customer data
customers = []
for _ in range(10000):
    customers.append({
        'id': fake.uuid4(),
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'registration_date': fake.date_between(start_date='-5y', end_date='today'),
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=65) if fake.boolean(chance_of_getting_true=95) else None, # 5% of missing birth dates
        'street_address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state() if fake.boolean(chance_of_getting_true=95) else None,
        'prefered_device': fake.random_element(elements=('Mobile' 'Desktop', 'Tablet')) if fake.boolean(chance_of_getting_true=90) else None, # 10% of missing prefered_device
        'email_opt_in': fake.boolean(chance_of_getting_true=40),
        'prefered_payment_methods': fake.random_element(elements=('Credit Card', 'Paypal', 'Apple Pay', 'Google Pay')),
        'gender': fake.random_element(elements=('male', 'female')),
        })

# Save the data to a DataFrame
customers_df = pd.DataFrame(customers)

# Generate sales data

# Define churn parameters
churn_rate = 0.20  # Overall churn rate (20%)
sudden_churn_ratio = 0.3  # 30% of churners will be sudden churners
reactivation_rate = 0.05  # 5% of churned customers will reactivate

# Assign churn behavior to customers
customers_df['churn_type'] = np.random.choice(
    ['no_churn', 'sudden_churn', 'gradual_churn'],
    p=[1 - churn_rate, sudden_churn_ratio * churn_rate, (1 - sudden_churn_ratio) * churn_rate],
    size=len(customers_df)
)

gradual_churners = customers_df[customers_df['churn_type'] == 'gradual_churn']
gradual_churners['churn_pattern'] = np.random.choice(
    ['exponential', 'logarithmic', 'stepwise'],
    size=len(gradual_churners)
)

customers_df.update(gradual_churners)

# Generate sales data over 12 months
start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2023-12-31')

sales_data = []
for _, customer in customers_df.iterrows():
    # Assign a random first_order_month between 1 and 12
    first_order_month = random.randint(1, 12)

    churn_month = None
    reactivation_month = None
    
    if customer['churn_type'] == 'sudden_churn':
        # Churn cannot be the first month
        churn_month = random.randint(max(2, first_order_month), 12) 
    elif customer['churn_type'] == 'gradual_churn':
        # Churn cannot be the first 3 months
        churn_month = random.randint(max(3, first_order_month), 12)

        if customer['churn_type'] != 'no_churn' and churn_month < 12:
            reactivation_month = random.randint(churn_month + 1, 12)

        for month in range(1, 13):
            if month < first_order_month:
                continue # Skip months before the first order

            if churn_month and month >= churn_month and (not reactivation_month or month < reactivation_month):
                continue 

            num_orders = fake.random_int(min=1, max=10)

            # Check if 'churn_pattern' exists before accessing it
            if 'churn_pattern' in customer:
                if customer['churn_pattern'] == 'stepwise':
                    decline_factor = stepwise_decline(month, churn_month, step_size=3)
                elif customer['churn_pattern'] == 'logarithmic':
                    decline_factor = logarithmic_decline(month, churn_month, base=2)
                elif customer['churn_pattern'] == 'exponential':
                    decline_factor = exponential_decline(month, churn_month, decay_rate=0.2)
                else:
                    raise ValueError("Invalid churn pattern")

                num_orders = int(num_orders * decline_factor) 

            for _ in range(num_orders):
                order_date = fake.date_between(start_date=start_date + pd.DateOffset(months=month-1),
                                               end_date=start_date + pd.DateOffset(months=month))
                total_amount = fake.random_int(min=10, max=2000)
                sales_data.append({
                    'order_id': fake.uuid4(),
                    'customer_id': customer['id'],
                    'order_date': order_date,
                    'total_amount': total_amount
                })

# Drop the churn_type column
customers_df.drop(columns='churn_type', inplace=True)

sales_df = pd.DataFrame(sales_data)

if __name__ == '__main__':
    print('Customer data has been generated and saved to data/customers.csv')
    print('Sales data has been generated and saved to data/sales.csv')

    # Export the customers csv file 
    customers_df.to_csv('../data/customers.csv', index=False)

    # Export the sales csv file
    sales_df.to_csv('../data/sales.csv', index=False)
    
