#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:26:04 2024

@author: danielhill
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose

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
    
    #Adjust year for Q4 (January)
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

#Create time series
ts = filtered_df['Number of Offences']

#Check for stationarity
def test_stationarity(timeseries):
    result = adfuller(timeseries, autolag='AIC')
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:', result[4])

test_stationarity(ts)

#Differencing by 1
ts_diff = ts.diff().dropna()

#Test stationarity on differenced series
print("\nResults for differenced series:")
test_stationarity(ts_diff)

#Perform seasonal decomposition to assess level of seasonality
result = seasonal_decompose(ts, model='additive', period=4)
result.plot()
plt.show()

#Define the number of quarters to predict
n_quarters = 12  # This will predict 3 years (12 quarters)

#Split data into training and testing sets
train = ts[:-n_quarters]
test = ts[-n_quarters:]

#Plot ACF and PACF to help determine p and q parameters
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8))
plot_acf(ts_diff, ax=ax1)
plot_pacf(ts_diff, ax=ax2)
plt.show()

#Fit the ARIMA model on the entire dataset
model = ARIMA(ts, order=(15, 1, 1))
results = model.fit()

#Generate in-sample predictions starting from the second period
in_sample_predictions = results.get_prediction(start=ts.index[1], end=ts.index[-1])
predicted_mean = in_sample_predictions.predicted_mean

#Calculate errors (aligning the indices)
errors = ts[predicted_mean.index] - predicted_mean

#Calculate error metrics
mae = mean_absolute_error(ts[predicted_mean.index], predicted_mean)
rmse = np.sqrt(mean_squared_error(ts[predicted_mean.index], predicted_mean))
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Square Error: {rmse}")

#Plot the results
plt.figure(figsize=(12, 6))
plt.plot(ts.index, ts, label='Observed')
plt.plot(predicted_mean.index, predicted_mean, color='red', label='Fitted')
plt.title(f'ARIMA In-Sample Fit: {place} - {crime_type}', fontsize=14)
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
plt.title(f'ARIMA In-Sample Fit: {place} - {crime_type}', fontsize=14)
plt.xlabel('Period', fontsize=14)
plt.ylabel('Error (Observed - Fitted)', fontsize=14)
plt.xticks(fontsize=14)  # Increase x-axis tick label font size
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.show()