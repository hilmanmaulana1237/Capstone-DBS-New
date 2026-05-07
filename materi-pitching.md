# 🎤 Naskah & Struktur Presentasi (Pitching) MindTrack
**Durasi Maksimal:** 10 Menit
**Total Anggota:** 6 Orang (~1.5 Menit / Orang)

Berikut adalah panduan slide dan naskah bicara (script) agar presentasi terstruktur, rapi, dan mencakup semua kriteria dari DBS Foundation.

---

## 🟢 SLIDE 1 & 2: Opening & Latar Belakang (Waktu: 0:00 - 1:30)
**Speaker: Hilman Maulana (AI Engineer)**

*   **Konten Slide:** Logo MindTrack, Nama Anggota Tim, Grafik WHO / Statistik Burnout & Depresi.
*   **Draft Naskah:**
    > "Halo Dewan Juri dan teman-teman semua. Kami dari Tim CC26-PSU264 dengan bangga mempresentasikan **MindTrack**, sebuah Sistem Deteksi Dini Risiko Kesehatan Mental dan Burnout Berbasis AI. 
    > 
    > Tahukah Anda, menurut data WHO dan Riskesdas, angka depresi dan stres kerja di Indonesia melonjak drastis. Masalah utamanya adalah: kita baru sadar ketika kesehatan kita sudah *drop*. Akses ke psikiater masih mahal dan dipenuhi stigma. Oleh karena itu, kami membangun MindTrack sebagai **Painkiller**, bukan sekadar vitamin. Kami ingin memecahkan masalah ini dengan memberikan deteksi awal yang non-invasif, cukup dengan menganalisis pola tidur dan gaya hidup pengguna secara instan."

## 🟡 SLIDE 3 & 4: Data Analytics & Insight (Waktu: 1:30 - 3:00)
**Speaker: Sarah Nurul Yakin (Data Scientist)**

*   **Konten Slide:** Screenshot Dashboard Streamlit, Grafik Sunburst/Pie Chart Distribusi Dataset.
*   **Draft Naskah:**
    > "Untuk membangun sistem yang cerdas, semuanya berawal dari data. Kami mengekstrak dan membersihkan *Sleep Health and Lifestyle Dataset* yang terdiri dari metrik gaya hidup seperti durasi tidur, detak jantung, dan level aktivitas fisik. 
    > 
    > Melalui Exploratory Data Analysis, kami menemukan insight penting: *Terdapat korelasi yang sangat kuat antara durasi tidur di bawah 6 jam dengan probabilitas tinggi terkena Insomnia*. Insight analitik ini tidak kami simpan sendiri, melainkan kami deploy menjadi Dashboard Streamlit interaktif yang dapat digunakan oleh perusahaan untuk memantau kesehatan populasi karyawannya secara *real-time*."

## 🟡 SLIDE 5 & 6: Komparasi, SWOT, & Implementasi Lokal (Waktu: 3:00 - 4:30)
**Speaker: Nisrina Aliya Tharifah (Data Science)**

*   **Konten Slide:** Tabel Perbandingan (MindTrack vs Flo/Apple Health), Matriks SWOT, Timeline Implementasi.
*   **Draft Naskah:**
    > "Jika dibandingkan dengan aplikasi bawaan *smartwatch*, aplikasi di pasaran saat ini hanya bersifat mencatat atau *tracking*. MindTrack berbeda, kami menggunakan algoritma prediksi cerdas yang memberikan peringatan dini medis. 
    > 
    > Dari analisis SWOT kami, kekuatan utama kami ada di pendekatan non-invasif dan akurasi tinggi, meskipun tantangannya adalah dataset yang masih harus diperluas. Dalam 6 bulan ke depan, rencana implementasi lokal kami adalah membawa MindTrack sebagai program B2B (*Employee Wellness*) untuk melakukan *pilot project* dengan divisi HR perusahaan demi mencegah *burnout* massal karyawan."

## 🟢 SLIDE 7 & 8: Keunggulan Model AI (Waktu: 4:30 - 6:00)
**Speaker: Naisila Zia Ulhaq (AI Engineer)**

*   **Konten Slide:** Arsitektur TensorFlow, Angka Akurasi 92%, Confusion Matrix.
*   **Draft Naskah:**
    > "Sebagai otak dari MindTrack, kami mengembangkan model klasifikasi multi-class (Normal, Insomnia, Sleep Apnea) *from scratch* menggunakan TensorFlow Functional API. 
    > 
    > Kami tidak menggunakan *AutoML*, melainkan merancang arsitektur Deep Learning sendiri dengan mengimplementasikan **Custom Attention Layer**. Layer ini bertugas memberi bobot lebih besar pada input yang paling krusial. Hasilnya? Meskipun dataset cukup *imbalanced*, optimasi yang kami lakukan berhasil mendongkrak performa model hingga mencapai akurasi **92.00%**, melampaui standar kelulusan Capstone."

## 🔵 SLIDE 9 & 10: Arsitektur Tech Stack & Integrasi (Waktu: 6:00 - 7:30)
**Speaker: Ariel Aziz Bhadrika (Full-Stack Web Developer)**

*   **Konten Slide:** Diagram Arsitektur Microservices (React -> Express -> FastAPI).
*   **Draft Naskah:**
    > "Untuk menyajikan AI tersebut ke pengguna, kami membangun arsitektur web berbasis Microservices. Kami menggunakan **Vite & React** beserta Tailwind CSS di sisi Frontend untuk *rendering* yang responsif. 
    > 
    > Untuk Backend, kami memilih **Express.js** dan database **SQLite** agar histori pengguna tersimpan ringan namun aman dengan autentikasi JWT. Mengapa kami pisah? Agar server AI (FastAPI Python) dan server aplikasi tidak membebani satu sama lain. Arsitektur RESTful yang kokoh ini memastikan aplikasi tidak akan *crash* meskipun menerima banyak *request* prediksi."

## 🔵 SLIDE 11 & 12: Demo Produk & Penutup (Waktu: 7:30 - 9:30)
**Speaker: Agung Permana (Full-Stack Web Developer)**

*   **Konten Slide:** Video Screen-record Aplikasi (Screencast), Link GitHub & Dokumentasi.
*   **Draft Naskah:**
    > *(Sambil memutar video demo di slide)*
    > "Mari kita lihat demonya. Pengguna cukup login, lalu mengisi form gaya hidup hariannya. Saat menekan tombol 'Analisis', request dikirim ke backend dan diproses oleh AI kami dalam hitungan detik. Hasilnya keluar berupa persentase probabilitas, sehingga pengguna tahu tindakan medis apa yang harus diambil selanjutnya.
    > 
    > Seluruh baris kode, dokumentasi README, dan tautan *deployment* Vercel/Render telah kami publikasikan di repositori GitHub kami. Sekian presentasi dari Tim CC26-PSU264. MindTrack: Pantau Pikiranmu, Lindungi Masa Depanmu. Terima Kasih."

---

## 📝 Tips Rekaman Pitching
1. **Google Meet:** Gunakan Google Meet, minta salah satu orang *share screen* slide presentasinya, lalu mulai *Record*. 
2. **On Cam:** Pastikan wajah semua anggota terlihat saat bicara.
3. **Pakaian Bebas Rapi:** Sesuaikan dengan aturan penyelenggara.
4. **Latihan Waktu (Gladi Resik):** Pakai *stopwatch* di HP, pastikan tidak ada yang ngomongnya kecepetan atau terlalu lama. Total harus di bawah 10 menit!
5. **Upload YouTube:** Setelah rekaman beres, Agung atau Hilman bisa upload ke YouTube. Jangan lupa ubah privasinya ke **Unlisted** (Tidak Publik), lalu *copy* link-nya.
