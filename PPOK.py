#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from datetime import datetime

import streamlit as st

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Sistem Pakar Diagnosis PPOK",
    page_icon="🫁",
    layout="wide"
)

st.markdown("""
    <style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #E8F6F3;
        padding: 30px 20px;
        width: 280px !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        text-align: center;
        color: #2F4F4F;
    }

    .sidebar-content {
        margin-top: 30px;
        line-height: 2;
        font-size: 16px;
    }

    /* Konten Utama */
    .main-title {
        color: #006666;
        font-size: 28px;
        font-weight: bold;
    }

    .sub-title {
        color: #333;
        font-size: 18px;
    }

    .feature-list {
        margin-left: 30px;
        font-size: 16px;
        line-height: 1.8;
    }

    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("## 🫁 Sistem Pakar Diagnosis Penyakit Paru Obstruktif Kronis")
st.sidebar.divider()
st.sidebar.markdown("""
<div class="sidebar-content">
    <a href="#">🏠 Dashboard</a><br>
    <a href="#">🧪 Diagnosis PPOK</a><br>
    <a href="#">ℹ️ Tentang Aplikasi</a>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.caption("© 2025 Sistem Pakar PPOK | by Rahma Yuliana")

# --- Konten Utama ---
st.markdown("<h1 class='main-title'>Selamat Datang di Sistem Pakar Diagnosis PPOK</h1>", unsafe_allow_html=True)
st.markdown("""
Sistem ini membantu pengguna mendiagnosis <b>Penyakit Paru Obstruktif Kronis (PPOK)</b> 
berdasarkan gejala yang dialami menggunakan metode <b>Dempster-Shafer</b>.
""", unsafe_allow_html=True)

st.markdown("<h3 class='sub-title'>Fitur Utama:</h3>", unsafe_allow_html=True)
st.markdown("""
<ul class='feature-list'>
    <li>Form input pengguna & gejala interaktif</li>
    <li>Proses diagnosis otomatis</li>
    <li>Tingkat keyakinan hasil dalam bentuk persentase</li>
    <li>Saran kesehatan dan pencegahan</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("💡 Klik menu <b>Diagnosis PPOK</b> di sebelah kiri untuk memulai pemeriksaan.", unsafe_allow_html=True)


# ===================== HALAMAN DIAGNOSIS =====================
elif menu == "🩺 Diagnosis PPOK":
    st.markdown("## 🩺 Form Diagnosis PPOK")

    # Basis pengetahuan
    knowledge_base = {
        'G01': {'PPOK': 0.42, 'theta': 0.58},
        'G02': {'PPOK': 0.42, 'theta': 0.58},
        'G03': {'PPOK': 0.14, 'theta': 0.86},
        'G04': {'PPOK': 0.20, 'theta': 0.80},
        'G05': {'PPOK': 0.39, 'theta': 0.61},
        'G06': {'PPOK': 0.58, 'theta': 0.42},
        'G07': {'PPOK': 0.77, 'theta': 0.23},
        'G08': {'PPOK': 0.96, 'theta': 0.04},
        'G09': {'PPOK': 0.07, 'theta': 0.93},
        'G10': {'PPOK': 0.105, 'theta': 0.895},
        'G11': {'PPOK': 0.035, 'theta': 0.965},
        'G12': {'PPOK': 0.035, 'theta': 0.965},
        'G13': {'PPOK': 0.035, 'theta': 0.965},
        'G14': {'PPOK': 0.035, 'theta': 0.965},
        'G15': {'PPOK': 0.105, 'theta': 0.895},
        'G16': {'PPOK': 0.105, 'theta': 0.895},
        'G17': {'PPOK': 0.105, 'theta': 0.895},
        'G18': {'PPOK': 0.035, 'theta': 0.965},
    }

    symptom_names = {
        'G01': 'Batuk Berdahak > 3 bulan',
        'G02': 'Batuk Kronis > 3 bulan',
        'G03': 'Usia > 45 tahun',
        'G04': 'Sesak saat aktivitas berat',
        'G05': 'Sesak saat naik tangga',
        'G06': 'Berjalan lambat karena sesak',
        'G07': 'Sesak saat berjalan 100m',
        'G08': 'Sesak saat mandi/pakai baju',
        'G09': 'Nyeri di dada',
        'G10': 'Mengi (suara tinggi saat napas)',
        'G11': 'Merasa lelah',
        'G12': 'Penurunan berat badan',
        'G13': 'Aktivitas fisik berkurang',
        'G14': 'Keluar masuk RS dengan keluhan sama',
        'G15': 'Merokok > 15 tahun',
        'G16': 'Kerja di tempat polusi tinggi',
        'G17': 'Tinggal di daerah polusi tinggi',
        'G18': 'Terpapar asap rokok (pasif)',
    }

    possible_hypotheses = set(['PPOK', 'theta'])

    def combine_mass(m1, m2):
        new_mass = {}
        conflict_k = 0
        for h1_str, val1 in m1.items():
            for h2_str, val2 in m2.items():
                h1 = set(h1_str.split(',')) if h1_str != 'theta' else possible_hypotheses
                h2 = set(h2_str.split(',')) if h2_str != 'theta' else possible_hypotheses
                intersection = h1.intersection(h2)
                if not intersection:
                    conflict_k += val1 * val2
                    continue
                new_h_str = ','.join(sorted(list(intersection)))
                if new_h_str == 'PPOK,theta':
                    new_h_str = 'theta'
                new_mass[new_h_str] = new_mass.get(new_h_str, 0) + (val1 * val2)
        if conflict_k == 1:
            st.error("❌ Terjadi konflik total antar bukti.")
            return {'theta': 1.0}
        denominator = 1 - conflict_k
        return {h: val / denominator for h, val in new_mass.items()}

    col1, col2 = st.columns([2, 1])
    with col1:
        nama = st.text_input("Nama Lengkap")
    with col2:
        umur = st.number_input("Umur", min_value=0, max_value=120, step=1)

    st.markdown("### Pilih Gejala yang Kamu Alami:")
    selected_symptoms_map = {}
    cols = st.columns(2)
    items = list(symptom_names.items())
    for i in range(0, len(items), 2):
        code1, name1 = items[i]
        with cols[0]:
            selected_symptoms_map[code1] = st.checkbox(name1)
        if i + 1 < len(items):
            code2, name2 = items[i + 1]
            with cols[1]:
                selected_symptoms_map[code2] = st.checkbox(name2)

    if st.button("💚 Proses Diagnosis"):
        selected_symptoms_list = [code for code, selected in selected_symptoms_map.items() if selected]

        if not nama or umur == 0:
            st.warning("⚠️ Silakan isi nama dan umur terlebih dahulu.")
        elif len(selected_symptoms_list) < 3:
            st.warning("⚠️ Silakan pilih minimal tiga gejala.")
        else:
            result_mass = knowledge_base[selected_symptoms_list[0]]
            for i in range(1, len(selected_symptoms_list)):
                result_mass = combine_mass(result_mass, knowledge_base[selected_symptoms_list[i]])

            belief_ppok = result_mass.get('PPOK', 0)
            belief_theta = result_mass.get('theta', 0)

            st.success("✅ Proses diagnosis selesai.")
            st.metric("Tingkat Keyakinan PPOK", f"{belief_ppok*100:.2f}%")
            st.progress(belief_ppok)

            st.write("### Detail Diagnosis")
            st.info(f"👤 Nama: {nama} | Umur: {umur} tahun")
            st.info(f"🩺 Gejala: {', '.join([symptom_names[c] for c in selected_symptoms_list])}")
            st.info(f"🕒 Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            if belief_ppok >= 0.625:
                st.success("🟢 Terdiagnosa PPOK")
                st.markdown("""
                #### 🌿 Saran:
                - Segera konsultasi ke dokter paru  
                - Berhenti merokok dan hindari polusi  
                - Lakukan latihan pernapasan  
                - Konsumsi makanan bergizi  
                """)
            else:
                st.info("🛡️ Tidak terdiagnosa PPOK")
                st.markdown("""
                #### 🌼 Saran Pencegahan:
                - Hindari asap rokok & debu  
                - Istirahat cukup dan olahraga ringan  
                - Makan bergizi dan banyak minum air putih  
                """)

# ===================== HALAMAN TENTANG =====================
elif menu == "ℹ️ Tentang Aplikasi":
    st.markdown("## ℹ️ Tentang Sistem Pakar PPOK")
    st.write("""
    Aplikasi ini dikembangkan untuk membantu masyarakat mendeteksi dini 
    **Penyakit Paru Obstruktif Kronis (PPOK)** dengan metode **Dempster-Shafer**.

    Versi: 2.0  
    Tahun: 2025  
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/9421/9421093.png", width=200)


