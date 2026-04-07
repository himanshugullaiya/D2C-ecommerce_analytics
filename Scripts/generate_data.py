import os
from pathlib import Path
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta, date


fake = Faker('en_IN')   # names, addresses, phone numbers will be indian format - not american/british. Data realistic to indian D2C Company
random.seed(42)
np.random.seed(42)

#............................CUSTOMERS.....................#

def cleaned_city_state():
    city_df = pd.read_csv("../Data/Bronze/city_state.csv")
    city_df['city'] = city_df['city'].apply(lambda x : x.replace('\x81',''))   #remove corrupted characters
    city_df['state'] = city_df['state'].apply(lambda x : x.replace('\x81',''))
    return city_df


def generate_customers(n = 15000):   #list of dictionaries
    city_df = cleaned_city_state()
    data = []
    for x in range(1,n+1):
        city_state = city_df.loc[random.choice(city_df.index)]
        fname,lname = fake.first_name(), fake.last_name()
        data_entry = {
            'customer_id' : f'CUST_{x:05d}',
            'first_name' :  fname,
            'last_name' :   lname,
            'city'     :    city_state['city'],
            'state'    : city_state['state'],
            'gender' : random.choice(['Male', 'Female']),
            'age' : random.randint(18, 50) if random.random() < 0.70 else random.randint(51, 70),   #such that 70% data is young
            'email' : fname + '_' + lname + str(np.random.randint(10,99)) + '@' + random.choice(['gmail', 'hotmail', 'yahoo']) + '.com',
            'signup_date' : fake.date_between(datetime(2023,1,1), datetime(2025,12,31)),
            'acquisition_channel' : random.choices(['organic','paid','referral'], weights = [40,40,20])[0],
            'phone' : '9' + str(np.random.randint(100000000, 999999999)),
            'pincode' : np.random.randint(110001, 855117)
        }
        data.append(data_entry)
    return pd.DataFrame(data)

print('Generating Customers \n')
customers_df = generate_customers()
customers_df.to_csv('../Data/Silver/customers.csv', index = False)

#......................Clothing............#


products_catalog = {
        'electronics' : {
            'phone' : {
                'Samsung': ['Galaxy S23', 'Galaxy A54', 'Galaxy M34', 'Galaxy F14'],
                'Apple': ['iPhone 14', 'iPhone 13', 'iPhone 14 Pro', 'iPhone 12'],
                'Xiaomi': ['Redmi Note 12', 'Redmi Note 11', 'Mi 11X', 'Poco X5']
                },
            
            'television' : {
                'Samsung': ['Crystal 4K 43', 'QLED 55', 'Frame TV 50'],
                'Apple': [],
                'Xiaomi': ['Mi TV 4X 43', 'Mi TV 5X 50', 'Mi QLED 55']
                },
            
            'laptop' : {
                 'Samsung': ['Galaxy Book 2', 'Galaxy Book Pro'],
                 'Apple': ['MacBook Air M1', 'MacBook Air M2', 'MacBook Pro 14'],
                 'Xiaomi': ['Mi Notebook 14', 'Mi Notebook Pro']
                }
            },
        
         'clothing': {
                't-shirts': {
                    'Levis': ['Original Fit Tee', 'Graphic Tee', 'Slim Fit Tee'],
                    'Arrow': ['Classic Cotton Tee', 'Sport Tee'],
                    'Zara': ['Basic Cotton Tee', 'Printed Tee', 'Oversized Tee']
                },
                'shirts': {
                    'Levis': ['Classic Western Shirt', 'Slim Fit Shirt'],
                    'Arrow': ['Formal Shirt', 'Casual Linen Shirt', 'Oxford Shirt'],
                    'Zara': ['Printed Shirt', 'Linen Shirt']
                },
                'trousers': {
                    'Levis': ['511 Slim', '501 Original', '514 Straight'],
                    'Arrow': ['Formal Trousers', 'Chinos'],
                    'Zara': ['Straight Fit Trouser', 'Tapered Trouser']
                },
                'dresses': {
                    'Levis': ['Denim Dress', 'Shirt Dress'],
                    'Arrow': [],
                    'Zara': ['Floral Midi Dress', 'Wrap Dress', 'Mini Dress']
                },
                'jackets': {
                    'Levis': ['Trucker Jacket', 'Sherpa Jacket'],
                    'Arrow': ['Blazer Jacket', 'Quilted Jacket'],
                    'Zara': ['Bomber Jacket', 'Trench Coat', 'Puffer Jacket']
                }
            },
            'sports & fitness': {
                'supplements': {
                    'MuscleBlaze': ['Whey Protein 1kg', 'Whey Protein 2kg', 'Creatine 250g', 'BCAA 250g'],
                    'Decathlon': ['Energy Bar Pack', 'Recovery Drink'],
                    'Yonex': []
                },
                'rackets & equipment': {
                    'Yonex': ['Voltric 50', 'Astrox 88S', 'Nanoray 900', 'Duora Z Strike'],
                    'Decathlon': ['Perfly BR 900', 'Artengo Tennis Racket'],
                    'MuscleBlaze': []
                },
                'footwear': {
                    'Decathlon': ['Kiprun Shoes', 'Kalenji Run Support', 'Newfeel Walking Shoe'],
                    'Yonex': ['Power Cushion 65Z', 'SHB 65X2'],
                    'MuscleBlaze': []
                },
                'fitness accessories': {
                    'MuscleBlaze': ['Resistance Band Set', 'Gym Gloves', 'Shaker Bottle'],
                    'Decathlon': ['Yoga Mat', 'Jump Rope', 'Foam Roller'],
                    'Yonex': ['Badminton Grip', 'Shuttlecock Pack']
                }
            }
                
        }

price_ranges = {
        'phone':               (15000, 120000),
        'laptop':              (50000, 300000),
        'television':          (15000, 200000),
        't-shirts':            (299,   2999),
        'shirts':              (499,   4999),
        'trousers':            (699,   5999),
        'dresses':             (599,   6999),
        'jackets':             (999,   9999),
        'supplements':         (499,   6999),
        'rackets & equipment': (299,   15000),
        'footwear':            (999,   12999),
        'fitness accessories': (199,   3999)
    }

def generate_products():
    all_products = []
    counter = 1 
    for category, subcategory in products_catalog.items():
        for subcategory, brand in subcategory.items():
            for brand, items in brand.items():
                for item in items:
                    data_entry = {
                        'product_id'  : 'PROD_'+f'{counter:03d}',
                        'product_name': item,
                        'category' : category,
                        'subcategory' : subcategory,
                        'brand' : brand,
                        'unit_price' : random.randint(*price_ranges[subcategory]),
                        }
                    counter += 1
                    all_products.append(data_entry)
    df = pd.DataFrame(all_products)
    df['cost_price'] = df['cost_price'] = (df['unit_price'] * np.random.uniform(0.40, 0.70, size=len(df))).round(2)         #vary the cost price to create realistic margins  
    return df

print('Generating Products \n')                    
products_df = generate_products()            
products_df.to_csv('../Data/Silver/products.csv', index = False)

#.......................Orders..............#

def get_date(start_date, for_order_date_gen = 1):
    end_date = date(2025,12,31)
    
    if for_order_date_gen == 1 : 
        days_between = (end_date - start_date).days
        n = random.randint(0,days_between)
        return start_date + timedelta(days = n)
    
    else:
        days_between = 15
        n = random.randint(1,days_between)
        return start_date + timedelta(days = n)
    
    

def generate_orders_with_items():
    orders_list = []
    order_items_list = []
    order_id = 1
    
    active_customers = customers_df[customers_df['customer_id'].isin(customers_df['customer_id'].sample(frac = 0.85))][['customer_id', 'signup_date']]
    
    for index, customer_row in active_customers.iterrows():
        print(f'\rWorking : {order_id}', end = " ", flush = True)
        total_orders = max(1, np.random.poisson(lam = 8))
        
        for cust_ord in range(total_orders):
            curr_order = {
                'order_id' : 'ORD_'+f'{order_id:05d}',
                'order_date' : get_date(customer_row['signup_date']),
                'customer_id': customer_row['customer_id'],
                'order_status': random.choice(['Delivered', 'Shipped']) if random.random() < 0.8 else random.choice(['Cancelled', 'Returned' ])
                }
            
            order_total = 0
            
            for order_item in range(1,random.randint(2,6)):
                product_row_index = random.choices(products_df.index)[0]
                random_qty = random.randint(1,5)
                
                curr_order_item = {
                    'order_id' : curr_order['order_id'],
                    'order_item_id' : str(curr_order['order_id']) + '#' + f'{order_item:02d}',
                    'product_id' : products_df.loc[product_row_index]['product_id'],
                    'qty' : random_qty,
                    'unit_price_at_purchase' : products_df.loc[product_row_index]['unit_price'],
                    'total_sales_curr_order' : random_qty * products_df.loc[product_row_index]['unit_price']
                    }
                
                order_total += curr_order_item['total_sales_curr_order']
                order_items_list.append(curr_order_item)
                
            curr_order['payement_method'] = random.choice(['UPI','Card']) if order_total < 100000 else random.choice(['Card', 'Net Banking'])
            curr_order['order_amount'] = order_total
            curr_order['discount_amount'] = 0.15*order_total if random.random() < 0.3 else 0  #( 15% discount)
            curr_order['net_amount'] = order_total - curr_order['discount_amount']
            orders_list.append(curr_order)
            order_id += 1
            
    return (pd.DataFrame(orders_list), pd.DataFrame(order_items_list))
                                                                                                          
print('Generating Orders \n')           
orders_df, order_items_df = generate_orders_with_items()        
                
orders_df.to_csv('../Data/Silver/orders.csv', index = False)
order_items_df.to_csv('../Data/Silver/order_items.csv', index = False)             
              
#.....................RETURNS  TABLE..................#

def generate_returns():
    all_returns = []
    returned_orders = orders_df[orders_df['order_status'] == 'Returned'][['order_id','order_date','customer_id', 'order_amount']].reset_index(drop = True)
    total_returns = returned_orders.shape[0]
    pad_size = len(str(total_returns))
    for x in range(0,total_returns):
        return_row = {
            'return_id' : 'RET_'+f'{x+1:0{pad_size}d}',
            'order_id' : returned_orders['order_id'].iloc[x],
            'customer_id': returned_orders['customer_id'].iloc[x],
            'return_date' : get_date(returned_orders['order_date'].iloc[x],0),
            'return_reason': random.choice(['Bad Quality', 'Damaged', 'No Longer Required', 'Wrong Item Delivered', 'Color Mismatch', 'Size Issues']),
            'return_amount' : returned_orders['order_amount'].iloc[x],
            'return_status' : random.choice(['refund_in_process', 'refunded'])
            }
        all_returns.append(return_row)
    return pd.DataFrame(all_returns)


print('Generating Returns \n')

return_orders = generate_returns()
return_orders.to_csv('../Data/Silver/returns.csv', index=False)        
        
print('All Generated')
    
    
    
    
    
        

        
        
        
        
        
        
    





