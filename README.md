# Air Quality Analysis Dashboard ✨

Dashboard interaktif untuk menganalisis data kualitas udara (PM2.5) dari berbagai stasiun pemantauan di seluruh wilayah. Visualisasi komprehensif mencakup tren musiman, perbandingan antar wilayah, dan pola polusi udara.

## 📋 Fitur Utama

- **Analisis Temporal**: Visualisasi tren PM2.5 harian, bulanan, dan tahunan
- **Perbandingan Regional**: Bandingkan tingkat polusi antar berbagai stasiun
- **Insight Musiman**: Identifikasi pola polusi berdasarkan musim
- **Dashboard Interaktif**: Interface yang user-friendly dengan Streamlit

## 🚀 Setup Environment

### Opsi 1: Menggunakan Anaconda (Recommended)

```bash
# Buat virtual environment baru
conda create --name main-ds python=3.9

# Aktivasi environment
conda activate main-ds

# Install dependencies
pip install -r requirements.txt
```

### Opsi 2: Menggunakan Shell/Terminal

```bash
# Buat direktori proyek
mkdir proyek_analisis_data
cd proyek_analisis_data

# Install dependencies
pip install -r requirements.txt
```

## 💻 Menjalankan Aplikasi

**⚠️ Penting:** Pastikan Anda berada di dalam direktori `dashboard` sebelum menjalankan aplikasi agar dataset dapat terbaca dengan benar.

```bash
# Masuk ke direktori dashboard
cd dashboard

# Jalankan aplikasi
streamlit run dashboard.py
```

### Troubleshooting

Jika mengalami error saat menjalankan aplikasi, coba gunakan perintah alternatif:

```bash
python -m streamlit run dashboard.py
```

## 📦 Dependencies

Pastikan semua package berikut terinstall (lihat `requirements.txt`):

- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly (optional, untuk visualisasi interaktif)

## 📊 Struktur Proyek

```
proyek_analisis_data/
│
├── dashboard/
│   ├── dashboard.py          # Main application
│   └── data/                 # Dataset folder
│
├── requirements.txt          # Python dependencies
└── README.md                # Dokumentasi
```

## 🎯 Cara Penggunaan

1. Clone atau download repository ini
2. Setup environment sesuai instruksi di atas
3. Masuk ke direktori `dashboard`
4. Jalankan aplikasi dengan streamlit
5. Buka browser di `http://localhost:8501`

## 📝 Catatan

- Dashboard ini menggunakan data PM2.5 dari stasiun pemantauan kualitas udara
- Pastikan dataset tersedia di folder `dashboard/data/`
- Untuk performa optimal, gunakan Python 3.9

## 🤝 Kontribusi

Kontribusi, issues, dan feature requests sangat diterima! Jangan ragu untuk membuat pull request.

## 📄 Lisensi

Project ini bersifat open source dan tersedia untuk penggunaan akademis dan pembelajaran.

---

**Dibuat dengan ❤️ untuk analisis kualitas udara yang lebih baik**
