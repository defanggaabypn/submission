import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya visualisasi seaborn
sns.set(style='dark')

# --- 1. Load Data ---
@st.cache_data
def load_data():
    # PERBAIKAN PATH: Menggunakan 'main_data.csv' langsung
    # Asumsi: script dijalankan dari dalam folder 'dashboard/'
    df = pd.read_csv("main_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# --- 2. Sidebar Filter ---
st.sidebar.header("Filter Data")
min_date = df['date'].min()
max_date = df['date'].max()

# Input Rentang Waktu
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Input Pilihan Stasiun
selected_station = st.sidebar.multiselect(
    label="Pilih Stasiun",
    options=df['station'].unique(),
    default=df['station'].unique() # Default terpilih semua
)

# Filter data utama berdasarkan input user
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) & 
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['station'].isin(selected_station))
]

# --- 3. Main Dashboard ---
st.title('Air Quality Analysis Dashboard ☁️')
st.markdown("Dashboard ini menampilkan analisis kualitas udara berdasarkan data PM2.5 historis.")

# Tampilkan Metrics Sederhana
col1, col2, col3 = st.columns(3)
with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f}")
with col2:
    max_pm25 = filtered_df['PM2.5'].max()
    st.metric("Max PM2.5", value=f"{max_pm25:.2f}")
with col3:
    min_pm25 = filtered_df['PM2.5'].min()
    st.metric("Min PM2.5", value=f"{min_pm25:.2f}")

st.markdown("---")

# --- Visualisasi 1: Tren Bulanan (Menjawab Pertanyaan 1) ---
st.subheader('1. Tren Rata-rata Bulanan PM2.5 (Analisis Musiman)')
st.markdown("*Grafik ini menampilkan pola kenaikan/penurunan polusi per bulan.*")

# Resample data ke bulanan agar grafik lebih bersih dan pola terlihat
monthly_df = filtered_df.resample(rule='M', on='date').agg({
    "PM2.5": "mean"
}).reset_index()

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=monthly_df, x='date', y='PM2.5', marker='o', linewidth=2, color="#90CAF9", ax=ax)
ax.set_ylabel("Rata-rata PM2.5")
ax.set_xlabel("Tanggal")
ax.set_title("Fluktuasi Kualitas Udara Bulanan")
st.pyplot(fig)

# --- Visualisasi 2: Perbandingan Stasiun (Menjawab Pertanyaan 2) ---
st.subheader('2. Perbandingan Tingkat Polusi Antar Stasiun')
st.markdown("*Mengidentifikasi stasiun dengan rata-rata polusi tertinggi dan terendah.*")

station_avg = filtered_df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x="PM2.5", y="station", data=station_avg, palette="viridis", ax=ax2)
ax2.set_ylabel(None)
ax2.set_xlabel("Rata-rata PM2.5")
ax2.set_title("Peringkat Stasiun Berdasarkan Rata-rata Polusi")
st.pyplot(fig2)

st.markdown("---")

# --- Visualisasi 3: Korelasi Faktor Cuaca (Analisis Tambahan) ---
st.subheader('3. Pengaruh Faktor Cuaca')
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### PM2.5 vs Curah Hujan")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='RAIN', y='PM2.5', alpha=0.5, ax=ax3)
    ax3.set_title("Korelasi Hujan & Polusi")
    st.pyplot(fig3)

with col2:
    st.markdown("#### PM2.5 vs Suhu")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='TEMP', y='PM2.5', alpha=0.5, color='orange', ax=ax4)
    ax4.set_title("Korelasi Suhu & Polusi")
    st.pyplot(fig4)

# --- Visualisasi 4: Distribusi Kategori (Analisis Lanjutan) ---
st.subheader('4. Distribusi Kategori Kualitas Udara')

def categorize_pm25(pm):
    if pm <= 35: return 'Good'
    elif pm <= 75: return 'Moderate'
    elif pm <= 115: return 'Unhealthy for Sensitive Groups'
    elif pm <= 150: return 'Unhealthy'
    elif pm <= 250: return 'Very Unhealthy'
    else: return 'Hazardous'

filtered_df['PM2.5_Category'] = filtered_df['PM2.5'].apply(categorize_pm25)
category_counts = filtered_df['PM2.5_Category'].value_counts()

# Urutan kategori agar grafik rapi
order = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
# Filter order hanya yang ada datanya
existing_order = [x for x in order if x in category_counts.index]

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, order=existing_order, palette="rocket", ax=ax5)
plt.xticks(rotation=45)
ax5.set_ylabel("Jumlah Jam")
ax5.set_title("Frekuensi Kategori Kualitas Udara")
st.pyplot(fig5)

st.caption('Copyright (c) 2026 - Air Quality Dashboard')