import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

customers_df  = pd.read_csv('../Data/Silver/customers.csv')
orders_df     = pd.read_csv('../Data/Silver/orders.csv')
order_items_df= pd.read_csv('../Data/Silver/order_items.csv')
products_df   = pd.read_csv('../Data/Silver/products.csv')
returns_df    = pd.read_csv('../Data/Silver/returns.csv')

def inject_nulls():
    #... customers :  5% Email, phone to be set as Null
    #... orders    :  3% payement_method to null
    #... order_items: 2% qty to null
    
    c_null_index = np.random.choice(customers_df.index, size = int(len(customers_df)*0.05), replace = False)
    customers_df.loc[c_null_index, ['email', 'phone']] = np.nan  #you must use column names, inside the loc for update on OG
    
    o_null_index = np.random.choice(orders_df.index, size = int(len(orders_df)*0.05), replace = False)
    orders_df.loc[o_null_index, ['payement_method']] = np.nan 
    
    oi_null_index = np.random.choice(order_items_df.index, size = int(len(order_items_df)*0.02), replace = False)
    order_items_df.loc[oi_null_index, ['qty']] = np.nan
    
    return customers_df, orders_df, order_items_df

    
def inject_duplicates():
    #customers : 
    global customers_df, orders_df, order_items_df
    c_index = np.random.choice(customers_df.index, size = int(len(customers_df)*0.05), replace = False) #random choices for duplicates
    customers_df = pd.concat([customers_df, customers_df.loc[c_index]], ignore_index = True)  #append new_duplicates
    customers_df = customers_df.sample(frac = 1, random_state = 10).reset_index(drop = True)  #shuffle
    
    o_index = np.random.choice(orders_df.index, size = int(len(orders_df)*0.05), replace = False)
    orders_df = pd.concat([orders_df, orders_df.loc[o_index]], ignore_index = True)
    orders_df = orders_df.sample(frac = 1, random_state = 10).reset_index(drop = True)
    
    oi_index = np.random.choice(order_items_df.index, size = int(len(order_items_df)*0.02), replace = False)
    order_items_df = pd.concat([order_items_df, order_items_df.loc[oi_index]], ignore_index = True)
    order_items_df = order_items_df.sample(frac = 1, random_state = 10).reset_index(drop = True)
    
    return customers_df, orders_df, order_items_df
    
def inject_date_formats():
    
    ord_index = np.random.choice(orders_df.index, size = int(0.3*len(orders_df)), replace = False)  
    ord_index_1 = ord_index[:int(len(ord_index)*0.6)]
    ord_index_2 = ord_index[int(len(ord_index)*0.6)+1 : ]
    orders_df.loc[ord_index_1, 'order_date'] = orders_df.loc[ord_index_1, 'order_date'].str.replace('-','/', regex = False)
    orders_df.loc[ord_index_2, 'order_date'] = pd.to_datetime(orders_df.loc[ord_index_2, 'order_date']).apply(lambda x : x.strftime('%d %B %Y'))
    
    ret_index = np.random.choice(returns_df.index, size = int(0.3*len(returns_df)), replace = False)
    ret_index_1 = ret_index[:int(len(ret_index)*0.3)]
    ret_index_2 = ret_index[int(len(ret_index)*0.3)+1:]
    returns_df.loc[ret_index_1, 'return_date'] = returns_df.loc[ret_index_1, 'return_date'].str.replace('-','/', regex = False)
    returns_df.loc[ret_index_2, 'return_date'] = pd.to_datetime(returns_df.loc[ret_index_2, 'return_date']).apply(lambda x : x.strftime('%d %B %Y'))
    

def inject_outliers():
    sampled_products = products_df.sample(frac = 0.02)
    for x in range(len(sampled_products)):
        products_df.loc[sampled_products.index[x], 'unit_price'] = random.choice([np.random.randint(5), np.random.randint(90000, 100000)])
        
    sampled_orders = orders_df.sample(frac = 0.02)
    for x in range(len(sampled_orders)):
        ord_amt = sampled_orders.iloc[x]['order_amount']
        orders_df.loc[sampled_orders.index[x], 'order_amount'] = random.choice([ord_amt*1000, ord_amt*0.001])
        
def inject_inconsistent_values():
    sample_orders = np.random.choice(orders_df.index, size = int(0.1*len(orders_df)), replace = False)
    orders_df.loc[sample_orders, 'payement_method'] = orders_df.loc[sample_orders, 'payement_method'].apply(lambda x : x.lower() if isinstance(x,str) else x)
    
    sample_customers = np.random.choice(customers_df.index, size = int(0.1*len(customers_df)), replace = False)
    customers_df.loc[sample_customers, 'city'] = customers_df.loc[sample_customers, 'city'].apply(lambda x : x.upper() if isinstance(x,str) else x)
    
def inject_invalid_values():
    sample_customers = np.random.choice(customers_df.index, size = int(0.02*len(customers_df)), replace = False)
    customers_df.loc[sample_customers, 'age'] = -1*customers_df.loc[sample_customers, 'age']

    sample_oi = np.random.choice(order_items_df.index, size = int(0.02*len(order_items_df)), replace = False)
    order_items_df.loc[sample_oi, 'qty'] = 0
    
def inject_orphans():
    sample_orders = np.random.choice(orders_df.index, size = int(0.02*len(orders_df)), replace = False)
    orders_df.loc[sample_orders, 'customer_id'] = [f'CUST_{np.random.randint(99999,9999999)}' for _ in range(len(sample_orders))]
    
    
def dirty_pipeline():
    inject_nulls()
    inject_duplicates()
    inject_date_formats()
    inject_inconsistent_values()
    inject_invalid_values()
    inject_orphans()
    inject_outliers()
    


dirty_pipeline()

customers_df.to_csv('../Data/Bronze/dirty_customers.csv', index = False)
orders_df.to_csv('../Data/Bronze/dirty_orders.csv', index = False)
order_items_df.to_csv('../Data/Bronze/dirty_order_items.csv', index = False)
products_df.to_csv('../Data/Bronze/dirty_products.csv', index = False)
returns_df.to_csv('../Data/Bronze/dirty_returns.csv', index = False)
    
    
    
    
    
    
    
    

    
    
    
    
    