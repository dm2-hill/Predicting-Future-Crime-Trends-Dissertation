#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:07:58 2024

@author: danielhill
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


#Load the data
df = pd.read_excel('combined_df FINAL 2023 Q4 added.xlsx')

#Convert Financial Year to datetime
df['Financial Year'] = pd.to_datetime(df['Financial Year'].str[:4], format='%Y')

#Make sure offence group names match for all years
df['Offence Group'] = df['Offence Group'].replace('Miscellaneous crimes against society', 
                                                 'Miscellaneous crimes')

df['Offence Group'] = df['Offence Group'].replace('Theft Offences', 'Theft offences')

#Remove 2023 and 'Fraud offences' as these are incomplete data
df = df[(df['Financial Year'].dt.year != 2023) & (df['Offence Group'] != 'Fraud offences')]

#Group the data by Financial Year and Offence Group, summing the Number of Offences
grouped_data = df.groupby(['Financial Year', 'Offence Group'])['Number of Offences'].sum().unstack()

#Create overall line chart for UK
plt.figure(figsize=(12, 6))
for column in grouped_data.columns:
    plt.plot(grouped_data.index, grouped_data[column], label=column)

#Format y-axis to show values in millions
def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'

plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

plt.title('Crime Trends Over Time by Offence Group')
plt.xlabel('Year')
plt.ylabel('Number of Offences (Millions)')
plt.legend(title='Offence Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.show()


#Create stacked area chart
fig, ax = plt.subplots(figsize=(12, 6))
grouped_data.plot.area(ax=ax, stacked=True)

plt.title('Composition of Total Crime Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Offences (Millions)')
plt.legend(title='Offence Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'

ax.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

plt.show()


#Percentage stacked bar chart
fig, ax = plt.subplots(figsize=(12, 6))
grouped_data_percent = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
grouped_data_percent.plot.area(ax=ax, stacked=True)

plt.title('Composition of Total Crime Over Time')
plt.xlabel('Year')
plt.ylabel('Percentage of Total Crime')
plt.legend(title='Offence Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.show()


#Create interactive plot using plotly
import plotly.graph_objects as go

fig = go.Figure()
for column in grouped_data.columns:
    fig.add_trace(go.Scatter(
        x=grouped_data.index, 
        y=grouped_data[column],
        mode='lines',
        stackgroup='one',
        name=column,
        hovertemplate='%{y:,.0f}<extra></extra>'  #Only show the y-value
    ))

fig.update_layout(
    title='Composition of Total Crime Over Time',
    xaxis_title='Year',
    yaxis_title='Number of Offences',
    legend_title='Offence Group',
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
    ),
)

#Add a hover template for the x-axis (year)
fig.update_traces(
    xaxis='x',
    hovertemplate='%{y:,.0f}',  #Format for individual traces
)
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
    ),
    hovermode='x unified',
)

#Customise hover template
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
    ),
    hovermode='x unified',
    xaxis=dict(
        hoverformat='%Y'  #Format the year in the hover text
    )
)

fig.show()
fig.write_html("crime_composition_plot.html")


#Create heatmaps
import seaborn as sns

#Group the data by year, quarter and offence group
grouped_data = df.groupby(['Financial Year', 'Financial Quarter', 'Offence Group'])['Number of Offences'].sum().unstack(level='Offence Group')

#Create a heatmap for each offence group
offence_groups = grouped_data.columns

for offence in offence_groups:
    plt.figure(figsize=(12, 8))
    
    #Reshape data for this specific offense
    offence_data = grouped_data[offence].unstack(level='Financial Quarter')
    
    #Create the heatmap
    ax = sns.heatmap(offence_data, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Number of Offences'})
    
    plt.title(f'Heatmap of {offence} Across Quarters and Years')
    plt.xlabel('Financial Quarter')
    plt.ylabel('Financial Year')
    
    #Modify y-axis ticks to show only years
    ax.set_yticklabels(offence_data.index.get_level_values('Financial Year'))
    
    plt.tight_layout()
    plt.show()

#Create an overall heatmap (sum of all offenses)
overall_data = grouped_data.sum(axis=1).unstack(level='Financial Quarter')

plt.figure(figsize=(12, 8))
ax = sns.heatmap(overall_data, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Total Number of Offences'})

plt.title('Heatmap of Total Offences Across Quarters and Years')
plt.xlabel('Financial Quarter')
plt.ylabel('Financial Year')

#Modify y-axis ticks to show only years
ax.set_yticklabels(overall_data.index.get_level_values('Financial Year'))

plt.tight_layout()
plt.show()


#Create Bar Charts for total crime, 2002 and 2022 comparison
latest_year = df['Financial Year'].max()
df_latest = df[df['Financial Year'] == latest_year]

first_year = df['Financial Year'].min()
df_first = df[df['Financial Year'] == first_year]

#Remove "London, City of" and calculate total crime rate
df_latest = df_latest[df_latest['Force Name'] != 'London, City of']
df_first = df_first[df_first['Force Name'] != 'London, City of']
crime_rates = df_latest.groupby('Force Name')['Offences per 1000 population'].sum().sort_values(ascending=False)
crime_rates2 = df_first.groupby('Force Name')['Offences per 1000 population'].sum().sort_values(ascending=False)

#Create the bar chart for 2022
plt.figure(figsize=(15, 10))
sns.barplot(x=crime_rates.index, y=crime_rates.values)

plt.title(f'Total Crime Rate per 1000 Population by Force Area ({latest_year})')
plt.xlabel('Force Area')
plt.ylabel('Crimes per 1000 Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Create the bar chart 2002
plt.figure(figsize=(15, 10))
sns.barplot(x=crime_rates2.index, y=crime_rates2.values)

plt.title(f'Total Crime Rate per 1000 Population by Force Area ({first_year})')
plt.xlabel('Force Area')
plt.ylabel('Crimes per 1000 Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Create a bar chart for a specific crime type
crime_type = 'Theft Offences'  # Change this to the crime type you're interested in
crime_type_rates = df_latest[df_latest['Offence Group'] == crime_type].groupby('Force Name')['Offences per 1000 population'].sum().sort_values(ascending=False)

plt.figure(figsize=(15, 10))
sns.barplot(x=crime_type_rates.index, y=crime_type_rates.values)

plt.title(f'{crime_type} Rate per 1000 Population by Force Area ({latest_year})')
plt.xlabel('Force Area')
plt.ylabel(f'{crime_type} per 1000 Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Create stacked bar chart for specific crime types
crime_types = ['Theft offences', 'Violence against the person', 'Criminal damage and arson']
crime_data = df_latest[df_latest['Offence Group'].isin(crime_types)]

#Create a pivot table to calculate crime rates by force area and crime type
crime_rates = crime_data.pivot_table(
    values='Offences per 1000 population', 
    index='Force Name', 
    columns='Offence Group', 
    aggfunc='sum'
)

#Calculate the total crime rate for each force area
crime_rates['Total Crime Rate'] = crime_rates.sum(axis=1)

#Sort the data by total crime rate
crime_rates = crime_rates.sort_values(by='Total Crime Rate', ascending=False)

#Drop the 'Total Crime Rate' column as it's not needed for plotting
crime_rates = crime_rates.drop(columns='Total Crime Rate')

#Set font size for various chart elements
font_size = 14
title_font_size = 18

#Plot the stacked bar chart
ax = crime_rates.plot(kind='bar', stacked=True, figsize=(15, 10), fontsize=font_size)

#Customise title, labels, and legend font size
plt.title(f'Crime Rates per 1000 Population by Force Area and Crime Type ({latest_year})', fontsize=title_font_size)
plt.xlabel('Force Area', fontsize=font_size)
plt.ylabel('Crimes per 1000 Population', fontsize=font_size)

#Place the legend inside the top right corner of the chart
plt.legend(title='Crime Type', loc='upper right', bbox_to_anchor=(0.95, 0.95), fontsize=font_size, title_fontsize=font_size)

#Customize the tick label font size
plt.xticks(rotation=90, fontsize=font_size)
plt.yticks(fontsize=font_size)

plt.tight_layout()
plt.show()


#Scatter plots to show trends in population and crime 
force_data = df_latest.groupby('Force Name').agg({
    'Population': 'first',  # Assuming population is the same for each force across offense types
    'Offences per 1000 population': 'sum'
}).reset_index()

#Create the scatter plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=force_data, x='Population', y='Offences per 1000 population', hue='Force Name')

plt.title(f'Relationship between Population Size and Crime Rate ({latest_year})')
plt.xlabel('Population')
plt.ylabel('Total Crimes per 1000 Population')
plt.legend(title='Force Name', bbox_to_anchor=(1.05, 1), loc='upper left')

#Add trend line
sns.regplot(data=force_data, x='Population', y='Offences per 1000 population', 
            scatter=False, color='red', line_kws={'linestyle': '--'})

plt.tight_layout()
plt.show()

#Create scatter plots for specific crime types
crime_types = ['Theft offences', 'Violence against the person', 'Criminal damage and arson']

for crime_type in crime_types:
    crime_data = df_latest[df_latest['Offence Group'] == crime_type].groupby('Force Name').agg({
        'Population': 'first',
        'Offences per 1000 population': 'sum'
    }).reset_index()
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=crime_data, x='Population', y='Offences per 1000 population', hue='Force Name')
    
    plt.title(f'Relationship between Population Size and {crime_type} Rate ({latest_year})')
    plt.xlabel('Population')
    plt.ylabel(f'{crime_type} per 1000 Population')
    plt.legend(title='Force Name', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add a trend line
    sns.regplot(data=crime_data, x='Population', y='Offences per 1000 population', 
                scatter=False, color='red', line_kws={'linestyle': '--'})
    
    plt.tight_layout()
    plt.show()

#Log-transformed scatter plot for better visualization
plt.figure(figsize=(12, 8))
sns.scatterplot(data=force_data, x='Population', y='Offences per 1000 population', hue='Force Name')

plt.title(f'Relationship between Population Size and Crime Rate ({latest_year}) - Log Scale')
plt.xlabel('Population (Log Scale)')
plt.ylabel('Total Crimes per 1000 Population (Log Scale)')
plt.legend(title='Force Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xscale('log')
plt.yscale('log')

#Add trend line
sns.regplot(data=force_data, x='Population', y='Offences per 1000 population', 
            scatter=False, color='red', line_kws={'linestyle': '--'})

plt.tight_layout()
plt.show()

#Multiple crime types on one graph
plt.figure(figsize=(12, 8))
for crime_type in crime_types:
    crime_data = df_latest[df_latest['Offence Group'] == crime_type].groupby('Force Name').agg({
        'Population': 'first',
        'Offences per 1000 population': 'sum'
    }).reset_index()
    plt.scatter(crime_data['Population'], crime_data['Offences per 1000 population'], label=crime_type)

plt.xlabel('Population')
plt.ylabel('Crimes per 1000 Population')
plt.legend()
plt.title(f'Relationship between Population Size and Crime Rates by Type ({latest_year})')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.show()


#Produce table of summary statistics
summary = df.describe(include = None)
html_table = summary.to_html(classes='table table-striped', justify='center')
with open('summary_table3.html', 'w') as f:
    f.write(html_table)
    
#Filter for theft offences, excluding 'London, City of'
theft_df = df[(df['Offence Group'] == 'Theft offences') & 
              (df['Force Name'] != 'London, City of')]

#Filter for violence against the person, excluding 'London, City of'
violence_df = df[(df['Offence Group'] == 'Violence against the person') & 
                 (df['Force Name'] != 'London, City of')]

#Generate summary statistics for theft offences
theft_summary = theft_df['Offences per 1000 population'].describe()

#Generate summary statistics for violence against the person
violence_summary = violence_df['Offences per 1000 population'].describe()

#Print the summary tables
print("Theft Offences Summary:")
print(theft_summary)
print("\nViolence Against the Person Summary:")
print(violence_summary)

# Function to get min and max info
def get_min_max_info(data):
    min_row = data.loc[data['Offences per 1000 population'].idxmin()]
    max_row = data.loc[data['Offences per 1000 population'].idxmax()]
    
    return pd.DataFrame({
        'Statistic': ['Min', 'Max'],
        'Number of Offences': [min_row['Offences per 1000 population'], max_row['Offences per 1000 population']],
        'Financial Year': [min_row['Financial Year'], max_row['Financial Year']],
        'Financial Quarter': [min_row['Financial Quarter'], max_row['Financial Quarter']],
        'Force Name': [min_row['Force Name'], max_row['Force Name']]
    })

# Filter for theft offences, excluding 'London, City of'
theft_df = df[(df['Offence Group'] == 'Theft offences') & 
              (df['Force Name'] != 'London, City of')]

# Filter for violence against the person, excluding 'London, City of'
violence_df = df[(df['Offence Group'] == 'Violence against the person') & 
                 (df['Force Name'] != 'London, City of')]

# Get min/max info for theft offences
theft_summary = get_min_max_info(theft_df)

# Get min/max info for violence against the person
violence_summary = get_min_max_info(violence_df)

# Print the summary tables
print("Theft Offences Summary (excluding London, City of):")
print(theft_summary.to_string(index=False))
print("\nViolence Against the Person Summary (excluding London, City of):")
print(violence_summary.to_string(index=False))
