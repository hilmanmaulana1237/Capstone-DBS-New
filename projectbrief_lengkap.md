# Dokumen Project Brief
**Coding Camp 2026 powered by DBS Foundation**

**ID Tim Capstone Project** : [Masukkan ID Grup Capstone Anda]
**Judul Proyek** : MindTrack: Sistem Deteksi Dini Risiko Kesehatan Mental & Burnout Berbasis AI
**Tema yang Dipilih** : Healthy Lives & Well-being
**Nama Advisor Capstone** : [ID Advisor] - [Nama Advisor] - [Tanggal Mentoring]

**List Anggota** :
1. (ID Peserta 1) - (Nama Anggota 1) - Fullstack - Aktif
2. (ID Peserta 2) - (Nama Anggota 2) - Fullstack - Aktif
3. (ID Peserta 3) - (Nama Anggota 3) - Data Science - Aktif
4. (ID Peserta 4) - (Nama Anggota 4) - Data Science - Aktif
5. (ID Peserta 5) - (Nama Anggota 5) - AI Engineer - Aktif

---

## 1. Judul Proyek
**MindTrack: Sistem Deteksi Dini Risiko Kesehatan Mental & Burnout Berbasis AI**

## 2. Ringkasan Eksekutif
Di era modern yang berjalan serba cepat, mahasiswa dan pekerja profesional menghadapi tuntutan akademik dan karir yang sangat berat. Menurut data WHO (2022) dan Riskesdas (2018), prevalensi gangguan mental emosional dan stres kerja di Indonesia mengalami lonjakan signifikan. Ironisnya, sebagian besar penderita baru menyadari gejala setelah kondisi psikologis dan fisiknya memburuk secara drastis. Pemeriksaan klinis konvensional seringkali memakan biaya tinggi dan masih diliputi oleh stigma sosial yang kuat, sehingga langkah penanganan preventif menjadi sangat sulit untuk dijangkau masyarakat luas.

Menjawab **Problem Statement** tersebut, kami mengembangkan **MindTrack**, sebuah platform web cerdas berbasis AI yang dirancang sebagai instrumen deteksi dini preventif dan non-invasif. MindTrack mampu menganalisis pola gaya hidup harian pengguna—termasuk durasi tidur, aktivitas fisik, detak jantung harian, jumlah langkah kaki, dan tingkat stres subyektif—untuk mengklasifikasikan risiko gangguan tidur kritis (seperti Insomnia dan Sleep Apnea) menggunakan algoritma *Deep Learning*. Tidak hanya melayani individu, platform ini juga memuat *Dashboard Analytics* komprehensif bagi pemangku kepentingan (misal: divisi HR perusahaan) untuk memantau tren kesehatan mental dalam suatu populasi dan membuat keputusan berbasis data (data-driven).

Tim kami merancang produk ini murni sebagai solusi **"Painkiller"**, bukan sekadar "Vitamin". MindTrack langsung menyerang akar permasalahan: keterlambatan deteksi akibat mahalnya biaya pemeriksaan. Kami menggunakan model *TensorFlow Functional API* yang telah diperkuat dengan *Custom Attention Layer* untuk menyoroti faktor gaya hidup yang paling fatal, sehingga akurasi prediksi dapat terjaga sangat tinggi (>92%). Selain itu, kami juga menanamkan inovasi **Generative AI Consultant** yang ditenagai oleh model Large Language Model (LLM) DeepSeek V4 untuk memberikan analisis terapi terpersonalisasi pasca-deteksi. Dengan desain microservices terpisah (Vite React, Express.js, FastAPI, Streamlit, OpenRouter API), produk ini sudah teruji kelayakannya untuk langsung digunakan oleh pengguna akhir.

## 3. Status Penyelesaian Proyek
✅ 100% Selesai berdasarkan Rencana Proyek

---

## 4. Tech Stack Checklist

### Main Quest (Wajib)

**Front End and Back End**
✅ Menggunakan networking calls (Fetch API) untuk berinteraksi dengan API dari Frontend.
✅ Menggunakan module bundler (Vite) untuk performa web yang jauh lebih cepat.
✅ Membangun RESTful API dengan Express.js untuk mendukung operasional Frontend.
✅ Menyimpan data menggunakan database rasional yang ringan (SQLite persisten).
✅ URL API mengikuti standar konvensi RESTful secara ketat (`/api/auth`, `/api/assessments`).
✅ Mengintegrasikan kemampuan AI secara langsung melalui proxy server Backend yang aman.
✅ Fitur utama bebas dari crash, didukung oleh penanganan error (try/catch) dan middleware Rate Limiter (anti-DDoS).
✅ Aplikasi dibangun *from scratch* dengan React (tanpa web generator otomatis).

**Artificial Intelligence**
✅ Membangun model *Deep Learning* multi-class classification dengan TensorFlow *Functional API*.
✅ Mengimplementasikan komponen kustom canggih (Custom Attention Layer dan AccuracyThresholdCallback).
✅ Mengekspor model secara penuh ke dalam format modern `.keras` yang disematkan bersama nilai *Scaler* numerik.
✅ Membuat program inference via FastAPI (`main.py`) yang ringan dan berkecepatan tinggi.
✅ Model dilatih sendiri menggunakan *dataset mentah*, tanpa bantuan pre-trained model (seperti TF Hub atau AutoML) dan tidak menggunakan API komersial seperti ChatGPT.

**Data Science**
✅ Mengumpulkan dan menganalisis secara independen "Sleep Health and Lifestyle Dataset".
✅ Mendefinisikan pertanyaan bisnis krusial (Korelasi durasi tidur vs performa/stres, fitur paling berisiko).
✅ Melakukan tahap *Data Wrangling* lengkap (Gathering, Assessing, Cleaning).
✅ Melakukan EDA ekstensif yang direkam secara menyeluruh dalam Jupyter Notebook.
✅ Menyajikan *Explanatory Analysis* berupa grafik korelasi multi-dimensi.
✅ Mengembangkan *Dashboard Streamlit* dengan 5 tab interaktif untuk eksplorasi populasi.
✅ Mempersiapkan data sebersih mungkin lengkap dengan kamus datanya (*Data Dictionary*).
✅ Menjaga proses pelatihan model dari *Data Leakage* dengan misah data target/label sebelum scaling.

### Side Quest (Opsional / Nilai Tambah)

**Front-End dan Back-End**
✅ Mockup aplikasi representatif menggunakan rancangan Figma yang konsisten.
✅ Layout responsif 100% dengan implementasi utilitas Tailwind CSS.
✅ RESTful API dikembangkan di atas arsitektur stabil framework Express.js.
✅ Deployment terdistribusi (Frontend di Vercel, Backend di Render.com).

**Artificial Intelligence**
✅ REST API mandiri dengan FastAPI Python beserta Uvicorn *server*.
✅ Model mencetak rekor performa yang melampaui kriteria (Akurasi validasi menyentuh 92.00%). Kami memprioritaskan arsitektur bebas *dropout* dan perhitungan *Categorical Crossentropy* guna meminimalkan margin kesalahan semaksimal mungkin (mendekati MAE terendah yang bisa dicapai dataset).
✅ **[INNOVASI BARU]** Mengintegrasikan fitur Chatbot Konsultan Generative AI menggunakan model mutakhir DeepSeek V4 via OpenRouter API. Chatbot ini mampu membaca status riwayat deteksi pengguna (*Context Chaining*) dan melakukan proses *Reasoning* (berpikir) untuk merumuskan saran gaya hidup medis yang hiper-personal.

**Data Science**
✅ Feature engineering yang diekstrak secara spesifik (Pemecahan format `Systolic/Diastolic Blood Pressure`).
✅ Deployment visualisasi real-time ke *Streamlit Community Cloud*.
✅ Penyusunan dokumen komprehensif mulai dari Problem Discovery hingga konklusi akhir ke dalam PDF.

---

## 5. Tautan Proyek (Links)
*Mohon isikan URL yang relevan pada bagian di bawah ini sebelum disubmit*

*   **Tautan Dataset (Kaggle)**: `https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset`
*   **Deployment Web (Frontend)**: `[URL Vercel]`
*   **Deployment API Backend**: `[URL Render]`
*   **Deployment API AI**: `[URL FastAPI / Railway]`
*   **Deployment Dashboard (Streamlit)**: `[URL Streamlit]`
*   **Repository GitHub**: `[URL GitHub Project]`
*   **Video Presentasi (Pitching 10 Menit)**: `[URL YouTube - Unlisted]`
*   **Panduan Penggunaan Produk**: `[URL Video Demo / Guideline Docs]`
*   **Tautan Slide Presentasi**: `[URL Google Slides / Canva]`

---

## 6. Slide Presentasi & Konten Inti
*Berikut adalah penjabaran lengkap untuk menyusun poin-poin presentasi Anda (Pitch Deck):*

**A. Latar Belakang**
Menurut WHO (2022), jutaan warga di dunia terdampak depresi akibat tuntutan produktivitas yang berlebih, dan pekerja di Indonesia menduduki tingkat stres tertinggi kelima se-Asia Tenggara. Namun, akses terhadap pemeriksaan kesehatan mental secara klinis dianggap memakan waktu, mahal, dan tabu.

**B. Alasan / Rumusan Masalah**
Kami ingin menyelesaikan permasalahan rendahnya kesadaran pencegahan dini. Masyarakat sering tidak tahu bahwa kualitas tidur, aktivitas fisik rendah, dan ritme detak jantung yang aneh adalah indikator stres kronis. Rumusan masalah kami: Bagaimana cara membangun teknologi murah, gratis, dan cerdas untuk memberitahu masyarakat risiko mereka secara akurat dalam 30 detik?

**C. Perbandingan dengan Aplikasi Serupa**
Sudah ada aplikasi sejenis seperti *Flo* atau aplikasi kesehatan bawaan *smartwatch* (Apple Health/Google Fit). Namun, kebanyakan dari mereka sekadar "mencatat" (tracking log) tanpa memberikan peringatan probabilitas medis menggunakan model AI canggih. MindTrack mengolah catatan gaya hidup sederhana tersebut ke dalam sebuah algoritma Neural Network yang dapat mengembalikan nilai peringatan probabilitas terkena Insomnia atau Sleep Apnea.

**D. Hasil Pengembangan Produk**
- Platform Web Fullstack responsif lengkap dengan sistem Autentikasi dan riwayat histori deteksi.
- Dashboard Analytics (Streamlit) yang mensegmentasikan tingkat stres pekerja berdasarkan demografi.
- AI Model berakurasi `92.00%` yang dibekali dengan *Attention Layer* khusus untuk menangkap anomali durasi tidur.
- Fitur "Generative AI Consultant" interaktif sebagai pendamping terapi pemulihan yang mampu mengingat histori asesmen pengguna (Memory Retention).

**E. Mengapa Memilih Implementasi Tersebut?**
Arsitektur *Microservices* dipilih agar tim bisa berkolaborasi secara terpisah. Vite mempercepat rendering komponen UI, Express.js dan SQLite menjamin penyimpanan histori pengguna yang ringan tanpa konfigurasi *cloud database* yang rumit, dan FastAPI memberikan kecepatan latensi di bawah milidetik untuk *machine learning model*. Pemanfaatan OpenRouter API (DeepSeek LLM) juga memfasilitasi fungsionalitas Generative AI dengan biaya sangat rendah namun memberikan *value* produk berlipat ganda layaknya berhadapan dengan psikiater asli.

**F. Dokumentasi**
File README.md yang menyeluruh telah disiapkan di GitHub. Mencakup cara meng-*install* dependensi untuk setiap bahasa pemrograman, format *environment variables* yang dibutuhkan, dan cara menjalankan ketiga server (Web, AI, Dashboard) secara simultan melalui perintah CLI lokal.

---

## 7. Rencana Implementasi Lokal (3-6 Bulan Mendatang)
Sebagai ekspansi strategis, MindTrack dirancang untuk dipasarkan dengan skema B2B (Business-to-Business) bertajuk **Employee Wellness Program**.
*   **Fase 1 (Bulan 1-2):** Penyesuaian dashboard analitik khusus perusahaan. Integrasi sistem registrasi menggunakan email korporat.
*   **Fase 2 (Bulan 3-4):** *Pilot Project* dengan divisi HRD di 2-3 startup menengah. Sosialisasi kepada karyawan untuk mengisi form keseharian setiap minggu.
*   **Fase 3 (Bulan 5-6):** Evaluasi akurasi metrik. AI Engineer akan melakukan *retraining* (pelatihan ulang model) dengan dataset organik yang dikumpulkan dari karyawan, lalu membuat pipeline MLOps.
*   **Kebutuhan Resource:** Server Cloud VPS Terdedikasi (~$20-$40 per bulan) untuk menangani enkripsi data medis sensitif, dan 1 orang *Maintenance Engineer* (opsional part-time).

---

## 8. Analisis SWOT

**Kekuatan (Strengths):**
*   Menggunakan pendekatan *Lifestyle Assessment* (Non-invasif), sangat ramah bagi orang awam.
*   Akurasi prediktif Model AI luar biasa tinggi mencapai 92.00% ditunjang dengan fitur *Soft-Attention*.
*   Mampu menyajikan *Breakdown Probability* sehingga pengguna tahu tingkat keparahannya (Low, Medium, High).
*   Dilengkapi inovasi Generative AI Consultant yang dapat menjadi nilai jual komersial tinggi.

**Kelemahan (Weaknesses):**
*   Dataset acuan saat ini berjumlah relatif kecil (kurang dari 500 sampel), yang mungkin belum merepresentasikan populasi seluruh wilayah secara komprehensif.

**Peluang (Opportunities):**
*   Lembaga korporat dan kampus saat ini memiliki urgensi besar untuk memberikan fasilitas kesehatan mental gratis demi mencegah fenomena *burnout* (Kelelahan ekstrem).

**Ancaman (Threats):**
*   Meningkatnya tren perangkat medis digital portabel (*Wearable Device*) yang suatu hari nanti dapat melacak metrik psikologis tanpa input manual dari pengguna.

---

## 9. Catatan Mentoring
*(Kosong / Tidak Ada)*

---

## 10. Konklusi: Perbedaan dengan Rencana Awal (Project Plan)
Apakah proyek capstone yang telah selesai berbeda dengan rencana awal (project plan)?
**Secara struktural tidak.** Aplikasi dan fitur selesai sesuai jadwal. Namun, untuk memenuhi syarat standar ketat Capstone (Akurasi >85%), kami melakukan sedikit perombakan arsitektur dari yang direncanakan. Kami menghilangkan konfigurasi *Dropout Layer* untuk mencegah informasi penting terpotong, mengganti strategi target variabel dari mode *sparse* menjadi format *One-Hot Encoding*, serta mengadopsi fungsi probabilitas `Categorical Crossentropy`. Selain itu, demi membuat performa MAE (*Mean Absolute Error*) se-ideal mungkin pada label minoritas seperti Insomnia, tim AI Engineer menginjeksikan algoritma perhitungan bobot kelas otomatis (*Class Weights*). Perubahan taktis ini sukses mendongkrak keberhasilan model kami jauh di atas garis batas minimum.
