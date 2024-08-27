#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:18:51 2024

@author: danielhill
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

#Load the data
df = pd.read_excel('combined_df FINAL 2023 Q4 added.xlsx')

#Prepare and filter the data for running single place and crime type combination
place = 'Avon & Somerset'
crime_type = 'Criminal damage and arson'

filtered_df = df[(df['Force Name'] == place) & (df['Offence Group'] == crime_type)]

#Function to map financial quarter to the correct month
def quarter_to_month(year, quarter):
    quarter_month_map = {1: 4, 2: 7, 3: 10, 4: 1}
    month = quarter_month_map[quarter]
    
    # Adjust year for Q4 (January)
    if quarter == 4:
        year = str(int(year[:4]) + 1)
    else:
        year = year[:4]
    
    return f"{year}-{month:02d}"

#Convert Financial Year and Quarter to a datetime
filtered_df['Date'] = pd.to_datetime(
    filtered_df.apply(lambda row: quarter_to_month(row['Financial Year'], row['Financial Quarter']), axis=1),
    format='%Y-%m'
)

filtered_df.set_index('Date', inplace=True)
filtered_df.sort_index(inplace=True)

#Ensure the data is sorted by the period
filtered_df.sort_index(inplace=True)

#Select the target variable
y = filtered_df['Number of Offences']

#Define the number of quarters to predict
n_quarters = 12

#Split data into training and testing sets
train = y[:-n_quarters]
test = y[-n_quarters:]

#Fit the Holt-Winters Exponential Smoothing model on the entire dataset
model = ExponentialSmoothing(y, trend='add', seasonal='add', seasonal_periods=4, damped=True)
results = model.fit(optimized=True)

#Generate in-sample predictions
in_sample_predictions = results.fittedvalues

#Calculate errors
errors = y - in_sample_predictions

#Calculate error metrics
mae = mean_absolute_error(y, in_sample_predictions)
rmse = np.sqrt(mean_squared_error(y, in_sample_predictions))
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Square Error: {rmse}")

#Plot the results (Observed vs Fitted)
plt.figure(figsize=(12, 6))
plt.plot(y.index, y, label='Observed')
plt.plot(in_sample_predictions.index, in_sample_predictions, color='red', label='Fitted')
plt.title(f'Exponential Smoothing In-Sample Fit: {place} - {crime_type}', fontsize=14)
plt.xlabel('Period', fontsize=14)
plt.ylabel('Number of Offences', fontsize=14)
plt.xticks(fontsize=14)  # Increase x-axis tick label font size
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.show()

#Plot the prediction errors
plt.figure(figsize=(12, 6))
plt.plot(errors.index, errors, label='Error')
plt.axhline(y=0, color='r', linestyle='-')
plt.title(f'Exponential Smoothing In-Sample Fit: {place} - {crime_type}', fontsize=14)
plt.xlabel('Period', fontsize=14)
plt.ylabel('Error (Observed - Fitted)', fontsize=14)
plt.xticks(fontsize=14)  # Increase x-axis tick label font size
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.show()

#If you still want to generate and print future forecasts, you can keep this part:
n_quarters = 12
forecast = results.forecast(steps=n_quarters)
forecast_index = pd.date_range(start=y.index[-1] + pd.DateOffset(months=3), periods=n_quarters, freq='Q')

#Print forecasts for each quarter
for i, value in enumerate(forecast):
    print(f"Forecast for Quarter {i+1}: {value}")
