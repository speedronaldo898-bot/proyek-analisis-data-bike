import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema visual seaborn
sns.set_theme(style='darkgrid')

# Menyiapkan fungsi pembantu
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby('mnth')['cnt'].sum().reset_index()
    return monthly_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby('weathersit')['cnt'].mean().reset_index().sort_values(by='cnt', ascending=False)
    return weather_rent_df

# Load data yang sudah bersih
# File ini harus berada di folder yang sama dengan dashboard.py
all_df = pd.read_csv("dashboard/main_data.csv")

# Memastikan kolom tanggal bertipe datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Filter Data Berdasarkan Tahun
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # 1. Gunakan try-except untuk menangkap error saat pengguna baru memilih 1 tanggal
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        # 2. Jika error terjadi (pengguna baru pilih 1 tanggal), tampilkan peringatan
        st.error("Silakan pilih rentang tanggal yang lengkap (Tanggal Awal dan Tanggal Akhir).")
        # 3. Hentikan eksekusi kode di bawahnya agar aplikasi tidak crash
        st.stop()

# 4. Jika berhasil melewati try-except (2 tanggal terpilih), lanjutkan filter data
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Menyiapkan dataframe
monthly_rent_df = create_monthly_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Header Dashboard
st.header('Bike Sharing Dashboard 🚲')

# Menampilkan metrik utama
st.subheader('Total Penyewaan Sepeda')
total_rent = main_df['cnt'].sum()
st.metric("Total Penyewaan", value=total_rent)

# Visualisasi 1: Tren Bulanan
st.subheader('Tren Penyewaan Sepeda per Bulan')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='mnth', y='cnt', data=monthly_rent_df, marker='o', linewidth=2, color="#72BCD4", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.set_xticks(range(1, 13))
st.pyplot(fig)

# Visualisasi 2: Berdasarkan Cuaca
st.subheader('Rata-rata Penyewaan Berdasarkan Cuaca')
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
sns.barplot(x='cnt', y='weathersit', data=weather_rent_df, palette=colors, ax=ax)
ax.set_xlabel("Rata-rata Penyewaan")
ax.set_ylabel("Kondisi Cuaca")
st.pyplot(fig)