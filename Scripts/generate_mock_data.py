import os
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUTPUT_DIR = "data-warehouse/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Generating Customers & Accounts...")

TIERS = ["Starter", "Professional", "Enterprise"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]

customers = []
for i in range(1, 201):
    tier = random.choices(TIERS, weights=[0.5, 0.35, 0.15])[0]
    customers.append({
        "customer_id": f"CUST-{i:04d}",
        "company_name": fake.company(),
        "industry": fake.job().split()[-1].capitalize() + " Tech",
        "region": random.choice(REGIONS),
        "tier": tier,
        "signup_date": fake.date_between(start_date="-2y", end_date="-6m").isoformat()
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(f"{OUTPUT_DIR}/dim_customers.csv", index=False)

print("Generating Product Plans...")

products = [
    {"product_id": "PROD-01", "product_name": "MetricMind Starter", "monthly_price": 99, "billing_cycle": "Monthly"},
    {"product_id": "PROD-02", "product_name": "MetricMind Pro Annual", "monthly_price": 299, "billing_cycle": "Annual"},
    {"product_id": "PROD-03", "product_name": "MetricMind Enterprise Core", "monthly_price": 999,
     "billing_cycle": "Annual"},
    {"product_id": "PROD-04", "product_name": "AI Copilot Add-On", "monthly_price": 150, "billing_cycle": "Monthly"}
]

df_products = pd.DataFrame(products)
df_products.to_csv(f"{OUTPUT_DIR}/dim_products.csv", index=False)

print("Generating Fact Transactions...")

start_date = datetime(2024, 1, 1)
end_date = datetime.now()

transactions = []
tx_id = 10001

for cust in customers:
    cust_id = cust["customer_id"]
    c_signup = datetime.strptime(cust["signup_date"], "%Y-%m-%d")

   
    if cust["tier"] == "Enterprise":
        prod = products[2]
    elif cust["tier"] == "Professional":
        prod = products[1]
    else:
        prod = products[0]

    curr_date = c_signup
    active = True

    while curr_date < end_date and active:

        discount = random.choices([0.0, 0.1, 0.2], weights=[0.8, 0.15, 0.05])[0]
        amount = round(prod["monthly_price"] * (1 - discount), 2)

        transactions.append({
            "transaction_id": f"TXN-{tx_id}",
            "customer_id": cust_id,
            "product_id": prod["product_id"],
            "transaction_date": curr_date.strftime("%Y-%m-%d"),
            "amount": amount,
            "currency": "USD",
            "status": random.choices(["Settled", "Refunded", "Failed"], weights=[0.94, 0.04, 0.02])[0]
        })

        tx_id += 1


        curr_date += timedelta(days=30)

        if random.random() < 0.03:
            active = False

df_tx = pd.DataFrame(transactions)
df_tx.to_csv(f"{OUTPUT_DIR}/fact_transactions.csv", index=False)

print(f"Data generation complete! Saved files to '{OUTPUT_DIR}/'.")
print(f"Total Transactions Generated: {len(df_tx)}")
