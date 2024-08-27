#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:22:58 2024

@author: danielhill
"""

import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

#Load the data
df = pd.read_excel('combined_df FINAL 2023 Q4 added.xlsx')

#Prepare and filter the data
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

#Create a time series
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

#Check for seasonality
result = seasonal_decompose(ts, model='additive', period=4)
result.plot()
plt.show()

#Store the results
results_dict = {}

#Define the number of quarters to forecast
n_quarters = 12

#Define a dictionary with optimal ARIMA parameters for each crime type
#These parameters should be determined beforehand using auto arima code
crime_type_params = {
    'Criminal damage and arson': (15, 1, 1),
    'Drug offences': (19, 1, 1),
    'Miscellaneous crimes against society': (18, 1, 1),
    'Possession of weapons offences': (14, 1, 1),
    'Public order offences': (10, 1, 1),
    'Robbery': (19, 1, 1),
    'Sexual offences': (10, 1, 1),
    'Theft offences': (14, 1, 1),
    'Violence against the person': (9, 1, 1)
}

#Iterate over each crime type
for crime_type, arima_params in crime_type_params.items():
    for place in df['Force Name'].unique():
        filtered_df = df[(df['Force Name'] == place) & (df['Offence Group'] == crime_type)]
        
        #Convert Financial Year and Quarter to a datetime
        filtered_df['Date'] = pd.to_datetime(
            filtered_df.apply(lambda row: quarter_to_month(row['Financial Year'], row['Financial Quarter']), axis=1),
            format='%Y-%m'
        )
        filtered_df.set_index('Date', inplace=True)
        filtered_df.sort_index(inplace=True)
        
        #Create time series
        ts = filtered_df['Number of Offences']
        
        #Differencing if necessary
        ts_diff = ts.diff().dropna() if arima_params[1] > 0 else ts
        
        #Fit ARIMA model with specific parameters for the crime type
        model = ARIMA(ts, order=arima_params)
        results = model.fit()
        
        #Forecast
        forecast = results.forecast(steps=n_quarters)
        
        #Store the results
        results_dict[(place, crime_type)] = {
            'observed': ts,
            'forecast': forecast
        }

#Dash application for interactive visualisation
app = Dash(__name__)

#Define the layout
app.layout = html.Div([
    html.H1('Crime Forecasting Dashboard'),
    html.Div([
        html.Label('Select Crime Type'),
        dcc.Dropdown(
            id='crime-dropdown',
            options=[{'label': crime_type, 'value': crime_type} for crime_type in crime_type_params.keys()],
            value=list(crime_type_params.keys())[0]  #Default value
        ),
    ]),
    html.Div([
        html.Label('Select Force Area'),
        dcc.Dropdown(
            id='force-dropdown',
            options=[],  #This will be populated based on selected crime type
            value=None
        ),
    ]),
    dcc.Graph(id='time-series-chart')
])

#Update force area dropdown based on selected crime type
@app.callback(
    Output('force-dropdown', 'options'),
    Input('crime-dropdown', 'value')
)
def set_force_options(selected_crime):
    forces = df[df['Offence Group'] == selected_crime]['Force Name'].unique()
    return [{'label': force, 'value': force} for force in forces]

#Define a set of problematic combinations
problematic_combinations = {
    ('Dyfed-Powys', 'Public order offences'),
    ('London, City of', 'Theft offences'),
    ('Devon & Cornwall', 'Criminal damage and arson'),
    ('Devon & Cornwall', 'Drug offences'),
    ('Devon & Cornwall', 'Miscellaneous crimes against society'),
    ('Devon & Cornwall', 'Possession of weapons offences'),
    ('Devon & Cornwall', 'Public order offences'),
    ('Devon & Cornwall', 'Robbery'),
    ('Devon & Cornwall', 'Sexual offences'),
    ('Devon & Cornwall', 'Theft offences'),
    ('Devon & Cornwall', 'Violence against the person')
}

#Modify the update_chart callback
@app.callback(
    Output('time-series-chart', 'figure'),
    Input('crime-dropdown', 'value'),
    Input('force-dropdown', 'value')
)
def update_chart(selected_crime, selected_force):
    if selected_crime and selected_force:
        if (selected_force, selected_crime) in problematic_combinations:
            #Create a figure with the error message
            fig = go.Figure()
            fig.add_annotation(
                text="Data unavailable due to quality issues",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
            fig.update_layout(
                title=f"{selected_force} - {selected_crime}",
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, showticklabels=False)
            )
            return fig
        
        data = results_dict.get((selected_force, selected_crime))
        if data:
            observed = data['observed']
            forecast = data['forecast'].round()  #Round the forecast to the nearest whole number

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=observed.index, y=observed, mode='lines', name='Observed'))
            fig.add_trace(go.Scatter(x=forecast.index, y=forecast, mode='lines', name='Forecast', line=dict(color='red')))
            fig.update_layout(title=f"{selected_force} - {selected_crime}", xaxis_title="Date", yaxis_title="Number of Offences")
            return fig
    return {}

#Run the app on http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run_server(debug=True)
