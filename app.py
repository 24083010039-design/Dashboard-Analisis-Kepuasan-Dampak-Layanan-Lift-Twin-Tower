# ====================================================================
# 🎓 DASHBOARD FINAL: ANALISIS & SOLUSI SURVEI LIFT TWIN TOWER
# (VERSI SIAP DEPLOY/UPLOAD KE GITHUB)
# ====================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# KONFIGURASI HALAMAN & FONT
# ==============================
st.set_page_config(
    page_title="Dashboard Analisis Lift UPNV Jatim",
    layout="wide",
    page_icon="🏢",
)

# Kustomisasi CSS untuk Font Montserrat dan estetika lainnya
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Montserrat', sans-serif;
}
.stMetric {
    background-color: #F0F2F6;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #E0E0E0;
}

/* === ATURAN UMUM: MEMAKSA SEMUA FONT MENJADI GELAP & BOLD === */
p, h1, h2, h3, h4, h5, h6, .stMarkdown, .stHeader, .stSubheader, li, label {
    color: #31333F !important;
    font-weight: bold !important;
}

/* === PERBAIKAN KHUSUS UNTUK KPI/METRIC YANG PUTIH (INI KUNCINYA) === */
div[data-testid="stMetric"] label[data-testid="stMetricLabel"] p {
    color: #31333F !important; /* Warna Label (mis: "Tingkat Ketidakpuasan") */
    font-weight: bold !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #31333F !important; /* Warna Value (mis: "63.9%") */
    font-weight: bold !important;
}

/* Memastikan teks di dalam tabel juga menjadi gelap & bold */
.stDataFrame th, .stDataFrame td {
    color: #31333F !important;
    font-weight: bold !importan
    t;
}
/* ============================================================= */

</style>
""", unsafe_allow_html=True)


# ==============================
# FUNGSI UNTUK MEMBACA DATA (JAUH LEBIH SIMPEL)
# ==============================
@st.cache_data
def muat_data():
    # <<< INI BAGIAN YANG MEMBACA DATA BERSIHMU
    try:
        # Kita hanya membaca SATU file yang sudah bersih
        df_lengkap = pd.read_csv("data_final_bersih.csv")
        return df_lengkap
    except FileNotFoundError:
        st.error("❌ GAGAL MEMBACA FILE 'data_final_bersih.csv'. Pastikan file tersebut ada di folder yang sama dengan app.py.")
        return None

df_original = muat_data()

# ==============================
# JUDUL UTAMA DAN PENDAHULUAN
# ==============================
st.title("🎓 Dashboard Analisis Kepuasan & Dampak Layanan Lift Twin Tower")
st.markdown("Analisis Data Eksploratif untuk Menemukan Solusi Berbasis Data dari Survei Mahasiswa UPN 'Veteran' Jawa Timur dari kelompok josjis: Marsha Suciana (24083010039)| Putri Amanda Khairunnisa (24083010046)| Esthi Nurani Sri Handayani (24083010081)")

if df_original is None:
    # Error sudah ditangani di dalam fungsi muat_data()
    pass
else:
    # ==============================
    # SIDEBAR UNTUK FILTER GLOBAL
    # ==============================
    st.sidebar.header("Filter Data Responden")
    
    df_filtered = df_original.copy()

    list_fakultas = ['Semua Fakultas'] + df_original['Fakultas'].dropna().unique().tolist()
    fakultas_pilihan = st.sidebar.selectbox("Pilih Fakultas:", options=list_fakultas)

    if fakultas_pilihan != 'Semua Fakultas':
        df_filtered = df_filtered[df_filtered['Fakultas'] == fakultas_pilihan]

    list_prodi = ['Semua Prodi'] + df_filtered['Prodi'].dropna().unique().tolist()
    prodi_pilihan = st.sidebar.selectbox("Pilih Program Studi:", options=list_prodi)

    if prodi_pilihan != 'Semua Prodi':
        df_filtered = df_filtered[df_filtered['Prodi'] == prodi_pilihan]

    st.sidebar.info(f"Menampilkan **{len(df_filtered)}** dari **{len(df_original)}** total responden.")
    st.sidebar.markdown("---")
    st.sidebar.write("Dibuat oleh: Marsha")
    
    # ==============================
    # MEMBUAT TABS
    # ==============================
    tab_ringkasan, tab_analisis = st.tabs(["**Ringkasan & Solusi** 💡", "**Analisis Detail** 🔍"])

    # ==============================
    # ISI TAB 1: RINGKASAN & SOLUSI
    # ==============================
    with tab_ringkasan:
        st.header("Ringkasan Utama dan Rekomendasi Solusi")
        
        if len(df_filtered) > 0:
            st.markdown(f"Analisis ini didasarkan pada **{len(df_filtered)} responden** yang dipilih.")
            # --- KPI UTAMA ---
            c1, c2, c3 = st.columns(3)
            # Perhatikan: Kita sekarang menghitung berdasarkan kolom label, bukan 'num_kecukupan_lift'
            tingkat_ketidaksetujuan = df_filtered[
                df_filtered['label_kecukupan'].isin(['Tidak Setuju', 'Sangat Tdk Setuju'])
            ].shape[0] / len(df_filtered) * 100
            
            penyebab_utama = df_filtered['label_penyebab'].mode()[0]
            solusi_teratas = df_filtered['label_saran_detail'].mode()[0]

            c1.metric("Tingkat Ketidakpuasan", f"{tingkat_ketidaksetujuan:.1f}%", help="Persentase responden yang merasa jumlah lift 'Tidak Setuju' atau 'Sangat Tidak Setuju' sudah mencukupi.")
            c2.metric("Akar Masalah Utama", penyebab_utama)
            c3.metric("Solusi Paling Diinginkan", solusi_teratas)
            st.divider()

            # --- REKOMENDASI SOLUSI ---
            st.subheader("Rekomendasi Solusi Berbasis Data")
            
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                st.markdown(f"Akar masalah utamanya adalah **{penyebab_utama}**. Solusi yang paling banyak disarankan oleh mahasiswa adalah **{solusi_teratas}**.")
                saran_data = df_filtered['label_saran_detail'].value_counts().reset_index()
                fig_saran = px.bar(saran_data, x='count', y='label_saran_detail', orientation='h', title="Peringkat Kategori Saran dari Mahasiswa", text_auto=True, color='count', color_continuous_scale=px.colors.sequential.Teal)
                fig_saran.update_layout(yaxis_title="", xaxis_title="Jumlah Responden")
                st.plotly_chart(fig_saran, use_container_width=True)

            with col2:
                st.markdown("#### **Poin-Poin Kunci:**")
                st.info("""
                1.  **Ketidakpuasan Mayoritas:** Sebagian besar mahasiswa merasa jumlah lift yang ada saat ini tidak mencukupi.
                2.  **Fokus pada Penambahan Unit:** Solusi yang paling konkret adalah penambahan unit lift baru atau penyediaan alternatif vertikal seperti eskalator.
                3.  **Masalah Jam Sibuk:** Kepadatan pada jam-jam tertentu memperparah masalah, menunjukkan perlunya pengaturan antrean.
                4.  **Kenyamanan Terganggu:** Selain antrean, fasilitas seperti pendingin udara (AC) juga menjadi keluhan utama.
                """)
                st.warning("**Langkah Selanjutnya:** Data ini sangat kuat untuk diajukan kepada pihak manajemen gedung atau rektorat sebagai dasar untuk pengajuan penambahan fasilitas.")
        else:
            st.warning("Tidak ada data untuk ditampilkan dengan filter yang dipilih.")

    # ==============================
    # ISI TAB 2: ANALISIS DETAIL
    # ==============================
    with tab_analisis:
        st.header("Analisis Data Eksploratif Secara Mendalam")

        if len(df_filtered) > 0:
            # --- 1. Profil Penggunaan Lift ---
            st.subheader("A. Profil Penggunaan Lift")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Seberapa sering Anda menggunakan lift?**")
                frek_data = df_filtered['label_frek_penggunaan'].value_counts().reindex(['Tidak Pernah', 'Sangat Jarang', 'Jarang', 'Kadang-kadang', 'Sering', 'Sangat Sering']).reset_index()
                fig_frek = px.bar(frek_data, x='label_frek_penggunaan', y='count', text_auto=True, title="Frekuensi Penggunaan Lift", color='count', color_continuous_scale=px.colors.sequential.Blues)
                st.plotly_chart(fig_frek, use_container_width=True)
            with col2:
                st.markdown("**Berapa lama rata-rata waktu tunggu di jam sibuk?**")
                waktu_data = df_filtered['label_waktu_tunggu'].value_counts().reindex(['< 3 Menit', '3-5 Menit', '5-10 Menit', '> 10 Menit']).reset_index()
                fig_waktu = px.bar(waktu_data, x='label_waktu_tunggu', y='count', text_auto=True, title="Waktu Tunggu di Jam Sibuk", color='count', color_continuous_scale=px.colors.sequential.Purples)
                st.plotly_chart(fig_waktu, use_container_width=True)
            st.divider()

            # --- 2. Persepsi dan Dampak Negatif ---
            st.subheader("B. Persepsi dan Dampak Negatif")
            col1, col2 = st.columns([0.4, 0.6])
            with col1:
                st.markdown("**Apakah jumlah lift mencukupi?**")
                kecukupan_data = df_filtered['label_kecukupan'].value_counts().reset_index()
                fig_donut = px.pie(kecukupan_data, names='label_kecukupan', values='count', hole=0.5, color_discrete_sequence=px.colors.sequential.OrRd)
                st.plotly_chart(fig_donut, use_container_width=True)
            with col2:
                st.markdown("**Pengalaman negatif apa yang paling sering terjadi?**")
                pengalaman_df = df_filtered.melt(value_vars=['label_pengalaman_masuk', 'label_frek_menyerobot', 'label_rasa_tidak_nyaman', 'label_terlambat'], var_name='Kategori', value_name='Frekuensi')
                pengalaman_summary = pengalaman_df[pengalaman_df['Frekuensi'] == 'Sering'].groupby('Kategori').size().reset_index(name='Jumlah')
                pengalaman_summary['Kategori'] = pengalaman_summary['Kategori'].replace({'label_pengalaman_masuk': 'Orang Masuk Sblm Keluar', 'label_frek_menyerobot': 'Menyerobot Antrean', 'label_rasa_tidak_nyaman': 'Merasa Tidak Nyaman', 'label_terlambat': 'Terlambat Kelas'})
                fig_pengalaman = px.bar(pengalaman_summary.sort_values('Jumlah'), x='Jumlah', y='Kategori', orientation='h', text_auto=True, title="Jumlah Responden yang 'Sering' Mengalami", color='Jumlah', color_continuous_scale=px.colors.sequential.Reds)
                st.plotly_chart(fig_pengalaman, use_container_width=True)
            st.divider()

            # --- 3. Analisis Penyebab, Kendala, dan Saran ---
            st.subheader("C. Analisis Penyebab, Kendala, dan Saran")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Apa penyebab utama antrean?**")
                penyebab_data = df_filtered['label_penyebab'].value_counts().reset_index()
                fig_penyebab = px.bar(penyebab_data.sort_values('count'), x='count', y='label_penyebab', orientation='h', text_auto=True, color='count', color_continuous_scale='Greens', title="Penyebab Utama Antrean")
                st.plotly_chart(fig_penyebab, use_container_width=True)
            with col2:
                st.markdown("**Apa kendala utama yang dialami?**")
                kendala_data = df_filtered['label_kendala'].value_counts().reset_index()
                fig_kendala = px.bar(kendala_data.sort_values('count'), x='count', y='label_kendala', orientation='h', text_auto=True, color='count', color_continuous_scale='Oranges', title="Kendala Utama Penggunaan Lift")
                st.plotly_chart(fig_kendala, use_container_width=True)
            
            # --- 4. Detail Saran Teks Asli ---
            st.subheader("D. Detail Saran dan Masukan dari Responden")
            st.markdown("Berikut adalah beberapa saran asli yang ditulis oleh responden (difilter berdasarkan pilihan Anda).")
            saran_asli = df_filtered[['Fakultas', 'Prodi', 'Saran_Masukan']].dropna()
            saran_asli = saran_asli[saran_asli['Saran_Masukan'].str.len() > 5]
            st.dataframe(saran_asli, height=400, use_container_width=True)
            st.divider()

            # --- 5. Matriks Korelasi ---
            st.subheader("E. Matriks Korelasi (Hubungan Antar Variabel)")
            st.markdown("Heatmap ini menunjukkan korelasi antar jawaban numerik. Angka mendekati 1 (biru tua) atau -1 (merah tua) menunjukkan hubungan yang kuat.")
            
            # Kita masih perlu kolom numerik asli untuk korelasi
            kolom_numerik_saja = df_filtered.columns[df_filtered.columns.str.startswith('num_')]
            if len(kolom_numerik_saja) >= 2:
                corr = df_filtered[kolom_numerik_saja].corr()
                fig_heatmap, ax = plt.subplots(figsize=(12, 9))
                sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5, ax=ax)
                ax.set_title("Matriks Korelasi", fontsize=16)
                st.pyplot(fig_heatmap)
        else:
            st.warning("Tidak ada data untuk ditampilkan dengan filter yang dipilih.")