import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine('postgresql://postgres:admin@localhost:5432/project')

# Read cleaned CSVs
customers_df   = pd.read_csv('../data/silver/Cleaned/clean_customers.csv')
orders_df      = pd.read_csv('../data/silver/Cleaned/clean_orders.csv')
order_items_df = pd.read_csv('../data/silver/Cleaned/clean_order_items.csv')
products_df    = pd.read_csv('../data/silver/Cleaned/clean_products.csv')
returns_df     = pd.read_csv('../data/silver/Cleaned/clean_returns.csv')

# Load to PostgreSQL silver schema
customers_df.to_sql('customers', engine, schema='silver', if_exists='replace', index=False)
print("customers loaded")

orders_df.to_sql('orders', engine, schema='silver', if_exists='replace', index=False)
print("orders loaded")

order_items_df.to_sql('order_items', engine, schema='silver', if_exists='replace', index=False)
print("order_items loaded")

products_df.to_sql('products', engine, schema='silver', if_exists='replace', index=False)
print("products loaded")

returns_df.to_sql('returns', engine, schema='silver', if_exists='replace', index=False)
print("returns loaded")

print("All tables loaded to PostgreSQL silver schema successfully.")