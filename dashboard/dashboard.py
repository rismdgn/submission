import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset
hour_df = pd.read_csv("dashboard/main_data.csv")
day_df = pd.read_csv("dashboard/main_data.csv")

st.title("Bike Sharing Data Analysis")

# Sidebar for interactivity
st.sidebar.header("Pilihan Analisis")
analysis_option = st.sidebar.selectbox(
    "Pilih analisis yang ingin ditampilkan",
    [
        "Trends Over Time",
        "Dampak Cuaca pada Peminjaman Sepeda",
        "Waktu Peminjaman Sepeda"
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
    st.write("### Tren berdasarkan Jam")
    fig_hour, ax_hour = plt.subplots()
    sns.lineplot(x='hour', y='cnt', data=hourly_trend, ax=ax_hour, marker='o', color='blue')
    ax_hour.set_title('Rata rata peminjam sepeda berdasarkan jam')
    ax_hour.set_xlabel('Jam')
    ax_hour.set_ylabel('Rata rata jumlah peminjam sepeda')
    ax_hour.grid(True)
    ax_hour.set_xticks(range(24))
    st.pyplot(fig_hour)

    # Weekly trend
    day_trend = hour_df.groupby('weekday')['cnt'].mean().reset_index()
    weekday_mapping = {
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu',
        4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    }
    day_trend['weekday'] = day_trend['weekday'].map(weekday_mapping)
    st.write("### Tren berdasarkan Hari")
    fig_day, ax_day = plt.subplots()
    sns.barplot(x='weekday', y='cnt', data=day_trend, ax=ax_day, palette='viridis')
    ax_day.set_title('Rata rata peminjam sepeda berdasarkan hari')
    ax_day.set_xlabel('Hari')
    ax_day.set_ylabel('Rata rata jumlah peminjam sepeda')
    ax_day.set_xticklabels(ax_day.get_xticklabels(), rotation=30)
    st.pyplot(fig_day)

    # Monthly trend
    monthly_trend = hour_df.groupby('mnth')['cnt'].mean().reset_index()
    st.write("### Tren berdasarkan Bulan")
    fig_month, ax_month = plt.subplots()
    sns.lineplot(x='mnth', y='cnt', data=monthly_trend, ax=ax_month, marker='o', color='green')
    ax_month.set_title('Rata rata peminjam sepeda berdasarkan bulan')
    ax_month.set_xlabel('Bulan')
    ax_month.set_ylabel('Rata rata peminjam sepeda')
    ax_month.set_xticks(range(1, 13))
    ax_month.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des'])
    ax_month.grid(True)
    st.pyplot(fig_month)

elif analysis_option == "Dampak Cuaca pada Peminjaman Sepeda":
    st.write("## Dampak Cuaca pada Peminjaman Sepeda")
    
    # Average rentals by weather
    avg_rentals_by_weather = day_df.groupby('weathersit')['cnt'].mean()
    st.write("### Average Rentals by Weather Situation")
    fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
    avg_rentals_by_weather.plot(kind='bar', color=['green', 'orange', 'blue', 'red'], ax=ax_weather)
    ax_weather.set_title('Rata rata peminjam sepeda berdasarkan kondisi cuaca')
    ax_weather.set_xlabel('Kondisi Cuaca')
    ax_weather.set_ylabel('Rata rata jumlah peminjam sepeda')
    ax_weather.set_xticklabels(['Clear', 'Mist', 'Rain', 'Snow'], rotation=45)
    ax_weather.grid(True)
    st.pyplot(fig_weather)

elif analysis_option == "Waktu Peminjaman Sepeda":
    st.write("## Waktu Peminjaman Sepeda")
    time_group = hour_df.groupby('time_of_day')['cnt'].mean().reset_index()

    # Sort hasil
    time_group = time_group.sort_values(by='time_of_day', key=lambda x: x.map({'Morning': 1, 'Afternoon': 2, 'Evening': 3}))
    
    st.write("### Persebaran waktu peminjaman sepeda")
    
    # Create the barplot with customized style
    fig_time, ax_time = plt.subplots(figsize=(10, 6))
    
    # Plotting with Seaborn and making sure the colors match your style
    sns.barplot(x='time_of_day', y='cnt', data=time_group, ax=ax_time, palette='Blues_d')
    
    # Add title, labels, and grid as in your original code
    ax_time.set_title('Rata rata jumlah peminjam sepeda berdasarkan waktu')
    ax_time.set_xlabel('Waktu')
    ax_time.set_ylabel('Rata rata jumlah peminjam sepeda')
    
    # Customize gridlines (similar to your plot)
    ax_time.grid(True)
    
    # Display the plot in Streamlit
    st.pyplot(fig_time)
