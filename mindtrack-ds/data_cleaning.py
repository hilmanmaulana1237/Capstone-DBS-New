import pandas as pd
import numpy as np

print("====================================")
print("  MindTrack - Data Cleaning Script")
print("====================================")

# 1. Load Data Mentah
try:
    df = pd.read_csv('dataset_raw.csv')
    print(f"[1] Berhasil memuat data: {df.shape[0]} baris, {df.shape[1]} kolom.")
except Exception as e:
    print(f"Error memuat file: {e}")
    exit()

# 2. Inspeksi Dataset
print(f"[2] Menghitung sel kosong (NaN):")
print(df.isnull().sum()[df.isnull().sum() > 0])

duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"    Menemukan {duplicates} baris duplikat. Menghapusnya...")
    df = df.drop_duplicates()
else:
    print("    Tidak ditemukan baris duplikat.")

# 3. Membersihkan Kolom Blood Pressure
# Format asli: "120/80" -> Kita pisah jadi 'Systolic BP' dan 'Diastolic BP'
if 'Blood Pressure' in df.columns:
    print("[3] Memisahkan kolom Blood Pressure ditarik menjadi numerik Systolic/Diastolic...")
    df[['Systolic BP', 'Diastolic BP']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
    df = df.drop('Blood Pressure', axis=1)

# 4. Menangani Nilai Kosong pada Sleep Disorder
if 'Sleep Disorder' in df.columns:
    print("[4] Mengganti nilai kosong pada gangguan tidur menjadi 'Aman' (Tidak ada)...")
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('Aman')
    df['Sleep Disorder'] = df['Sleep Disorder'].replace('None', 'Aman')

# 5. Mengecek Data Imbalance (Distribusi Target)
print("[5] Cek Distribusi Label Target (Sleep Disorder):")
dist = df['Sleep Disorder'].value_counts(normalize=True) * 100
for k, v in dist.items():
    print(f"    - {k}: {v:.1f}%")

if dist.max() > 70.0:
    print("    Peringatan: Data Imbalance terdeteksi! Kelas mayoritas mendominasi > 70%.")
else:
    print("    Keseimbangan target (Label Distribusi) cukup terdistribusi baik.")

# 6. Menyimpan Hasil Akhir
output_file = 'dataset_clean.csv'
df.to_csv(output_file, index=False)
print(f"\n[Selesai] Data berhasil dibersihkan dan disimpan sebagai '{output_file}'!")
print("Sekarang model AI & Visualisasi Streamlit dapat menggunakan data yang sudah tersaring ini.")
