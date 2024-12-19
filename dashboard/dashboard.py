import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset
hour_df = pd.read_csv("dashboard/main_data.csv")
day_df = pd.read_csv("dashboard/main_data.csv")

st.title("Bike Sharing Data Analysis")

# Sidebar untuk filter interaktif
st.sidebar.header("Filters")

# Filter berdasarkan tanggal
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(hour_df['dteday']).min().date())
end_date = st.sidebar.date_input("End Date", pd.to_datetime(hour_df['dteday']).max().date())

# Mapping weather condition
weather_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}
hour_df['weather_category'] = hour_df['weathersit'].map(weather_mapping)
day_df['weather_category'] = day_df['weathersit'].map(weather_mapping)

# Convert date and hour columns for easier handling
hour_df['datetime'] = pd.to_datetime(hour_df['dteday']) + pd.to_timedelta(hour_df['hr'], unit='h')
hour_df['month'] = hour_df['datetime'].dt.month
hour_df['weekday'] = hour_df['datetime'].dt.weekday
hour_df['hour'] = hour_df['datetime'].dt.hour


# Pertanyaan 1: Tren Penggunaan Sepeda Berdasarkan Waktu
st.write("## 1. Tren Penggunaan Sepeda Berdasarkan Waktu")

# Agregasi per jam
hourly_trend = hour_df.groupby('hour')['cnt'].mean().reset_index()

# Visualisasi tren per jam
st.write("### Tren Per Jam")
fig_hour, ax_hour = plt.subplots()
sns.lineplot(x='hour', y='cnt', data=hourly_trend, ax=ax_hour, marker='o', color='blue')
ax_hour.set_title('Average Bike Rentals by Hour')
ax_hour.set_xlabel('Hour of the Day')
ax_hour.set_ylabel('Average Bike Rentals')
ax_hour.grid(True)
ax_hour.set_xticks(range(24))  # Menampilkan 24 jam
st.pyplot(fig_hour)

# Agregasi per hari dalam seminggu
day_trend = hour_df.groupby('weekday')['cnt'].mean().reset_index()
weekday_mapping = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
    4: 'Thursday', 5: 'Friday', 6: 'Saturday'
}
day_trend['weekday'] = day_trend['weekday'].map(weekday_mapping)

# Visualisasi tren per hari
st.write("### Tren Harian")
fig_day, ax_day = plt.subplots()
sns.barplot(x='weekday', y='cnt', data=day_trend, ax=ax_day, palette='viridis')
ax_day.set_title('Average Bike Rentals by Day of the Week')
ax_day.set_xlabel('Day of the Week')
ax_day.set_ylabel('Average Bike Rentals')
ax_day.set_xticklabels(ax_day.get_xticklabels(), rotation=30)
st.pyplot(fig_day)

# Pilih jenis visualisasi
chart_type = st.radio(
    "Select Chart Type for Hourly Trend",
    options=["Line Chart", "Bar Chart"]
)

if chart_type == "Line Chart":
    sns.lineplot(x='hr', y='cnt', data=hourly_trend, ax=ax_hour, marker='o', color='blue')
elif chart_type == "Bar Chart":
    sns.barplot(x='hr', y='cnt', data=hourly_trend, ax=ax_hour, palette='Blues_d')
    
# Agregasi per bulan
monthly_trend = hour_df.groupby('month')['cnt'].mean().reset_index()

# Visualisasi tren bulanan
st.write("### Tren Bulanan")
fig_month, ax_month = plt.subplots()
sns.lineplot(x='month', y='cnt', data=monthly_trend, ax=ax_month, marker='o', color='green')
ax_month.set_title('Average Bike Rentals by Month')
ax_month.set_xlabel('Month')
ax_month.set_ylabel('Average Bike Rentals')
ax_month.set_xticks(range(1, 13))
ax_month.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax_month.grid(True)
st.pyplot(fig_month)

# Pertanyaan 2: Pengaruh Cuaca
st.write("## 2. Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

# Agregasi rata-rata penyewaan berdasarkan cuaca
avg_rentals_by_weather = day_df.groupby('weathersit')['cnt'].mean()

# Visualisasi pengaruh cuaca
st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
avg_rentals_by_weather.plot(kind='bar', color=['green', 'orange', 'blue', 'red'], ax=ax_weather)
ax_weather.set_title('Average Bike Rentals by Weather Situation')
ax_weather.set_xlabel('Weather Situation')
ax_weather.set_ylabel('Average Bike Rentals')
ax_weather.set_xticklabels(['Clear', 'Mist', 'Rain', 'Snow'], rotation=45)
ax_weather.grid(True)
st.pyplot(fig_weather)


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

# Agregasi data berdasarkan 'time_of_day'
time_group = hour_df.groupby('time_of_day')['cnt'].mean().reset_index()

# Sort hasil berdasarkan urutan waktu yang benar
time_group = time_group.sort_values(by='time_of_day', key=lambda x: x.map({'Morning': 1, 'Afternoon': 2, 'Evening': 3, 'Night': 4}))

# Tampilkan hasil agregasi di Streamlit
st.write("### Average Bike Rentals by Time of Day:")

# Visualisasi menggunakan seaborn
fig_time, ax_time = plt.subplots(figsize=(10, 6))

# Membuat bar plot dengan palet warna
sns.barplot(x='time_of_day', y='cnt', data=time_group, ax=ax_time, palette='Blues_d')

# Mengatur judul dan label
ax_time.set_title('Average Bike Rentals by Time of Day')
ax_time.set_xlabel('Time of Day')
ax_time.set_ylabel('Average Bike Rentals')

# Menambahkan grid dan menyesuaikan label
ax_time.grid(True)

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig_time)
