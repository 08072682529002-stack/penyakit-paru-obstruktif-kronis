#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Sistem Pakar PPOK", page_icon="🫁", layout="wide")

# Sidebar
st.markdown(
    """
    <style>
    /* Body */
    body { background-color: #f7fbfb; color: #00343a; font-family: "Inter", "Poppins", sans-serif; }

    /* Perlebar sidebar dan beri padding */
    [data-testid="stSidebar"] {
        width: 300px !important;
        background-color: #e8f6f3;
        padding-top: 28px;
        padding-left: 26px;
        padding-right: 26px;
    }

    /* Icon/user avatar area */
    .sidebar-avatar {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }
    .avatar-circle {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #9be7d0, #6cc1a5);
        display: inline-block;
    }
    .sidebar-title { font-weight: 700; color: #0a5957; margin: 0; font-size: 16px; line-height: 1.1; }

    /* Sidebar links spacing */
    .sidebar-links a {
        display: block;
        padding: 10px 6px;
        margin-bottom: 6px;
        border-radius: 8px;
        color: #054b49;
        text-decoration: none;
        font-size: 15px;
    }
    .sidebar-links a:hover {
        background-color: rgba(5,75,73,0.06);
        color: #023a39;
    }

    /* Main headings */
    .main-title { color: #006e6a; font-size: 32px; font-weight: 700; margin-bottom: 6px; }
    .sub-text { color: #2b4d4b; font-size: 15px; margin-bottom: 20px; }

    /* Feature list */
    .feature-list { margin-left: 18px; line-height: 1.8; font-size: 15px; }

    /* Card style for diagnosis results */
    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 10px rgba(3, 22, 18, 0.03);
        margin-top: 12px;
    }

    /* Make checkbox label spacing nicer */
    .stCheckbox label { line-height: 1.6; font-size: 15px; }

    /* Button style */
    div.stButton > button {
        background-color: #68c4af;
        color: white;
        border-radius: 10px;
        height: 40px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #4aa58f;
    }

    /* Small responsive fix */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] { width: 100% !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-avatar">
            <div class="avatar-circle"></div>
            <div>
                <p class="sidebar-title">🫁 Sistem Pakar<br>Penyakit Paru Obstruktif Kronis</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Use a radio for menu selection but show nicer links in HTML for spacing
    menu = st.radio(
        "Navigasi",
        ("🏠 Dashboard", "🩺 Diagnosis PPOK", "ℹ️ Tentang Aplikasi"),
        index=0,
    )

    st.markdown("---")
    st.caption("© 2025 Sistem Pakar PPOK | by Rahma Yuliana")

# ---------------- Knowledge base (unchanged) ----------------
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

# ---------------- Dempster-Shafer combine function ----------------
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
        # very high conflict — fallback to ignorance
        return {'theta': 1.0}
    return {h: (val / denominator) for h, val in new_mass.items()}

# ---------------- Pages ----------------
if menu == "🏠 Dashboard":
    st.markdown("## Selamat Datang di Sistem Pakar Diagnosis PPOK")
    st.write(
        "Sistem ini membantu mendiagnosis **Penyakit Paru Obstruktif Kronis (PPOK)** "
        "berdasarkan gejala yang dialami pengguna menggunakan metode **Dempster-Shafer**."
    )

    st.markdown("### ✨ Fitur Utama:")
    st.markdown("""
    - Form input pengguna & gejala interaktif  
    - Proses diagnosis otomatis menggunakan teori bukti  
    - Tingkat keyakinan hasil ditampilkan dalam persentase  
    - Saran kesehatan dan pencegahan
    """)

    # Penjelasan tambahan tentang PPOK
    st.markdown("---")
    st.markdown("### 🫁 Apa itu PPOK?")
    st.write("""
    **Penyakit Paru Obstruktif Kronis (PPOK)** adalah penyakit paru jangka panjang yang menyebabkan
    hambatan aliran udara dan kesulitan bernapas.  
    Penyebab utama PPOK adalah **merokok**, paparan polusi udara, dan bahan kimia berbahaya.
    Penyakit ini bersifat **kronis dan progresif**, artinya gejala dapat memburuk seiring waktu
    bila tidak ditangani dengan baik.
    """)

    # Tips Pencegahan
    st.markdown("### 💡 Tips Pencegahan:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🚭 **Berhenti Merokok**\n\nLangkah paling efektif mencegah PPOK.")
    with col2:
        st.markdown("😷 **Hindari Polusi Udara**\n\nGunakan masker di area berasap atau berdebu.")
    with col3:
        st.markdown("🏃 **Jaga Kesehatan Paru**\n\nLakukan olahraga ringan dan konsumsi makanan bergizi.")

    st.markdown("---")
    # Tombol navigasi manual
    if st.button("🩺 Mulai Diagnosis Sekarang"):
        st.session_state.menu = "🩺 Diagnosis PPOK"
        st.success("Silakan klik menu '🩺 Diagnosis PPOK' di sidebar untuk melanjutkan diagnosis.")

elif menu == "🩺 Diagnosis PPOK":
    st.markdown("## 🩺 Halaman Diagnosis PPOK")
    st.write("Form diagnosis akan ditampilkan di sini...")

elif menu == "ℹ️ Tentang Aplikasi":
    st.markdown("## ℹ️ Tentang Aplikasi")
    st.write("Aplikasi ini dibuat untuk membantu pengguna mendiagnosis PPOK secara dini.")



elif menu == "🩺 Diagnosis PPOK":
    st.markdown('<div class="main-title">Form Diagnosis PPOK</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Isi data lalu pilih minimal 3 gejala untuk melakukan proses diagnosis.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        nama = st.text_input("Nama Lengkap")
        # Display checkboxes in two columns
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
        selected_symptoms_list = [code for code, sel in selected_symptoms_map.items() if sel]

        if not nama or umur == 0:
            st.warning("⚠️ Silakan isi nama dan umur terlebih dahulu.")
        elif len(selected_symptoms_list) < 3:
            st.warning("⚠️ Silakan pilih minimal tiga gejala.")
        else:
            # Start combining masses
            result_mass = knowledge_base[selected_symptoms_list[0]].copy()
            for code in selected_symptoms_list[1:]:
                result_mass = combine_mass(result_mass, knowledge_base[code])

            belief_ppok = result_mass.get('PPOK', 0.0)
            belief_theta = result_mass.get('theta', 0.0)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Tingkat Keyakinan PPOK", f"{belief_ppok*100:.2f}%")
            st.progress(belief_ppok)
            st.metric("Ketidaktahuan (Theta)", f"{belief_theta*100:.2f}%")
            st.progress(belief_theta)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### Detail Diagnosis")
            st.info(f"👤 Nama: {nama} | Umur: {umur} tahun")
            st.info("🩺 Gejala: " + ", ".join([symptom_names[c] for c in selected_symptoms_list]))
            st.info(f"🕒 Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            if belief_ppok >= 0.625:
                st.success("🟢 Indikasi PPOK tinggi — segera konsultasikan ke dokter spesialis paru.")
                st.markdown(
                    """
                    #### Saran:
                    - Berhenti merokok dan hindari polusi udara  
                    - Lakukan latihan pernapasan ringan & olah raga teratur  
                    - Konsultasikan ke dokter paru untuk pemeriksaan lanjutan  
                    """
                )
            else:
                st.info("🛡️ Indikasi PPOK rendah atau tidak cukup bukti.")
                st.markdown(
                    """
                    #### Saran Pencegahan:
                    - Hindari paparan asap rokok & polusi  
                    - Jaga kebugaran dan konsumsi makanan bergizi  
                    - Periksa ke fasilitas kesehatan jika gejala berlanjut  
                    """
                )

elif menu == "ℹ️ Tentang Aplikasi":
    st.markdown('<div class="main-title">Tentang Sistem Pakar PPOK</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Aplikasi ini dirancang untuk membantu deteksi dini Penyakit Paru Obstruktif Kronis (PPOK)
        menggunakan metode Dempster-Shafer. Hasil yang ditampilkan adalah indikatif dan tidak
        menggantikan diagnosis langsung dari tenaga medis profesional.
        """
    )
    st.markdown("**Dibangun dengan**: Python & Streamlit")

