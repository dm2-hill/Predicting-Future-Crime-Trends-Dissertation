# Predicting future crime trends by area and crime type in England and Wales, using machine learning methods.

## Description
Crime is a global issue that can negatively impact the society in which it takes place in a number of ways. In recent years, governments have become increasingly committed to harnessing technology such as machine learning and artificial intelligence to tackle crime. This project investigated whether machine learning techniques can be used to predict future crime rates using time series forecasting. Police recorded crime data from the UK was used, covering the period from 2002-2023. A number of spatial and socio-economic variables were added to the data. 

This repository provides the code and data used in the project so that the results can be tested and replicated by other users. The code provided was used to prepare the data, perform exploratory analysis, build and run multiple linear regression and RNN-LSTM models, and to produce the associated dashboard using ARIMA.

## Installation

git clone https://github.com/dm2-hill/Predicting-Future-Crime-Trends-Dissertation

## Usage
All codes contain a line to read in the data, which is named 'combined_df FINAL 2023 Q4 added.xlsx'. This data is included in the repository, so once cloned to a local folder the code should be able to run with no problems. Every code is set up so that it should be run without any adjustments being required. 

### Data cleaning and preparation
The first code is named 'Data cleaning and preparation.py'. At initial download each year of the data was in a separate excel file. I put each of these onto separate sheets in the same excel file. I then loaded this data into python and ran this code. The code cleans the data by converting all zeros in the offence count column to NaN and then removing all rows with NaN. I then checked all column titles are the same across years, and changed any that were not. The code then removes any rows with a negative offence count as it is impossible to have a negative number of crimes. I then calculated the sum of number of offences for every force and offence group and combined everything into one excel file with one sheet. This has already been done in the data included in the Github repository so this code is included just for reference. 

### Exploratory analysis
The second code is 'Exploratory Analysis.py'. This creates a number of charts to visualise trends in the data. These include an overall line chart for UK crime, a stacked area chart, an interactive chart using plotly, heatmaps, bar charts by area, scatter plots to show trends, and a table of summary statistics. Lots of these are additional to what I was able to include in the report so can provide additional understanding of the data before proceeding. 

### Multiple Linear Regression and RNN-LSTM models
The third code is 'Regression and RNN-LSTM code.Rmd'. It is worth noting that this code is written in R, while all the others are written in Python. This is because I am most proficient at coding in R compared to Python. I have used mostly Python as I hoped to develop this skill over the course of the project. However, I had some difficulties with creating the RNN-LSTM model specifically in Python, so I switched to R just for this code, as I was starting to run low on time. As this is a markdown file, it can be run in chunks: 
- The first chunk does some data processing such as creating new geographic variables for Southern England, Northern England and Wales. 
- The second chunk creates the correlation matrix plot
- The third and fourth chunks create the multiple linear regression models. 
- The fifth and sixth chunks create the RNN-LSTM model, and produce observed vs predicted comparisons and error metrics. 
- The seventh chunk runs feature selection. 
- The remaining chunks run the RNN-LSTM model again with some of the lowest importance variable removed. 

### ARIMA and Exponential Smoothing comparison
The next codes are 'Arima prediction code.py' and 'Exponential smoothing.py'. These codes essentially do the same thing, by taking one example of area and crime type and running time series predictions. The sample used here and in the report is criminal damage and arson in Avon and Somerset. However, any combination of area and crime type could be used. The codes produce the same error charts, a comparison of which is available in the report. The main difference between them is that the ARIMA code produces differencing and seasonal decomposition to handle seasonality in the data. This was not required for exponential smoothing as this method handles seasonality well. 

### Auto ARIMA
The sixth code is 'auto arima.py'. This can be run before running 'Code for dashboard.py' to obtain the optimal number of past lags to use in ARIMA. This is already done but could be run again to compare performance between different numbers of lags. Once this was run for each crime type I manually updated the number in 'Code for dashboard.py'. 

### Code for dashboard
The final code is 'Code for dashboard.py'. This iterates through every combination of crime type and area and produces an ARIMA model, predicting the next 12 quarters of crime for each combination. The ARIMA parameters can be edited individually for each crime type on lines 80-90. Lines 124 onwards create the dashboard, as well as naming some area/crime type combinations that were problematic due to quality issues or missing data. For example, for some years Devon & Cornwall police did not record any crimes. This severely negatively affected predictions for this area. Therefore, I decided to display an error message in this circumstance. The final lines will run the dashboard on a local server. Once the code is run, the dashboard can be accessed on the following link if it does not open automatically - http://127.0.0.1:8050/


