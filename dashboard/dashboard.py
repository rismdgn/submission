import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset
hour_df = pd.read_csv("dashboard/main_data.csv")
day_df = pd.read_csv("dashboard/main_data.csv")

st.title("Bike Sharing Data Analysis")

# Sidebar for interactivity
st.sidebar.header("Analysis Options")
analysis_option = st.sidebar.selectbox(
    "Select Analysis to Display",
    [
        "Trends Over Time",
        "Weather Impact on Rentals",
        "Bike Rentals by Time of Day"
    ]
)

# Preprocessing
weather_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}
hour_df['weather_category'] = hour_df['weathersit'].map(weather_mapping)
hour_df['datetime'] = pd.to_datetime(hour_df['dteday']) + pd.to_timedelta(hour_df['hr'], unit='h')
hour_df['mnth'] = hour_df['datetime'].dt.month
hour_df['weekday'] = hour_df['datetime'].dt.weekday
hour_df['hour'] = hour_df['datetime'].dt.hour

# Assign time of day
def assign_time_of_day(hr):
    if 5 <= hr <= 11:
        return 'Morning'
    elif 12 <= hr <= 17:
        return 'Afternoon'
    elif 18 <= hr <= 21:
        return 'Evening'
    else:
        return 'Night'

hour_df['time_of_day'] = hour_df['hr'].apply(assign_time_of_day)

# Handle selection and display the corresponding graph
if analysis_option == "Trends Over Time":
    st.write("## Trends Over Time")
    
    # Hourly trend
    hourly_trend = hour_df.groupby('hour')['cnt'].mean().reset_index()
    st.write("### Hourly Trends")
    fig_hour, ax_hour = plt.subplots()
    sns.lineplot(x='hour', y='cnt', data=hourly_trend, ax=ax_hour, marker='o', color='blue')
    ax_hour.set_title('Average Bike Rentals by Hour')
    ax_hour.set_xlabel('Hour of the Day')
    ax_hour.set_ylabel('Average Bike Rentals')
    ax_hour.grid(True)
    ax_hour.set_xticks(range(24))
    st.pyplot(fig_hour)

    # Weekly trend
    day_trend = hour_df.groupby('weekday')['cnt'].mean().reset_index()
    weekday_mapping = {
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    }
    day_trend['weekday'] = day_trend['weekday'].map(weekday_mapping)
    st.write("### Weekly Trends")
    fig_day, ax_day = plt.subplots()
    sns.barplot(x='weekday', y='cnt', data=day_trend, ax=ax_day, palette='viridis')
    ax_day.set_title('Average Bike Rentals by Day of the Week')
    ax_day.set_xlabel('Day of the Week')
    ax_day.set_ylabel('Average Bike Rentals')
    ax_day.set_xticklabels(ax_day.get_xticklabels(), rotation=30)
    st.pyplot(fig_day)

    # Monthly trend
    monthly_trend = hour_df.groupby('mnth')['cnt'].mean().reset_index()
    st.write("### Monthly Trends")
    fig_month, ax_month = plt.subplots()
    sns.lineplot(x='mnth', y='cnt', data=monthly_trend, ax=ax_month, marker='o', color='green')
    ax_month.set_title('Average Bike Rentals by Month')
    ax_month.set_xlabel('Month')
    ax_month.set_ylabel('Average Bike Rentals')
    ax_month.set_xticks(range(1, 13))
    ax_month.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax_month.grid(True)
    st.pyplot(fig_month)

elif analysis_option == "Weather Impact on Rentals":
    st.write("## Weather Impact on Rentals")
    
    # Average rentals by weather
    avg_rentals_by_weather = day_df.groupby('weathersit')['cnt'].mean()
    st.write("### Average Rentals by Weather Situation")
    fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
    avg_rentals_by_weather.plot(kind='bar', color=['green', 'orange', 'blue', 'red'], ax=ax_weather)
    ax_weather.set_title('Average Bike Rentals by Weather Situation')
    ax_weather.set_xlabel('Weather Situation')
    ax_weather.set_ylabel('Average Bike Rentals')
    ax_weather.set_xticklabels(['Clear', 'Mist', 'Rain', 'Snow'], rotation=45)
    ax_weather.grid(True)
    st.pyplot(fig_weather)

elif analysis_option == "Bike Rentals by Time of Day":
    st.write("## Bike Rentals by Time of Day")
    
    # Rentals by time of day
    time_group = hour_df.groupby('time_of_day')['cnt'].mean().reset_index()
    
    # Sort the time_of_day column to maintain the correct order (Morning, Afternoon, Evening, Night)
    time_group = time_group.sort_values(by='time_of_day', key=lambda x: x.map({'Morning': 1, 'Afternoon': 2, 'Evening': 3, 'Night': 4}))
    
    st.write("### Average Bike Rentals by Time of Day")
    
    # Create the barplot with customized style
    fig_time, ax_time = plt.subplots(figsize=(10, 6))
    
    # Plotting with Seaborn and making sure the colors match your style
    sns.barplot(x='time_of_day', y='cnt', data=time_group, ax=ax_time, palette='Blues_d')
    
    # Add title, labels, and grid as in your original code
    ax_time.set_title('Average Bike Rentals by Time of Day')
    ax_time.set_xlabel('Time of Day')
    ax_time.set_ylabel('Average Bike Rentals')
    
    # Customize gridlines (similar to your plot)
    ax_time.grid(True)
    
    # Display the plot in Streamlit
    st.pyplot(fig_time)
