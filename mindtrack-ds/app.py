import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="MindTrack Analytics Dashboard",
    page_icon="🧠",
    layout="wide"
)

# ── CSS Custom ────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    .insight-box {
        background: #f0f7ff;
        border-left: 4px solid #2d6a9f;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1e3a5f; /* Memaksa warna teks menjadi gelap agar kontras */
    }
    h1 { color: #1e3a5f; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 MindTrack: Sleep Health Analytics Dashboard")
st.caption("Powered by Kaggle Dataset: Sleep Health and Lifestyle (374 Responden)")

# ── Load Data ─────────────────────────────────
@st.cache_data
def load_data():
    if not os.path.exists('dataset_clean.csv'):
        st.error("File dataset_clean.csv tidak ditemukan. Tolong jalankan data_cleaning.py terlebih dahulu.")
        return pd.DataFrame()
    df = pd.read_csv('dataset_clean.csv')
    return df

df = load_data()
if df.empty:
    st.stop()

# ── TABS ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Gambaran Data",
    "📈 Analisis Korelasi",
    "🤖 Evaluasi Model AI",
    "💡 Prediksi Mandiri",
    "🤖 Insight Otomatis"
])

# ══════════════════════════
# TAB 1: GAMBARAN DATA (EDA)
# ══════════════════════════
with tab1:
    st.header("Exploratory Data Analysis (EDA)")

    # Metrik Ringkasan
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Responden", len(df))
    col2.metric("😴 Avg Durasi Tidur", f"{df['Sleep Duration'].mean():.1f} Jam")
    col3.metric("⚡ Avg Aktivitas Fisik", f"{df['Physical Activity Level'].mean():.0f} Menit/Hari")
    col4.metric("❤️ Avg Detak Jantung", f"{df['Heart Rate'].mean():.0f} BPM")

    st.divider()

    # Distribusi Penyakit Tidur (Plotly)
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Distribusi Gangguan Tidur")
        disorder_counts = df['Sleep Disorder'].value_counts().reset_index()
        disorder_counts.columns = ['Gangguan Tidur', 'Jumlah']
        fig1 = px.pie(
            disorder_counts, values='Jumlah', names='Gangguan Tidur',
            color_discrete_sequence=['#2d6a9f', '#e74c3c', '#f39c12'],
            hole=0.4
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Distribusi Gender per Gangguan Tidur")
        fig2 = px.histogram(
            df, x='Sleep Disorder', color='Gender', barmode='group',
            color_discrete_sequence=['#2d6a9f', '#e91e8c'],
            labels={'Sleep Disorder': 'Gangguan Tidur', 'count': 'Jumlah'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Distribusi Durasi Tidur per Penyakit (Histogram Interaktif)")
    fig3 = px.histogram(
        df, x='Sleep Duration', color='Sleep Disorder', barmode='overlay',
        opacity=0.7, nbins=30,
        color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'],
        labels={'Sleep Duration': 'Durasi Tidur (Jam)', 'count': 'Jumlah Responden'}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Hierarki Risiko: Gender → BMI → Penyakit (Sunburst Chart)")
    try:
        fig_sunburst = px.sunburst(
            df, path=['Gender', 'BMI Category', 'Sleep Disorder'], 
            color='Stress Level', color_continuous_scale='RdBu_r',
            title='Eksplorasi Pohon Risiko Gaya Hidup'
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    except Exception as e:
        st.error(f"Sunburst gagal dirender: {e}")

    st.subheader("Data Mentah (10 Baris Pertama)")
    st.dataframe(df.head(10), use_container_width=True)

# ══════════════════════════════
# TAB 2: ANALISIS KORELASI
# ══════════════════════════════
with tab2:
    st.header("Analisis Korelasi antar Variabel")

    numerik_cols = ['Age', 'Sleep Duration', 'Physical Activity Level',
                     'Stress Level', 'Heart Rate', 'Daily Steps',
                     'Quality of Sleep', 'Systolic BP']

    col_c, col_d = st.columns([1.2, 1])
    with col_c:
        st.subheader("Heatmap Korelasi (Pearson)")
        corr = df[numerik_cols].corr()
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, linewidths=0.5, ax=ax4, annot_kws={'size': 9})
        ax4.set_title('Matriks Korelasi Antar Fitur Gaya Hidup')
        st.pyplot(fig4)

    with col_d:
        st.subheader("Scatter: Tidur vs Aktivitas Fisik")
        fig5 = px.scatter(
            df, x='Sleep Duration', y='Physical Activity Level',
            color='Sleep Disorder', size='Age', hover_data=['Occupation'],
            color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'],
            labels={
                'Sleep Duration': 'Durasi Tidur (Jam)',
                'Physical Activity Level': 'Aktivitas Fisik (Menit/Hari)'
            }
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Distribusi Stress Level per Pekerjaan")
    fig6 = px.box(
        df, x='Occupation', y='Stress Level', color='Sleep Disorder',
        color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'],
        labels={'Stress Level': 'Tingkat Stres (1-10)', 'Occupation': 'Pekerjaan'}
    )
    fig6.update_xaxes(tickangle=30)
    st.plotly_chart(fig6, use_container_width=True)

    st.divider()
    st.subheader("Pair Plot Relasional (Multi-Dimensi) AI Features")
    try:
        fig_pair = px.scatter_matrix(
            df, dimensions=['Age', 'Sleep Duration', 'Physical Activity Level', 'Heart Rate', 'Stress Level'],
            color='Sleep Disorder', opacity=0.6,
            color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12']
        )
        fig_pair.update_traces(diagonal_visible=False)
        fig_pair.update_layout(height=800)
        st.plotly_chart(fig_pair, use_container_width=True)
    except Exception as e:
        st.write("Pair plot error:", e)

# ══════════════════════════════
# TAB 3: EVALUASI MODEL AI
# ══════════════════════════════
with tab3:
    st.header("Evaluasi Model TensorFlow Deep Learning")

    if os.path.exists('../mindtrack-ai/model_evaluation.png'):
        st.image('../mindtrack-ai/model_evaluation.png', caption="Confusion Matrix & Feature Importance — MindTrack AI", use_container_width=True)
        st.success("✅ Model sudah dilatih! Confusion Matrix & Feature Importance tampil di atas.")
    else:
        st.warning("""
        ⏳ Grafik evaluasi belum tersedia.
        
        **Langkah untuk menggenerate:**
        1. Buka terminal baru di folder `mindtrack-ai`
        2. Aktifkan virtual environment: `.\\venv\\Scripts\\activate`
        3. Jalankan: `python train_model.py`
        4. Setelah selesai, kembali ke sini dan refresh halaman.
        """)

    st.divider()
    st.subheader("📌 Insight: Mengapa Fitur Ini Dipilih?")
    insights = {
        "Sleep Duration": "Durasi tidur adalah prediktor utama gangguan tidur — responden < 6 jam berisiko tinggi.",
        "Physical Activity Level": "Aktivitas fisik memiliki korelasi negatif dengan risiko insomnia.",
        "Heart Rate": "Detak jantung tinggi saat istirahat adalah indikator Sleep Apnea.",
        "Stress Level": "Stres kronis memperburuk kualitas tidur secara signifikan.",
        "BMI Category": "Obesitas meningkatkan risiko Sleep Apnea 3x lebih tinggi.",
    }
    for feat, desc in insights.items():
        st.markdown(f"""<div class="insight-box">
            <strong>🔹 {feat}</strong><br>{desc}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════
# TAB 4: PREDIKSI MANDIRI
# ══════════════════════════════
with tab4:
    st.header("💡 Coba Prediksi Mandiri")
    st.write("Isi data gaya hidup Anda di bawah ini untuk melihat prakiraan kondisi tidur dari model AI.")

    col_x, col_y = st.columns(2)
    with col_x:
        gender     = st.selectbox("Jenis Kelamin", ["Pria (Male)", "Wanita (Female)"])
        age        = st.slider("Usia", 18, 70, 30)
        sleep_dur  = st.slider("Durasi Tidur (Jam/Hari)", 4.0, 10.0, 7.0, 0.1)
        activity   = st.slider("Aktivitas Fisik (Menit/Hari)", 0, 200, 45)
    with col_y:
        stress     = st.slider("Tingkat Stres (1-10)", 1, 10, 5)
        heart_rate = st.slider("Detak Jantung Istirahat (BPM)", 50, 120, 70)
        steps      = st.number_input("Langkah Kaki Harian", 1000, 25000, 6000, 500)
        bmi        = st.selectbox("Kategori BMI", ["Normal", "Overweight", "Obese"])

    if st.button("🔍 Analisis Sekarang", type="primary", use_container_width=True):
        # Kirim langsung ke FastAPI AI Engine untuk mendapatkan Probability Breakdown tanpa Auth
        import requests
        payload = {
            "gender": 0 if "Pria" in gender else 1,
            "age": age, "sleep_duration": sleep_dur,
            "physical_activity": activity, "heart_rate": heart_rate,
            "daily_steps": steps, "stress_level": stress
        }
        try:
            resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
            data = resp.json()
            disorder = data.get("predicted_disorder", "Tidak Diketahui")

            if "Aman" in disorder or "Normal" in disorder:
                st.success(f"✅ Prediksi Mayoritas: **{disorder}** — Kondisi tidur Anda di level {data.get('risk_level', 'LOW')} Risk")
            elif "Insomnia" in disorder:
                st.warning(f"⚠️ Prediksi Mayoritas: **{disorder}** — Risiko Anda {data.get('risk_level', 'MEDIUM')} Risk")
            else:
                st.error(f"🚨 Prediksi Mayoritas: **{disorder}** — Peringatan {data.get('risk_level', 'HIGH')} Risk!")

            if "probabilities" in data:
                st.subheader("Distribusi Probabilitas Model")
                probs_df = pd.DataFrame(list(data["probabilities"].items()), columns=['Diagnosis', 'Confidence (%)'])
                fig_bar = px.bar(probs_df, x='Confidence (%)', y='Diagnosis', orientation='h', color='Diagnosis', text='Confidence (%)', color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c'])
                fig_bar.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")
            st.markdown("### 📊 Interpretasi Fitur vs Populasi:")
            st.write(f"- **Tidur Anda**: {sleep_dur} jam *(Rata-rata populasi: {df['Sleep Duration'].mean():.1f} jam)*")
            st.write(f"- **BPM Anda**: {heart_rate} BPM *(Rata-rata populasi: {df['Heart Rate'].mean():.1f} BPM)*")
            st.write(f"- **Aktivitas Fisik**: {activity} menit *(Rata-rata populasi: {df['Physical Activity Level'].mean():.1f} menit)*")

        except Exception as e:
            st.error(f"Gagal menghubungi Engine TensorFlow API (Localhost:8000).\nDetail: {e}")

# ══════════════════════════════
# TAB 5: INSIGHT OTOMATIS
# ══════════════════════════════
with tab5:
    st.header("🤖 Analisis Otomatis AI terhadap Dataset")
    st.write("Sistem mendeteksi narasi langsung dari parameter statistik `dataset_clean.csv` Anda:")
    
    # Generate insights based on live data
    avg_sleep = df['Sleep Duration'].mean()
    insomnia_pct = len(df[df['Sleep Disorder'] == 'Insomnia']) / len(df) * 100
    apnea_pct = len(df[df['Sleep Disorder'] == 'Sleep Apnea']) / len(df) * 100
    aman_pct = len(df[df['Sleep Disorder'].str.contains('Aman')]) / len(df) * 100
    
    st.success(f"📌 **Kesehatan Umum:** Sekitar **{aman_pct:.1f}%** populasi Anda tidak memiliki gangguan tidur kritis. Sisanya terbagi atas Insomnia ({insomnia_pct:.1f}%) dan Sleep Apnea ({apnea_pct:.1f}%).")
    
    # BMI insight
    if 'BMI Category' in df.columns:
        obese_with_apnea = len(df[(df['BMI Category'] == 'Obese') & (df['Sleep Disorder'].str.contains('Apnea'))])
        total_obese = len(df[df['BMI Category'] == 'Obese'])
        if total_obese > 0:
            prob_apnea_obese = (obese_with_apnea / total_obese) * 100
            st.warning(f"📌 **Korelasi Obesitas:** Dari total responden ber-BMI 'Obese', sebesar **{prob_apnea_obese:.1f}%** di antaranya mengidap Sleep Apnea. Korelasi tinggi ditemukan antara berat badan berlebih dengan penyumbatan jalan napas saat tidur.")
            
    # Sleep insight
    short_sleepers_insomnia = len(df[(df['Sleep Duration'] < 6.0) & (df['Sleep Disorder'] == 'Insomnia')])
    total_short_sleepers = len(df[df['Sleep Duration'] < 6.0])
    if total_short_sleepers > 0:
        prob = (short_sleepers_insomnia / total_short_sleepers) * 100
        st.error(f"📌 **Korelasi Tidur Kurang:** Respondens yang tidur di bawah 6 jam per hari memiliki probabilitas **{prob:.1f}%** untuk terjangkit Insomnia parah. Ini adalah fitur prediktor terkuat (`Feature Importance` #1) bagi deteksi algoritma neural network kita.")

