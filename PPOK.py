#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from datetime import datetime

# ---------------- Page Configuration ----------------
st.set_page_config(page_title="Sistem Pakar PPOK", page_icon="🫁", layout="wide")

# ---------------- Sidebar ----------------
st.markdown("""
<style>
/* Sidebar area */
[data-testid="stSidebar"] {
    background-color: #e8f5f2; /* warna hijau lembut */
    padding: 2rem 1.5rem;
    width: 270px !important;
}

/* Logo dan judul */
.sidebar-title {
    text-align: center;
    font-weight: 700;
    font-size: 18px;
    color: #0f5132;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

.sidebar-logo {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: radial-gradient(circle, #8fd3c8 0%, #4ca98a 100%);
}

/* Navigasi radio button */
[data-testid="stSidebar"] [role="radiogroup"] {
    margin-top: 1rem;
}

[data-testid="stSidebar"] label {
    font-size: 15px;
    font-weight: 500;
    color: #084c61;
    padding: 6px 10px;
    border-radius: 10px;
    margin-bottom: 6px;
    transition: all 0.2s ease-in-out;
}

[data-testid="stSidebar"] label:hover {
    background-color: #d9f0ea;
    color: #05668d;
    transform: translateX(5px);
}

[data-testid="stSidebar"] div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
    background-color: #b5e5d6 !important;
    font-weight: 600 !important;
    color: #063c32 !important;
}

/* Footer text */
.sidebar-footer {
    font-size: 12px;
    color: #49796b;
    text-align: center;
    margin-top: 2rem;
    border-top: 1px solid #aac7b4;
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown('<div class="sidebar-logo"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Sistem Pakar<br>Penyakit Paru Obstruktif Kronis</div>', unsafe_allow_html=True)
    menu = st.radio("Navigasi", ["🏠 Dashboard", "🩺 Diagnosis PPOK", "ℹ️ Tentang Aplikasi"])
    st.markdown("""
    <div class="sidebar-footer">
    © 2025 Sistem Pakar PPOK <br>by <b>Rahma Yuliana</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Knowledge Base ----------------
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
    'G01': 'Batuk berdahak > 3 bulan',
    'G02': 'Batuk kronis > 3 bulan',
    'G03': 'Usia > 45 tahun',
    'G04': 'Sesak saat aktivitas berat',
    'G05': 'Sesak saat naik tangga',
    'G06': 'Berjalan lambat karena sesak',
    'G07': 'Mulai sesak saat berjalan 100 meter',
    'G08': 'Sesak saat mandi atau saat berpakaian',
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

# ---------------- Dempster-Shafer Function ----------------
def combine_mass(m1, m2):
    new_mass = {}
    conflict_k = 0.0
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
            new_mass[new_h_str] = new_mass.get(new_h_str, 0.0) + (val1 * val2)
    if abs(conflict_k - 1.0) < 1e-12:
        st.error("❌ Terjadi konflik total antar bukti.")
        return {'theta': 1.0}
    denominator = 1.0 - conflict_k
    if denominator == 0:
        return {'theta': 1.0}
    return {h: (val / denominator) for h, val in new_mass.items()}

# ---------------- Halaman ----------------
if menu == "🏠 Dashboard":
    st.markdown("""
    <style>
    .header-container {
        position: relative;
        background-image: url('https://akcdn.detik.net.id/visual/2019/10/03/c33549d5-78a2-494d-ad14-7c1ed37c36bb_169.jpeg?w=1200');
        background-size: cover;
        background-position: center;
        border-radius: 18px;
        overflow: hidden;
        height: 230px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 30px;
        animation: fadeIn 1s ease-in-out;
    }

    .header-overlay {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 40, 30, 0.45);
        backdrop-filter: blur(2px);
        z-index: 1;
    }

    .header-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: #ffffff;
        padding-top: 60px;
    }

    .header-content h1 {
        font-size: 2.2em;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }

    .header-content p {
        font-size: 1.05em;
        font-weight: 400;
        color: #e6f5ef;
        margin-top: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="header-container">
        <div class="header-overlay"></div>
        <div class="header-content">
            <h1>Selamat Datang di Sistem Pakar Diagnosis PPOK</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("""
    Sistem ini membantu mendiagnosis **Penyakit Paru Obstruktif Kronis (PPOK)** 
    berdasarkan gejala yang dialami pengguna menggunakan metode **Dempster-Shafer**.
    """)

    st.markdown("### Fitur Utama:")
    st.markdown("""
    - Form input pengguna & gejala interaktif  
    - Proses diagnosis otomatis  
    - Tingkat keyakinan hasil dalam persentase  
    - Saran kesehatan dan pencegahan
    """)

    st.markdown("---")
    st.markdown("### Apa itu PPOK?")
    st.write("""
    **Penyakit Paru Obstruktif Kronis (PPOK)** adalah penyakit paru jangka panjang 
    yang menyebabkan hambatan aliran udara dan kesulitan bernapas. 
    Penyebab utama PPOK adalah **merokok**, paparan polusi udara, dan bahan kimia berbahaya. 
    Penyakit ini bersifat **kronis dan progresif**, artinya gejala dapat memburuk seiring waktu 
    bila tidak ditangani dengan baik.
    """)
    # Tambah gambar ke halaman Tentang Aplikasi
    st.image("https://my.clevelandclinic.org/-/scassets/images/org/health/articles/8709-copd.jpg", 
         caption="Ciri-ciri PPOK meliputi hilangnya elastisitas, saluran napas meradang dan menyempit, alveoli membesar dan rusak, serta lendir kental.", 
         use_column_width=True)


    st.markdown("### Tips Pencegahan:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🚭 **Berhenti Merokok**\n\nLangkah paling efektif mencegah PPOK.")
    with col2:
        st.markdown("😷 **Hindari Polusi Udara**\n\nGunakan masker di area berasap atau berdebu.")
    with col3:
        st.markdown("🏃 **Jaga Kesehatan Paru**\n\nLakukan olahraga ringan dan konsumsi makanan bergizi.")

    st.markdown("---")
    if st.button("🩺 Mulai Diagnosis Sekarang"):
        st.session_state.menu = "🩺 Diagnosis PPOK"
        st.success("Silakan klik menu '🩺 Diagnosis PPOK' di sidebar untuk melanjutkan diagnosis.")

elif menu == "🩺 Diagnosis PPOK":
    st.markdown("## Formulir Diagnosis PPOK")
    st.markdown('<div class="sub-text">Isi data diri lalu pilih minimal 3 gejala untuk melakukan proses diagnosis.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        nama = st.text_input("Nama Lengkap")
        st.markdown("### Pilih Gejala yang Kamu Alami:")
        selected_symptoms_map = {}
        cols = st.columns(2)
        items = list(symptom_names.items())
        for i in range(0, len(items), 2):
            code1, name1 = items[i]
            with cols[0]:
                selected_symptoms_map[code1] = st.checkbox(name1, key=code1)
            if i + 1 < len(items):
                code2, name2 = items[i + 1]
                with cols[1]:
                    selected_symptoms_map[code2] = st.checkbox(name2, key=code2)
    with col_right:
        umur = st.number_input("Umur", min_value=0, max_value=120, step=1)
        st.markdown("### Info Singkat")
        st.markdown("- Minimal tiga gejala untuk proses valid")
        st.markdown("- Hasil bersifat indikatif, bukan diagnosis dokter")

    if st.button("Proses Diagnosis"):
        selected = [code for code, sel in selected_symptoms_map.items() if sel]

        if not nama or umur == 0:
            st.warning("⚠️ Silakan isi nama dan umur terlebih dahulu.")
        elif len(selected) < 3:
            st.warning("⚠️ Silakan pilih minimal tiga gejala.")
        else:
            result_mass = knowledge_base[selected[0]].copy()
            for code in selected[1:]:
                result_mass = combine_mass(result_mass, knowledge_base[code])

            belief_ppok = result_mass.get('PPOK', 0.0)
            belief_theta = result_mass.get('theta', 0.0)

            st.metric("Tingkat Keyakinan PPOK", f"{belief_ppok*100:.2f}%")
            st.progress(belief_ppok)
            st.metric("Ketidaktahuan (Theta)", f"{belief_theta*100:.2f}%")
            st.progress(belief_theta)

            st.info(f"👤 Nama: {nama} | Umur: {umur} tahun n/ 🩺 Gejala: " + ", ".join([symptom_names[c] for c in selected]) n/ 🕒 Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            if belief_ppok >= 0.625:
                st.success("🟢 Indikasi PPOK tinggi — segera konsultasikan ke dokter spesialis paru.")
                st.markdown("""
                #### Saran:
                - Berhenti merokok dan hindari polusi udara  
                - Lakukan latihan pernapasan ringan & olahraga teratur  
                - Konsultasikan ke dokter paru untuk pemeriksaan lanjutan
                """)
            else:
                st.info("🛡️ Indikasi PPOK rendah atau tidak cukup bukti.")
                st.markdown("""
                #### Saran Pencegahan:
                - Hindari paparan asap rokok & polusi  
                - Jaga kebugaran dan konsumsi makanan bergizi  
                - Periksa ke fasilitas kesehatan jika gejala berlanjut
                """)

elif menu == "ℹ️ Tentang Aplikasi":
    st.markdown("## Tentang Sistem Pakar PPOK")
    st.write("""
    Aplikasi ini dirancang untuk membantu deteksi dini Penyakit Paru Obstruktif Kronis (PPOK)
    menggunakan metode **Dempster-Shafer**.  
    Hasil yang ditampilkan bersifat **indikatif** dan tidak menggantikan diagnosis medis profesional.
    """)
    st.markdown("**Dibangun dengan:** Python & Streamlit — oleh **Rahma Yuliana**")
