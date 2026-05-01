# 🧠 MindTrack Capstone

**MindTrack** adalah platform cerdas *End-to-End* pendeteksi dini risiko kesehatan mental dan gangguan tidur (Sleep Apnea & Insomnia) yang dirancang khusus untuk mahasiswa dan pekerja modern. Aplikasi ini menggunakan teknologi _Deep Learning_ berdasarkan **Sleep Health and Lifestyle Dataset** asli dari Kaggle.

Proyek ini dibangun sebagai syarat kelulusan **Coding Camp 2026 powered by DBS Foundation**.

---

## 🌟 Arsitektur Sistem (Microservices)
Aplikasi ini dipecah menjadi 4 kerangka kerja yang berjalan saling terintegrasi:

1. **Frontend (UI/UX Klien)**
   * **Stack:** React.js, Vite, React Router DOM, Vanilla CSS.
   * **Tugas:** Menyediakan Form Asesmen gaya hidup, Halaman Login/Register, dan Papan Riwayat (*History*). Semua lalu lintas data API dikomunikasikan secara *asynchronous* ke Back-End utama.
2. **Backend (Server Pusat & Auth)**
   * **Stack:** Node.js, Express.js, SQLite Persisten, JWT, Bcrypt.
   * **Tugas:** Gerbang utama sistem. Mencatat pengguna ke database `.db` fisik, menerbitkan *Token Authorization*, serta mendistribusikan JSON kalkulasi *(Proxy)* ke mesin AI Python.
3. **AI Engineer (Inference Service)**
   * **Stack:** Python 3.12, FastAPI, Uvicorn, TensorFlow/Keras.
   * **Tugas:** Menjalankan otak Artificial Intelligence (Algoritma *Deep Learning Functional API* dengan *Custom Attention Layer* bertingkat) yang siaga melayani *request* `/predict` dan mengembalikan persentase diagnosis.
4. **Data Science (Eksplorasi Data & Dashboard)**
   * **Stack:** Python, Streamlit, Pandas, Plotly, Seaborn.
   * **Tugas:** Pusat pembersihan dataset, visualisasi *Exploratory Data Analysis* (korelasi pearson, histogram multi-label), dan mesin wawasan interaktif bagi tenaga medis dan pemangku kepentingan.

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

Anda membutuhkan 4 terminal yang berjalan secara paralel agar aplikasi E2E ini hidup.

### 1. Menyalakan AI Model (Wajib Pertama)
Pastikan Anda memiliki Python 3.12 lalu jalankan komputasi mesin pembelajaran AI:
```bash
cd mindtrack-ai
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Menyalakan Backend Server
```bash
cd mindtrack-backend
npm install
npm run start
```
*Server akan mengunci port 3000 dan mengaktifkan database SQLite `mindtrack.db`.*

### 3. Menyalakan Frontend Web
```bash
cd mindtrack-frontend
npm install
npm run dev
```
*Buka browser di http://localhost:5173*.

### 4. Buka Streamlit Data Science (Opsional)
Untuk melihat papan analisis statis:
```bash
cd mindtrack-ds
.\venv\Scripts\activate
streamlit run app.py
```

---

## 📚 Struktur Direktori Utama
```
D:\Capstone DBS\
├── mindtrack-ai/         # Logika Model TensorFlow & Endpoint Uvicorn FastAPI
├── mindtrack-backend/    # Server Express Node.js & Database .db
├── mindtrack-ds/         # Skrip Pembersihan Data & Streamlit Data Science
├── mindtrack-frontend/   # React Front-End App
├── .gitignore            # Filter git untuk menyembunyikan module/venv
├── .env.example          # Struktur variabel lingkungan Vercel/Render
└── README.md             # Dokumen ini
```

## 🌐 Rancangan Deployment (Segera Datang)
1. **React Frontend**: Vercel (Menggunakan environment `VITE_API_URL`)
2. **Express Backend**: Render.com (Web Service)
3. **FastAPI AI**: Render.com / Railway
4. **Streamlit**: Streamlit Community Cloud

*(Dibuat sepenuh hati oleh Grup Capstone untuk Coding Camp 2026)*
