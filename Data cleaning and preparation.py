#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:22:54 2024

@author: danielhill
"""

import pandas as pd
import numpy as np

df = pd.read_excel("/Users/danielhill/Documents/Documents - Daniel’s MacBook Air/MSc Data Science/Dissertation/Police recorded crime data.xlsx",
                   sheet_name=['2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', 
                               '2009-10','2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015_16', 
                               '2016_17', '2017_18', '2018_19', '2019_20', '2020_21', '2021_22', '2022_23', 
                               '2023_24'])

# Access individual sheets using sheet names
sheet1_df = df['2002-03']
sheet2_df = df['2003-04']
sheet3_df = df['2004-05']
sheet4_df = df['2005-06']
sheet5_df = df['2006-07']
sheet6_df = df['2007-08']
sheet7_df = df['2008-09']
sheet8_df = df['2009-10']
sheet9_df = df['2010-11']
sheet10_df = df['2011-12']
sheet11_df = df['2012-13']
sheet12_df = df['2013-14']
sheet13_df = df['2014-15']
sheet14_df = df['2015_16']
sheet15_df = df['2016_17']
sheet16_df = df['2017_18']
sheet17_df = df['2018_19']
sheet18_df = df['2019_20']
sheet19_df = df['2020_21']
sheet20_df = df['2021_22']
sheet21_df = df['2022_23']
sheet22_df = df['2023_24']

#replace all zeros in offence count with NaN values
sheet1_df.replace(0, np.nan, inplace=True)
sheet2_df.replace(0, np.nan, inplace=True)
sheet3_df.replace(0, np.nan, inplace=True)
sheet4_df.replace(0, np.nan, inplace=True)
sheet5_df.replace(0, np.nan, inplace=True)
sheet6_df.replace(0, np.nan, inplace=True)
sheet7_df.replace(0, np.nan, inplace=True)
sheet8_df.replace(0, np.nan, inplace=True)
sheet9_df.replace(0, np.nan, inplace=True)
sheet10_df.replace(0, np.nan, inplace=True)
sheet11_df.replace(0, np.nan, inplace=True)
sheet12_df.replace(0, np.nan, inplace=True)
sheet13_df.replace(0, np.nan, inplace=True)
sheet14_df.replace(0, np.nan, inplace=True)
sheet15_df.replace(0, np.nan, inplace=True)
sheet16_df.replace(0, np.nan, inplace=True)
sheet17_df.replace(0, np.nan, inplace=True)
sheet18_df.replace(0, np.nan, inplace=True)
sheet19_df.replace(0, np.nan, inplace=True)
sheet20_df.replace(0, np.nan, inplace=True)
sheet21_df.replace(0, np.nan, inplace=True)
sheet22_df.replace(0, np.nan, inplace=True)

#Remove all rows with nan in offence count
sheet1_df = sheet1_df.dropna()
sheet2_df = sheet2_df.dropna()
sheet3_df = sheet3_df.dropna()
sheet4_df = sheet4_df.dropna()
sheet5_df = sheet5_df.dropna()
sheet6_df = sheet6_df.dropna()
sheet7_df = sheet7_df.dropna()
sheet8_df = sheet8_df.dropna()
sheet9_df = sheet9_df.dropna()
sheet10_df = sheet10_df.dropna()
sheet11_df = sheet11_df.dropna()
sheet12_df = sheet12_df.dropna()
sheet13_df = sheet13_df.dropna()
sheet14_df = sheet14_df.dropna()
sheet15_df = sheet15_df.dropna()
sheet16_df = sheet16_df.dropna()
sheet17_df = sheet17_df.dropna()
sheet18_df = sheet18_df.dropna()
sheet19_df = sheet19_df.dropna()
sheet20_df = sheet20_df.dropna()
sheet21_df = sheet21_df.dropna()
sheet22_df = sheet22_df.dropna()

#Rename so all column titles are the same
sheet14_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet15_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet16_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet17_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet18_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet19_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet20_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet21_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)
sheet22_df.rename(columns={'Offence Count': 'Number of Offences'}, inplace=True)

sheet14_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet15_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet16_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet17_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet18_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet19_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet20_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet21_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)
sheet22_df.rename(columns={'Police Force': 'Force Name'}, inplace=True)

#Delete any negative values from offence count
sheet1_df = sheet1_df[sheet1_df['Number of Offences'] >= 0]
sheet2_df = sheet2_df[sheet2_df['Number of Offences'] >= 0]
sheet3_df = sheet3_df[sheet3_df['Number of Offences'] >= 0]
sheet4_df = sheet4_df[sheet4_df['Number of Offences'] >= 0]
sheet5_df = sheet5_df[sheet5_df['Number of Offences'] >= 0]
sheet6_df = sheet6_df[sheet6_df['Number of Offences'] >= 0]
sheet7_df = sheet7_df[sheet7_df['Number of Offences'] >= 0]
sheet8_df = sheet8_df[sheet8_df['Number of Offences'] >= 0]
sheet9_df = sheet9_df[sheet9_df['Number of Offences'] >= 0]
sheet10_df = sheet10_df[sheet10_df['Number of Offences'] >= 0]
sheet11_df = sheet11_df[sheet11_df['Number of Offences'] >= 0]
sheet12_df = sheet12_df[sheet12_df['Number of Offences'] >= 0]
sheet13_df = sheet13_df[sheet13_df['Number of Offences'] >= 0]
sheet14_df = sheet14_df[sheet14_df['Number of Offences'] >= 0]
sheet15_df = sheet15_df[sheet15_df['Number of Offences'] >= 0]
sheet16_df = sheet16_df[sheet16_df['Number of Offences'] >= 0]
sheet17_df = sheet17_df[sheet17_df['Number of Offences'] >= 0]
sheet18_df = sheet18_df[sheet18_df['Number of Offences'] >= 0]
sheet19_df = sheet19_df[sheet19_df['Number of Offences'] >= 0]
sheet20_df = sheet20_df[sheet20_df['Number of Offences'] >= 0]
sheet21_df = sheet21_df[sheet21_df['Number of Offences'] >= 0]
sheet22_df = sheet22_df[sheet22_df['Number of Offences'] >= 0]

# Group by 'Force Name' and 'Offence Group' and sum the 'Number of Offences'
grouped_df1 = sheet1_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df2 = sheet2_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df3 = sheet3_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df4 = sheet4_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df5 = sheet5_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df6 = sheet6_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df7 = sheet7_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df8 = sheet8_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df9 = sheet9_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df10 = sheet10_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df11 = sheet11_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df12 = sheet12_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df13 = sheet13_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df14 = sheet14_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df15 = sheet15_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df16 = sheet16_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df17 = sheet17_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df18 = sheet18_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df19 = sheet19_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df20 = sheet20_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df21 = sheet21_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()
grouped_df22 = sheet22_df.groupby(['Financial Year', 'Financial Quarter', 'Force Name', 'Offence Group'])['Number of Offences'].sum().reset_index()


#Combine all dataframes into one
grouped_df_list = [grouped_df1, grouped_df2, grouped_df3, grouped_df4, grouped_df5,
                   grouped_df6, grouped_df7, grouped_df8, grouped_df9, grouped_df10,
                   grouped_df11, grouped_df12, grouped_df13, grouped_df14, grouped_df15,
                   grouped_df16, grouped_df17, grouped_df18, grouped_df19, grouped_df20,
                   grouped_df21, grouped_df22]

combined_df = pd.concat(grouped_df_list, ignore_index=True)

#Save copy as xlsx
file_path = '/Users/danielhill/Documents/Documents - Daniel’s MacBook Air/MSc Data Science/Dissertation/combined_df2.xlsx'  # Specify your desired file path and name
combined_df.to_excel(file_path, index=False)

