import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 
from PIL import Image
import os
import gdown
import gcsfs

st.set_page_config(page_title='New York Citibike Dashboard', layout='wide')

# Sidebar for page navigation
page = st.sidebar.selectbox(
    'Select a Page',
    ["Introduction", "Popular Bike Stations", "Daily Rides & Temperature", "Aggregated Map", "Conclusion & Recommendations"]
)

####################### Import data #########################################
url = 'https://storage.googleapis.com/my-dataset-bucket-analysis/cleaned_citibike_weather_final.csv'
df = pd.read_csv(url)

df['date'] = pd.to_datetime(df['date'])


############################# DEFINE THE PAGES ############################

# Introduction Page
if page == "Introduction":
    st.title("New York Citibike Data Dashboard")
    myImage = Image.open("images/istockphoto-504748828-612x612.jpg")
    st.image(myImage, caption="New York Citi Bikes", use_column_width=True)
    st.markdown("This dashboard provides insights on bike rides and temperature trends in New York City during 2022.")
    st.markdown("""
        **Pages:**
        - **Popular Bike Stations**: Displays the top 20 most popular bike stations.
        - **Daily Rides & Temperature**: Shows a line chart comparing daily bike rides and average temperatures.
        - **Aggregated Map**: Displays an interactive map of bike trips in New York City.
    """)
    


############################# DEFINE THE CHARTS ############################

## Bar chart 

# Popular Bike Stations Page
elif page == "Popular Bike Stations":
    st.title("Most Popular Bike Stations")

    # Create a bar chart for the top 20 most popular stations
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

    # Interpretation of the chart
    st.markdown("""
        The bar chart highlights the top 20 bike stations with the highest number of trips. These stations are highly frequented, suggesting that they are central locations with high demand for bike services. Optimizing bike supply at these stations could help reduce shortages.
    """)

elif page == "Daily Rides & Temperature":
    st.title("Daily Bike Rides and Temperature Trends")
    
    # Load the cleaned dataset
    file_path = 'cleaned_citibike_daily_rides.csv'
    df_cleaned = pd.read_csv(file_path)
    df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
   
   
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2.add_trace(
        go.Scatter(x=df_cleaned['date'], y=df_cleaned['bike_rides_daily'], name='Daily Bike Rides', 
                   marker={'color': 'blue'}),
        secondary_y=False
    )
    fig_2.add_trace(
        go.Scatter(x=df_cleaned['date'], y=df_cleaned['avgTemp'], name='Average Temperature', 
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
    
    # Interpretation of the chart
    st.markdown("""
        This chart shows the relationship between daily bike rides and the average temperature. 
        We can observe that bike usage increases during warmer months and decreases significantly 
        during colder months. This suggests a strong correlation between weather and bike ride patterns.
    """)


        
### Add the map  ###

# Aggregated Map Page

elif page == "Aggregated Map":
    st.title("Aggregated Bike Trips in New York")

    path_to_html = "NY_Bike_Trips_Customized.html"

    # Read file and keep in variable
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    # Show the map on the web page
    st.components.v1.html(html_data, height=1000)

    # Interpretation of the map
    st.markdown("""
        The map visualizes the flow of bike trips throughout New York City. Areas with a high density of trips can be 
        identified, which provides insight into regions with higher demand for bike services. This data can be used to 
        allocate bike supply more effectively.
    """)
    
elif page == "Conclusion & Recommendations":
    st.title("Conclusion & Recommendations")

    # Detailed conclusion and recommendations
    st.markdown("""
        **Conclusion**:
        
        The Citibike data analysis for New York City in 2022 reveals several critical insights. The usage patterns of Citibike are significantly influenced by seasonal changes. During warmer months, bike usage increases notably, with peak demand occurring from May to October. Conversely, during colder months, from November through March, the number of daily bike rides drops sharply. This pattern highlights the strong correlation between weather conditions and bike usage.

        Additionally, certain stations exhibit consistently high demand, particularly in areas that serve as transportation hubs or popular tourist destinations. These high-traffic stations face frequent bike shortages, especially during peak hours. This suggests that better allocation strategies could help optimize bike availability at key locations, ensuring riders have access to bikes when they need them most.
        
        **Recommendations**:
        
        1. **Seasonal Bike Redistribution**: Adjust the distribution of bikes across the city based on seasonal demand patterns. More bikes should be placed in high-traffic areas during the warmer months, while bike availability can be reduced during the winter to optimize resources.
        
        2. **Increase Docking Capacity at High-Demand Stations**: As certain stations see consistently high bike traffic, the city should consider increasing docking capacities at these key locations. This will help alleviate the current strain on resources and reduce the frequency of empty or full stations.
        
        3. **Real-Time Usage Monitoring**: Implement a dynamic monitoring system that uses real-time data to adjust bike availability and optimize the system in response to fluctuations in rider demand. This approach could involve predictive models that account for daily weather forecasts, holidays, and city events.
        
        4. **Winter Promotions to Boost Usage**: To maintain consistent bike usage throughout the year, Citibike should introduce targeted promotions during the winter months. Discounted memberships, loyalty rewards, or ride credits could help incentivize riders to continue using Citibike despite the cold weather.
        
        5. **Enhanced City Planning Based on Data**: The insights from this analysis should inform broader city planning efforts, particularly in enhancing bike infrastructure, such as expanding bike lanes in high-traffic areas and ensuring safe routes are available for riders during all seasons.

        By adopting these recommendations, Citibike can enhance its service offering, improve rider satisfaction, and contribute to a more sustainable, bike-friendly city.
    """)

    

