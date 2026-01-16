import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
min_date = df['date'].min()
max_date = df['date'].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

selected_station = st.sidebar.multiselect(
    label="Pilih Stasiun",
    options=df['station'].unique(),
    default=df['station'].unique()
)

# Filter Data berdasarkan input
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) & 
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['station'].isin(selected_station))
]

# Judul Dashboard
st.title('Air Quality Analysis Dashboard')

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

# Visualisasi 1: Tren PM2.5 Seiring Waktu
st.subheader('Tren Kualitas Udara (PM2.5) Harian')
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=filtered_df, x='date', y='PM2.5', hue='station', ax=ax)
ax.set_ylabel("Konsentrasi PM2.5")
ax.set_xlabel("Tanggal")
st.pyplot(fig)

# Visualisasi 2: Korelasi Faktor Cuaca
st.subheader('Pengaruh Cuaca Terhadap Polusi')
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Hubungan PM2.5 vs Curah Hujan (RAIN)")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='RAIN', y='PM2.5', alpha=0.5, ax=ax2)
    st.pyplot(fig2)

with col2:
    st.markdown("#### Hubungan PM2.5 vs Suhu (TEMP)")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='TEMP', y='PM2.5', alpha=0.5, color='orange', ax=ax3)
    st.pyplot(fig3)

# Analisis Lanjutan: Kategori Kualitas Udara (Binning)
st.subheader('Distribusi Kategori Kualitas Udara')
def categorize_pm25(pm):
    if pm <= 35: return 'Good'
    elif pm <= 75: return 'Moderate'
    elif pm <= 115: return 'Unhealthy for Sensitive Groups'
    elif pm <= 150: return 'Unhealthy'
    elif pm <= 250: return 'Very Unhealthy'
    else: return 'Hazardous'

filtered_df['PM2.5_Category'] = filtered_df['PM2.5'].apply(categorize_pm25)
category_counts = filtered_df['PM2.5_Category'].value_counts()

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis", ax=ax4)
plt.xticks(rotation=45)
ax4.set_ylabel("Jumlah Observasi (Jam)")
st.pyplot(fig4)

st.caption('Copyright (c) 2026')