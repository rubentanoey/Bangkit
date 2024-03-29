# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kfdphxlFYE0mvvTC48jPNwMzjx4Tiq__

# Proyek Analisis Data: Bike Sharing Dataset
- **Nama:** Ruben Tanoey
- **Email:** M010D4KY2276@bangkit.academy
- **ID Dicoding:** rubentanoey

## Menentukan Pertanyaan Bisnis

- If we want to give the best experience for the customers, the bike requires maintenance within a specific timeframe. Is there any specific time during the 24-hour period when bicycle sharing is least utilized?
- We need to schedule an event for the bike-sharing system. We can create an event that gives Users excitement like criterium race. During which week is bike-sharing usage decrease at its lowest point, so that we can plan the event accordingly?
[Why searching lowest point? Because usually the highest point is where people will use the bike for their own business. If the event is in the reasonably low point, there could be a chance the bike can be used for marketing!]

## Import Semua Packages/Library yang Digunakan
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

"""## Data Wrangling

### Gathering Data

Get both the data files (csv format)
"""

df_day = pd.read_csv("submission/dashboard/day.csv")
df_hour = pd.read_csv("submission/dashboard/hour.csv")

"""### Assessing Data

The first thing I'd like to check is the missing values in the dataset.
"""

print("Number of missing values in df_day\n", df_day.isnull().sum(), "\n")
print("Number of missing values in df_hour\n", df_hour.isnull().sum())

"""Then, I'd like to check the numeric descriptions of the dataset."""

df_day.describe()

df_hour.describe()

"""### Cleaning Data"""

import pandas as pd

def detect_outliers(dataframe, threshold=1.5):
    cols = list(dataframe)
    outliers_list = []

    for column in cols:
        if column in dataframe.select_dtypes(include='number').columns:
            q1 = dataframe[column].quantile(0.25)
            q3 = dataframe[column].quantile(0.75)
            iqr = q3 - q1
            fence_low = q1 - threshold * iqr
            fence_high = q3 + threshold * iqr
            num_outliers = dataframe.loc[(dataframe[column] < fence_low) | (dataframe[column] > fence_high)].shape[0]
            outliers_list.append({'Feature': column, 'Number of Outliers': num_outliers})

    outliers = pd.DataFrame(outliers_list)
    return outliers

result_day = detect_outliers(df_day)
result_day

result_hour = detect_outliers(df_hour)
result_hour

"""We know that holiday, weathersit, humidity are in a normal range based on the description of the dataset as we get earlier. But how about the windspeed, casual, and registered? We need to check the validity of the data."""

df_hour_group = df_hour.groupby('dteday')['windspeed'].mean().reset_index()
df_hour_group

"""Check the windspeed in the day dataset is the same as the windspeed in the hour grouped dataset with precision 0.xxx"""

df_day['windspeed'].round(3).equals(df_hour_group['windspeed'].round(3))

"""By this point, we can assume that the big number of windspeed is valid and could be a weather anomaly. We can make keep the data as is.

Check if sum of casual and registered is equal to cnt.
"""

df_day['casual_registered_sum'] = df_day['casual'] + df_day['registered']
print(df_day['casual_registered_sum'].equals(df_day['cnt']))

df_hour['casual_registered_sum'] = df_hour['casual'] + df_hour['registered']
print(df_hour['casual_registered_sum'].equals(df_hour['cnt']))

"""All the data is true! Then I can give an argument that the data is already clean and valid without removing outliers. Let's analyze the data through EDA.

## Exploratory Data Analysis (EDA)

### Explore the specific time during the 24-hour period when bicycle sharing is least utilized

Group the hour dataset by hour and get the average count of bikes rented
"""

df_hour_group = df_hour.groupby('hr')['cnt'].mean().reset_index()
df_hour_group

"""Group the day dataset into weekly and get the increase of bike-sharing usage. Then search for the highest decrease."""

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['week'] = df_day['dteday'].dt.isocalendar().week
df_day_group = df_day.groupby('week')['cnt'].sum().reset_index()
df_day_group['increase'] = df_day_group['cnt'].diff()

df_day_group

"""Get 3 highest peaks of bike-sharing usage"""

df_day_group.nsmallest(3, 'increase')

"""## Visualization & Explanatory Analysis

### Pertanyaan 1: The bike requires maintenance within a specific timeframe. Is there any specific time during the 24-hour period when bicycle sharing is least utilized?

> Yes, there is. Based on the teal bar data, the bicycle usage is starting to increase at 6 AM and reach its peak at 5 PM. The bicycle usage is starting to decrease after 5 PM. If the bike requires maintenance, the best time to do it is between 11 PM to 5 AM.
"""

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df_hour_group['hr'], df_hour_group['cnt'], color='teal')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Average Bike Rentals')
ax.set_title('Average Bike Rentals by Hour of the Day')
ax.set_xticks(df_hour_group['hr'])
plt.xticks(rotation=45) 

st.pyplot(fig)

"""### Pertanyaan 2: We need to schedule an event for the bike-sharing system. During which week is bike-sharing usage decrease at its lowest point, so that we can plan the event accordingly?

> There are 3 lowest point of bike-sharing usage decreases, marked by the teal colored line. The first point is on the 47th week, the second point is on the 44th week, and the third point is on the 52nd week.
There also a line graph for bike-sharing usage weekly, the trends are increasing from the 1st week to the 47th week and then decreasing from the 47th week to the 52nd week.
"""

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_day_group['week'], df_day_group['cnt'], marker='o', label='Total Bike Rentals', color='orange')
ax.plot(df_day_group['week'], df_day_group['increase'], marker='o', label='Weekly Increase', color='teal')
ax.set_xlabel('Week')
ax.set_ylabel('Count')
ax.set_title('Bike Rentals and Weekly Increase Over Weeks')
ax.legend()
ax.grid(True)

st.pyplot(fig)

"""## Conclusion

> - For the first question, the best time to do maintenance is between 11 PM to 5 AM. It is the time when the bicycle sharing is getting least utilized. The maintainance will keep the bicycle clean and comfortable to use, affecting the user's satisfaction.
> - For the second question, the best time to schedule an event, such as criterium race, is on the 44th week, first because it is the one of the lowest point of increase of bike-sharing usage, and second because it is still in a reasonable weather (not winter - that also makes the usage lower low).
"""