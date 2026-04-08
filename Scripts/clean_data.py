import pandas as pd
import numpy as np
from datetime import datetime

dirty_customers_df  = pd.read_csv('../Data/Bronze/dirty_customers.csv')
dirty_orders_df     = pd.read_csv('../Data/Bronze/dirty_orders.csv')
dirty_order_items_df= pd.read_csv('../Data/Bronze/dirty_order_items.csv')
dirty_products_df   = pd.read_csv('../Data/Bronze/dirty_products.csv')
dirty_returns_df    = pd.read_csv('../Data/Bronze/dirty_returns.csv')

#... Remove rows where more than 4 columns are Null...#
dirty_customers_df  = dirty_customers_df.dropna(thresh = 4)
dirty_orders_df     = dirty_orders_df.dropna(thresh = 4)
dirty_order_items_df= dirty_order_items_df.dropna(thresh = 4)
dirty_products_df   = dirty_products_df.dropna(thresh = 4)
dirty_returns_df    = dirty_returns_df.dropna(thresh = 4)

    
    
#... Fix formatting inconsistencies...#

def fix_formatting():
    dirty_customers_df['city'] = dirty_customers_df['city'].str.title()
    dirty_orders_df['payement_method'] = dirty_orders_df['payement_method'].str.title()
    
    dirty_orders_df['order_date'] =   pd.to_datetime(dirty_orders_df['order_date'], dayfirst = True, errors = 'coerce')
    dirty_returns_df['return_date'] = pd.to_datetime(dirty_returns_df['return_date'], dayfirst = True, errors = 'coerce')
    
#... Fixing Null Values...#

def fix_nulls():
    dirty_customers_df['email'] = dirty_customers_df['email'].fillna('Unknown')
    dirty_customers_df['phone'] = dirty_customers_df['phone'].fillna('Unknown')
    
    dirty_orders_df['payement_method'] = dirty_orders_df['payement_method'].fillna('Unknown')
    
    #null_indices = np.where(dirty_order_items_df['qty'].isna())[0].tolist()
    #dirty_order_items_df.loc[null_indices, 'qty'] = (dirty_order_items_df.loc[null_indices, 'total_sales_curr_order'] / dirty_order_items_df.loc[null_indices, 'unit_price_at_purchase']).astype(int)
    
    #..better version..
    
    dirty_order_items_df['qty'] = dirty_order_items_df.apply(
    lambda row : int(row['total_sales_curr_order'] / row['unit_price_at_purchase'])    
    if pd.isna(row['qty']) else row['qty'], axis = 1 )
    
       
#....Fixing Invalid Data...#

def fix_invalid_data():
    
    dirty_customers_df.loc[dirty_customers_df['age'] < 0, 'age'] = int(dirty_customers_df[dirty_customers_df['age'] > 0]['age'].mean())
    dirty_order_items_df['qty'] = np.where(dirty_order_items_df['qty'] == 0, (dirty_order_items_df['total_sales_curr_order'] / dirty_order_items_df['unit_price_at_purchase']).astype(int), dirty_order_items_df['qty'])
    
    
#... Fixing orphan Records..#

def fix_orphan_records():
    global dirty_orders_df, dirty_order_items_df
    
    indices_to_remove = dirty_orders_df.loc[(~dirty_orders_df['customer_id'].isin(dirty_customers_df['customer_id'])), 'customer_id'].index
    order_ids_to_remove = dirty_orders_df.loc[indices_to_remove, 'order_id']
    
    dirty_orders_df = dirty_orders_df.drop(index = indices_to_remove).reset_index(drop = True)
    dirty_order_items_df = dirty_order_items_df[~dirty_order_items_df['order_id'].isin(order_ids_to_remove)].reset_index(drop = True)
    
    dirty_orders_df = dirty_orders_df[dirty_orders_df['order_id'].isin(dirty_order_items_df['order_id'])].reset_index(drop = True)
    
#... Fixing Outliers using IQR..#

def fix_outliers():
    global dirty_products_df, dirty_orders_df
    
    #Fix product unit_price outliers
    q1 = dirty_products_df['unit_price'].quantile(0.25)
    q3 = dirty_products_df['unit_price'].quantile(0.75)
    IQR = q3 - q1
    lower = q1 - 1.5 * IQR
    upper = q3 + 1.5 * IQR
    median_price = dirty_products_df['unit_price'].median()
    dirty_products_df.loc[
        (dirty_products_df['unit_price'] < lower) | 
        (dirty_products_df['unit_price'] > upper), 
        'unit_price'
    ] = median_price
    
    
    #Fix order_amount outlier
    
    q1 = dirty_orders_df['order_amount'].quantile(0.25)
    q3 = dirty_orders_df['order_amount'].quantile(0.75)
    IQR = q3 - q1
    lower = q1 - 1.5 * IQR
    upper = q3 + 1.5 * IQR
    median_price = dirty_orders_df['order_amount'].median()
    dirty_orders_df.loc[
        (dirty_orders_df['order_amount'] < lower) | 
        (dirty_orders_df['order_amount'] > upper),
        'order_amount'
    ] = median_price
    
    
#... Remove duplicate rows....#

def remove_duplicates():
    global dirty_customers_df
    global dirty_orders_df
    global dirty_order_items_df

    print('Row Dups Check : \n')
    dirty_customers_df.duplicated().value_counts() # No of true/false value
    dirty_orders_df.duplicated().value_counts()    # No of true/false value
    dirty_order_items_df.duplicated().value_counts()
    
    dirty_customers_df = dirty_customers_df.drop_duplicates()
    dirty_orders_df    = dirty_orders_df.drop_duplicates()
    dirty_order_items_df = dirty_order_items_df.drop_duplicates()
    
    print('Primary Key Dups Check : \n')
    
    dirty_customers_df['customer_id'].duplicated().value_counts()
    dirty_orders_df['order_id'].duplicated().value_counts()
    dirty_order_items_df['order_item_id'].duplicated().value_counts()
    
    #removing duplicate ids with imputed age    
    mean_age = int(dirty_customers_df['age'].mean())
    dup_customer_ids = dirty_customers_df.loc[dirty_customers_df['customer_id'].duplicated(), 'customer_id']  #find those id those are duplicated
    dirty_customers_df = dirty_customers_df[~((dirty_customers_df['customer_id'].isin(dup_customer_ids)) & (dirty_customers_df['age'] == mean_age))].sort_values('customer_id')
    
    #fixing order_ids with wrong order_amount and duplicate order_ids
    
    dirty_orders_df = dirty_orders_df.drop_duplicates(subset = 'order_id', keep = 'first').copy()
    dirty_orders_df['order_amount'] = dirty_orders_df['net_amount'] + dirty_orders_df['discount_amount']    
    

def clean_all():
    
    fix_formatting()
    fix_nulls()
    fix_invalid_data()
    fix_orphan_records()
    fix_outliers()
    remove_duplicates()
    
clean_all()

dirty_customers_df.to_csv('../Data/Silver/Cleaned/clean_customers.csv', index = False)
dirty_orders_df.to_csv('../Data/Silver/Cleaned/clean_orders.csv', index = False)
dirty_order_items_df.to_csv('../Data/Silver/Cleaned/clean_order_items.csv', index = False)
dirty_products_df.to_csv('../Data/Silver/Cleaned/clean_products.csv', index = False)
dirty_returns_df.to_csv('../Data/Silver/Cleaned/clean_returns.csv', index = False)

#....SANITY CHECK....#

print("Customers:", dirty_customers_df.shape)
print("Orders:", dirty_orders_df.shape)
print("Order Items:", dirty_order_items_df.shape)
print("Products:", dirty_products_df.shape)
print("Returns:", dirty_returns_df.shape)

# Check nulls remaining
print("Customer nulls:\n", dirty_customers_df.isnull().sum())
print("\nOrder nulls:\n", dirty_orders_df.isnull().sum())
print("\nOrder Items nulls:\n", dirty_order_items_df.isnull().sum())


