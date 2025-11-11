#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from datetime import datetime

# ===================== KONFIGURASI HALAMAN =====================
st.set_page_config(
    page_title="🫁 Sistem Pakar PPOK",
    page_icon="🫁",
    layout="wide"
)

# ===================== CSS KHUSUS (TEMA PASTEL) =====================
st.markdown("""
<style>
/* Background dan warna utama */
body {
    background-color: #f4f9f9;
    font-family: 'Poppins', sans-serif;
    color: #003366;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #e0f7f4 !important;
    color: #004c4c;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #005f5f;
}

/* Tombol */
div.stButton > button:first-child {
    background-color: #68c4af;
    color: white;
    border-radius: 12px;
    border: none;
    height: 3em;
    width: 100%;
    font-size: 1em;
    transition: 0.3s;
}
div.stButton > button:first-child:hover {
    background-color: #47a690;
    transform: scale(1.03);
}

/* Kotak hasil diagnosis */
.stSuccess, .stInfo, .stWarning {
    border-radius: 12px;
    padding: 15px;
}

/* Metric styling */
[data-testid="stMetric"] {
    background-color: #f0faf9;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* Heading */
h2, h3, h4 {
    color: #007b83;
}
</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR NAVIGASI =====================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3177/3177440.png", width=100)
st.sidebar.title("🫁 Sistem Pakar Penyakit Paru Obstruktif Kronis")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "🩺 Diagnosis PPOK", "ℹ️ Tentang Aplikasi"]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Sistem Pakar PPOK | by Rahma Yuliana")

# ===================== HALAMAN DASHBOARD =====================
if menu == "🏠 Dashboard":
    st.markdown("<h2 style='color:#007b83;'>Selamat Datang di Sistem Pakar Diagnosis PPOK</h2>", unsafe_allow_html=True)
    st.markdown("""
    Sistem ini membantu pengguna mendiagnosis **Penyakit Paru Obstruktif Kronis (PPOK)** 
    berdasarkan gejala yang dialami menggunakan metode **Dempster-Shafer**.

    ### 💡 Fitur Utama:
    - Form input pengguna & gejala interaktif  
    - Proses diagnosis otomatis  
    - Tingkat keyakinan hasil dalam bentuk persentase  
    - Saran kesehatan dan pencegahan

    💚 Klik menu **Diagnosis PPOK** di sebelah kiri untuk memulai pemeriksaan.
    """)
    st.image("https://img.freepik.com/free-vector/doctor-examining-patient-with-lung-disease_74855-19635.jpg", use_column_width=True)

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


