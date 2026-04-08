import pandas as pd 
import numpy as np

og_oi_df = pd.read_csv('../Data/Silver/order_items.csv')
og_o_df = pd.read_csv('../Data/Silver/orders.csv')

dirty_oi_df = pd.read_csv('../Data/Bronze/dirty_order_items.csv')
dirty_o_df = pd.read_csv('../Data/Bronze/dirty_orders.csv')
dirty_customers_df = pd.read_csv('../Data/Bronze/dirty_customers.csv')
dirty_returns_df = pd.read_csv('../Data/Bronze/dirty_returns.csv')
dirty_products_df = pd.read_csv('../Data/Bronze/dirty_products.csv')

cleaned_oi_df = pd.read_csv('../Data/Silver/Cleaned/clean_order_items.csv')
cleaned_o_df = pd.read_csv('../Data/Silver/Cleaned/clean_orders.csv')
cleaned_customers_df = pd.read_csv('../Data/Silver/Cleaned/clean_customers.csv')
cleaned_returns_df = pd.read_csv('../Data/Silver/Cleaned/clean_returns.csv')
cleaned_products_df = pd.read_csv('../Data/Silver/Cleaned/clean_products.csv')

def test_orphans():
    print("\n--*--*--*--*--*---*-----*--*--*--*--*-------\n")
    print('\nGenerated Clean Data')
    print(f'\nOG SHAPE \nOI :  {og_oi_df.shape}, O : {og_o_df.shape}')
    print(len(og_oi_df.loc[~og_oi_df['order_id'].isin(og_o_df['order_id']), 'order_id']))
    print(len(og_o_df.loc[~og_o_df['order_id'].isin(og_oi_df['order_id']), 'order_id']))
    
    print('\nAfter Dirtying The Data from Bronze')
    print(f'\nDIRTY SHAPE \nOI :  {dirty_oi_df.shape}, O : {dirty_o_df.shape}')
    print(len(dirty_oi_df.loc[~dirty_oi_df['order_id'].isin(dirty_o_df['order_id']), 'order_id']))
    print(len(dirty_o_df.loc[~dirty_o_df['order_id'].isin(dirty_oi_df['order_id']), 'order_id']))
    
    print('\nAfter Cleaning')
    print(f'\nCLEANED SHAPE \nOI :  {cleaned_oi_df.shape}, O : {cleaned_o_df.shape}')
    print(len(cleaned_oi_df.loc[~cleaned_oi_df['order_id'].isin(cleaned_o_df['order_id']), 'order_id']))
    print(len(cleaned_o_df.loc[~cleaned_o_df['order_id'].isin(cleaned_oi_df['order_id']), 'order_id']))


def test_duplicates():
    print("\n--*--*--*--*--*---*-----*--*--*--*--*-------\n")
    print("Total Dups in Dirty DF : \n")
    print(f"Orders      : {dirty_o_df.duplicated().sum()}")
    print(f"Order_items : {dirty_oi_df.duplicated().sum()}")
    print(f"Customers : {dirty_customers_df.duplicated().sum()}")
    print(f"Returns : {dirty_returns_df.duplicated().sum()}")
    print(f"Products : {dirty_products_df.duplicated().sum()}")
    
    print("\n\n\n\nTotal Dups in Cleaned DF : \n")
    
    print(f"Orders      : {cleaned_o_df.duplicated().sum()}")
    print(f"Order_items : {cleaned_oi_df.duplicated().sum()}")
    print(f"Customers : {cleaned_customers_df.duplicated().sum()}")
    print(f"Returns : {cleaned_returns_df.duplicated().sum()}")
    print(f"Products : {cleaned_products_df.duplicated().sum()}")
    
    print("\n\n\n\nTotal Dups in Cleaned DF on PKeys: \n")
    
    print(f"Orders      : {cleaned_o_df['order_id'].duplicated().sum()}")
    print(f"Order_items : {cleaned_oi_df['order_item_id'].duplicated().sum()}")
    print(f"Customers : {cleaned_customers_df['customer_id'].duplicated().sum()}")
    print(f"Returns : {cleaned_returns_df['return_id'].duplicated().sum()}")
    print(f"Products : {cleaned_products_df['product_id'].duplicated().sum()}")
    
def test_nulls():
    print("\n--*--*--*--*--*---*-----*--*--*--*--*-------\n")
    print("Total Nulls in Dirty DF : \n")
    print(f"Orders      : {dirty_o_df.isnull().sum()}")
    print(f"Order_items : {dirty_oi_df.isnull().sum()}")
    print(f"Customers : {dirty_customers_df.isnull().sum()}")
    print(f"Returns : {dirty_returns_df.isnull().sum()}")
    print(f"Products : {dirty_products_df.isnull().sum()}")
    
    print("\n\nTotal Nulls in Cleaned DF : \n")
    
    print(f"Orders      : {cleaned_o_df.isnull().sum()}")
    print(f"Order_items : {cleaned_oi_df.isnull().sum()}")
    print(f"Customers : {cleaned_customers_df.isnull().sum()}")
    print(f"Returns : {cleaned_returns_df.isnull().sum()}")
    print(f"Products : {cleaned_products_df.isnull().sum()}")
    
test_nulls()
test_duplicates()
test_orphans()


dup_customers = cleaned_customers_df.loc[cleaned_customers_df['customer_id'].duplicated(), 'customer_id']
checker_cust = cleaned_customers_df.loc[cleaned_customers_df['customer_id'].isin(dup_customers)].sort_values(by = 'customer_id')

dup_orders = cleaned_o_df.loc[cleaned_o_df['order_id'].duplicated(), 'order_id']
checker_orders = cleaned_o_df.loc[cleaned_o_df['order_id'].isin(dup_orders)].sort_values(by = 'order_id')
