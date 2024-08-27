#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:38:35 2024

@author: danielhill
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

#Load cleaned dataset
df = pd.read_excel('combined_df FINAL 2023 Q4 added.xlsx')

#Remove City of London because it is an outlier
df = df.drop(df[df['Force Name'] == 'London, City of'].index)

warnings.filterwarnings("ignore")  #Suppress warnings

def prepare_data(df, crime_type):
    crime_data = df[df['Offence Group'] == crime_type]
    crime_data = crime_data.groupby(['Financial Year', 'Financial Quarter'])['Number of Offences'].sum().reset_index()
    
    def quarter_to_month(quarter):
        quarter_map = {1: '04', 2: '07', 3: '10', 4: '01'}
        return quarter_map[quarter]
    
    crime_data['Date'] = crime_data['Financial Year'].str[:4] + '-' + crime_data['Financial Quarter'].apply(quarter_to_month)
    
    crime_data.loc[crime_data['Financial Quarter'] == 4, 'Date'] = (
        (pd.to_datetime(crime_data.loc[crime_data['Financial Quarter'] == 4, 'Financial Year'].str[:4]) + pd.DateOffset(years=1)).dt.strftime('%Y') + '-01'
    )
    
    crime_data['Date'] = pd.to_datetime(crime_data['Date'])
    crime_data.set_index('Date', inplace=True)
    crime_data.sort_index(inplace=True)
    return crime_data['Number of Offences']

def evaluate_window_size(data, window_sizes):
    results = []
    for window in window_sizes:
        mae_list = []
        rmse_list = []
        for i in range(len(data) - window):
            train = data.iloc[i:i+window]
            test = data.iloc[i+window]
            try:
                model = auto_arima(train, start_p=1, start_q=1, max_p=3, max_q=3, m=4,
                                   start_P=0, seasonal=True, d=1, D=1, trace=False,
                                   error_action='ignore', suppress_warnings=True, stepwise=True)
                forecast = model.predict(n_periods=1)
                mae = mean_absolute_error([test], forecast)
                rmse = np.sqrt(mean_squared_error([test], forecast))
                mae_list.append(mae)
                rmse_list.append(rmse)
            except:
                print(f"Error occurred for window size {window} at index {i}")
        if mae_list:  #Only append results if we have successful forecasts
            results.append({
                'window': window,
                'mae': np.mean(mae_list),
                'rmse': np.mean(rmse_list)
            })
    return pd.DataFrame(results)

#Prepare data for a specific crime type
crime_type = 'Violence against the person'
data = prepare_data(df, crime_type)

#Define window sizes to test (in quarters)
window_sizes = range(4, 21)  # Test windows from 4 quarters (1 year) to 20 quarters (5 years)

#Evaluate different window sizes
results = evaluate_window_size(data, window_sizes)

#Plot results
plt.figure(figsize=(12, 6))
plt.plot(results['window'], results['mae'], label='MAE')
plt.plot(results['window'], results['rmse'], label='RMSE')
plt.xlabel('Window Size (Quarters)')
plt.ylabel('Error')
plt.title(f'Forecast Error vs Window Size for {crime_type}')
plt.legend()
plt.show()

#Find optimal window size
optimal_window = results.loc[results['mae'].idxmin(), 'window']
print(f"Optimal window size: {optimal_window} quarters")

#Print full results
print(results)

