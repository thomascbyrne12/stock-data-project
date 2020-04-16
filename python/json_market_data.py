# Import Dependencies
import requests
import json
from config import api_key

# Import Libraries to manipulate data
import pandas as pd
import numpy as np

# Import Libraries to display data
import seaborn as sns
import matplotlib.pyplot as plt

# SQL Alchemy Engine
from sqlalchemy import create_engine

# Flask App Dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Define variables
url = 'https://www.quandl.com/api/v3/datasets/EOD/HD?api_key='

# Extract api data
response = requests.get(url + api_key)
data = response.json()

# Creating a dataframe from the data to pull information from
data_df = pd.DataFrame(data)

# The closing, open, high, low, etc prices for each day in a grouped list. And column names respectively
bulk_price_data = (data_df.iat[3,0])
column_names = data_df.iat[2,0]

# Creating variables to reprsent types of information in the bulk_price_data
dates_data = []
open_values = []
high_values = []
low_values = []
close_values = []
volume_values = []
dividend_values = []
split_values = []
adj_open_values = []
adj_high_values = []
adj_low_values = []
adj_close_values = []
adj_volume_values = []

# Adding the appropriate type of information from bulk_price_data into each variable creaetd above
# Used an index for this because I was lazy and didn't want to type out each number
for days_data in bulk_price_data:
	index = 0
	dates_data.append(days_data[index])
	index += 1
	open_values.append(days_data[index])
	index += 1
	high_values.append(days_data[index])
	index += 1
	low_values.append(days_data[index])
	index += 1
	close_values.append(days_data[index])
	index += 1
	volume_values.append(days_data[index])
	index += 1
	dividend_values.append(days_data[index])
	index += 1
	split_values.append(days_data[index])
	index += 1
	adj_open_values.append(days_data[index])
	index += 1
	adj_high_values.append(days_data[index])
	index += 1
	adj_low_values.append(days_data[index])
	index += 1
	adj_close_values.append(days_data[index])
	index += 1
	adj_volume_values.append(days_data[index])
	index = 0

# Created a finalized dictionary for each bulk_price_data variable
finalized_dict = {
				'Date' : dates_data,
				'Open' : open_values,
				'High' : high_values,
				'Low' : low_values,
				'Close' : close_values,
				'Volume' : volume_values,
				'Dividend' : dividend_values,
				'Split' : split_values,
				'Adj Open' : adj_open_values,
				'Adj High' : adj_high_values,
				'Adj Low' : adj_low_values,
				'Adj Close' : adj_close_values,
				'Adj Volume' : adj_volume_values,
}

# Created a pandas dataframe from finalized_dict
stock_info_df = pd.DataFrame(finalized_dict)

# Indicators
def moving_average(dataframe,range_length):
	"""Creating a moving average list of numbers from a dataframe
		Range = length of moving average
		Dataframe = source of info with 'Close' and 'Date' values
	"""

	# Pull the data from the dataframe
	price_list = dataframe['Close'].tolist()[::-1]
	date_list = dataframe['Date'].tolist()[::-1]

	# Create empties to fill with info, and then make a dict from them
	moving_average_values = []
	moving_average_dates = []
	moving_average_dict = {"Value" : moving_average_values, "Date" : moving_average_dates}

	# Index to keep track of which variable to start/end from
	current_idx = int(range_length)

	# Add moving average and date value to the empty lists
	for price in price_list[range_length-1:]:
		moving_average_values.append(sum(price_list[current_idx-range_length:current_idx])/range_length)
		moving_average_dates.append(date_list[current_idx-1])
		current_idx += 1
	print(moving_average_dict['Value'])
	return moving_average_dict

# Establish connection and write to SQL file
database_path = 'postgresql://postgres:postgres@localhost:5432/stock_info_data'
engine = create_engine(f'sql:///{database_path}', echo = False)
conn = engine.connect()
stock_info_df.to_sql(name='stock_info_data', con=conn, if_exists='replace', \
						schema='stockdata', chunksize=20, method='multi')

# Write to CSV file
stock_info_df.to_csv('stock_info_data.csv', index = False, header = True)

# Create a basic line chart from date and close from stock info dataframe
plt.figure(figsize= (20,9))
sns.lineplot(data = stock_info_df, x='Date', y='Close')

# Create a moving average line chart
sns.lineplot(data = moving_average(stock_info_df,50), x='Date', y='Value')
plt.show()
