import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

st.set_page_config(page_title='New York Citibike Dashboard', layout='wide')

st.title("New York Citibike Data Dashboard")

st.markdown("This dashboard provides insights on bike rides and temperature trends in New York City during 2022.")

####################### Import data #########################################
df = pd.read_csv('cleaned_citibike_weather_final.csv')

df['date'] = pd.to_datetime(df['date'])

############################# DEFINE THE CHARTS ############################

## Bar chart 

df['value'] = 1
df_groupby_bar = df.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
top20 = df_groupby_bar.nlargest(20, 'value')

fig = go.Figure(go.Bar(
    x=top20['start_station_name'], 
    y=top20['value'], 
    marker={'color': top20['value'], 'colorscale': 'Blues'}
))

fig.update_layout(
    title='Top 20 Most Popular Bike Stations in New York',
    xaxis_title='Start Stations', 
    yaxis_title='Sum of Trips', 
    width=900, 
    height=600
)

st.plotly_chart(fig, use_container_width=True)

## line chart 

df_grouped = df.groupby('date').agg(
    bike_rides_daily=('ride_id', 'count'),
    avgTemp=('AvgTemp(C)', 'mean')
).reset_index()

df_grouped = df_grouped[df_grouped['date'] >= pd.to_datetime('2022-01-01')]

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
fig_2.add_trace(
    go.Scatter(x=df_grouped['date'], y=df_grouped['bike_rides_daily'], name='Daily Bike Rides', 
               marker={'color': 'blue'}),
    secondary_y=False
)
fig_2.add_trace(
    go.Scatter(x=df_grouped['date'], y=df_grouped['avgTemp'], name='Average Temperature', 
               marker={'color': 'red'}),
    secondary_y=True
)
fig_2.update_layout(
    title="Daily Bike Rides and Average Temperature (2022)",
    xaxis_title="Date",
    yaxis_title="Bike Rides",
    yaxis2_title="Average Temperature (C)",
    height=800
)
st.plotly_chart(fig_2, use_container_width=True)

### Add the map  ###

path_to_html = "NY_Bike_Trips_Customized.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()
    
# Show the map on the web page
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data, height=1000)
