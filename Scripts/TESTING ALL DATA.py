import pandas as pd 
import numpy as np

og_oi_df = pd.read_csv('../Data/Silver/order_items.csv')
og_o_df = pd.read_csv('../Data/Silver/orders.csv')

print('\nGenerated Clean Data---------------')
print(f'\nOG SHAPE \nOI :  {og_oi_df.shape}, O : {og_o_df.shape}')
print(len(og_oi_df.loc[~og_oi_df['order_id'].isin(og_o_df['order_id']), 'order_id']))
print(len(og_o_df.loc[~og_o_df['order_id'].isin(og_oi_df['order_id']), 'order_id']))


dirty_oi_df = pd.read_csv('../Data/Bronze/dirty_order_items.csv')
dirty_o_df = pd.read_csv('../Data/Bronze/dirty_orders.csv')

print('\nAfter Dirtying The Data from Bronze -------------')
print(f'\nDIRTY SHAPE \nOI :  {dirty_oi_df.shape}, O : {dirty_o_df.shape}')
print(len(dirty_oi_df.loc[~dirty_oi_df['order_id'].isin(dirty_o_df['order_id']), 'order_id']))
print(len(dirty_o_df.loc[~dirty_o_df['order_id'].isin(dirty_oi_df['order_id']), 'order_id']))

cleaned_oi_df = pd.read_csv('../Data/Silver/Cleaned/clean_order_items.csv')
cleaned_o_df = pd.read_csv('../Data/Silver/Cleaned/clean_orders.csv')

print('\nAfter Cleaning--------------')
print(f'\nCLEANED SHAPE \nOI :  {cleaned_oi_df.shape}, O : {cleaned_o_df.shape}')
print(len(cleaned_oi_df.loc[~cleaned_oi_df['order_id'].isin(cleaned_o_df['order_id']), 'order_id']))
print(len(cleaned_o_df.loc[~cleaned_o_df['order_id'].isin(cleaned_oi_df['order_id']), 'order_id']))
