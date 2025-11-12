#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- Konfigurasi Awal ---
st.set_page_config(page_title="Sistem Pakar PPOK", page_icon="🫁", layout="centered")

# --- MODE GELAP / TERANG + ANIMASI ---
st.markdown("""
<style>
body {
    transition: background-color 0.3s ease, color 0.3s ease;
}
[data-testid="stAppViewContainer"] {
    background-color: #f6fcf9;
}
@media (prefers-color-scheme: dark) {
    [data-testid="stAppViewContainer"] {
        background-color: #0c1c17 !important;
        color: #e8f5f2 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #153d33 !important;
    }
}
.result-card {
    animation: fadeInUp 0.7s ease-in-out;
}
@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# --- MENU SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966485.png", width=90)
st.sidebar.title("🧭 Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "🧪 Diagnosis PPOK", "📘 Panduan Penggunaan", "ℹ️ Tentang Aplikasi"]
)

# -------------------- HALAMAN BERANDA --------------------
if menu == "🏠 Beranda":
    st.title("🫁 Sistem Pakar Diagnosis PPOK")
    st.markdown("""
    Selamat datang di **Sistem Pakar Diagnosis Penyakit Paru Obstruktif Kronis (PPOK)**.

    Aplikasi ini menggunakan **metode Dempster-Shafer** untuk membantu menentukan tingkat keyakinan terhadap kemungkinan PPOK berdasarkan gejala yang kamu pilih.

    ---
    🔹 **Gunakan menu di kiri** untuk memulai diagnosis  
    🔹 **Unduh hasil diagnosis** dalam bentuk PDF  
    🔹 **Lihat grafik keyakinan** PPOK secara visual  
    ---
    """)

# -------------------- HALAMAN DIAGNOSIS --------------------
elif menu == "🧪 Diagnosis PPOK":
    st.title("🧪 Diagnosa Penyakit PPOK")
    st.markdown("Masukkan data pasien dan pilih gejala yang sesuai untuk memulai proses diagnosis.")

    # --- Input Pengguna ---
    st.sidebar.header("📋 Data Pasien")
    nama = st.sidebar.text_input("Nama Pasien")
    umur = st.sidebar.number_input("Umur Pasien (tahun)", min_value=1, max_value=120, value=40)

    # Gejala dan Nilai Densitas
    symptom_names = {
        "batuk_kronis": "Batuk Kronis",
        "sesak_napas": "Sesak Napas",
        "dahak_berlebih": "Produksi Dahak Berlebih",
        "riwayat_merokok": "Riwayat Merokok",
        "kehilangan_berat_badan": "Penurunan Berat Badan"
    }

    selected_symptoms_list = st.multiselect(
        "Pilih Gejala yang Dialami:",
        list(symptom_names.keys()),
        format_func=lambda x: symptom_names[x]
    )

    density_values = {
        "batuk_kronis": 0.6,
        "sesak_napas": 0.8,
        "dahak_berlebih": 0.7,
        "riwayat_merokok": 0.9,
        "kehilangan_berat_badan": 0.5
    }

    # --- Proses Diagnosis ---
    if st.button("🔬 Proses Diagnosis"):
        if not selected_symptoms_list:
            st.warning("⚠️ Silakan pilih minimal satu gejala untuk melanjutkan.")
        else:
            progress_text = "Menganalisis gejala pasien..."
            progress_bar = st.progress(0, text=progress_text)

            belief_ppok = 0
            belief_theta = 1

            for i, gejala in enumerate(selected_symptoms_list):
                d = density_values[gejala]
                belief_ppok = belief_ppok + (d * belief_theta)
                belief_theta = belief_theta * (1 - d)
                progress_bar.progress((i + 1) / len(selected_symptoms_list), text=progress_text)

            st.success("✅ Analisis Selesai!")

            # --- Hasil ---
            st.markdown(f"""
            <div class='result-card'>
            <h3>🧾 Hasil Diagnosis:</h3>
            <ul>
            <li><b>Nama Pasien:</b> {nama}</li>
            <li><b>Umur:</b> {umur} tahun</li>
            <li><b>Tingkat Keyakinan PPOK:</b> {belief_ppok*100:.2f}%</li>
            <li><b>Tingkat Ketidaktahuan (Theta):</b> {belief_theta*100:.2f}%</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            # --- Grafik Keyakinan ---
            fig, ax = plt.subplots()
            ax.bar(["PPOK", "Ketidaktahuan"], [belief_ppok * 100, belief_theta * 100])
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Visualisasi Keyakinan Diagnosis")
            st.pyplot(fig)

            # --- Unduh PDF ---
            if st.button("📄 Unduh Hasil Diagnosis (PDF)"):
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(180, 800, "HASIL DIAGNOSIS PPOK")
                c.setFont("Helvetica", 12)
                c.drawString(50, 770, f"Nama: {nama}")
                c.drawString(50, 750, f"Umur: {umur} tahun")
                c.drawString(50, 730, f"Tingkat Keyakinan PPOK: {belief_ppok*100:.2f}%")
                c.drawString(50, 710, f"Ketidaktahuan (Theta): {belief_theta*100:.2f}%")
                c.drawString(50, 690, "Gejala yang dipilih:")
                y = 670
                for g in selected_symptoms_list:
                    c.drawString(70, y, f"- {symptom_names[g]}")
                    y -= 20
                c.drawString(50, y-10, f"Waktu Diagnosis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                c.showPage()
                c.save()
                buffer.seek(0)
                st.download_button(
                    label="⬇️ Simpan Hasil Sebagai PDF",
                    data=buffer,
                    file_name=f"Hasil_Diagnosis_{nama}.pdf",
                    mime="application/pdf"
                )

            # --- Pesan Penutup ---
            st.markdown("---")
            st.markdown("""
            <div style="text-align:center; font-size:14px; color:#49796b;">
            🌿 <i>“Menjaga paru-paru berarti menjaga hidup. Mulailah dari hari ini.”</i> 🌿
            </div>
            """, unsafe_allow_html=True)

# -------------------- HALAMAN PANDUAN --------------------
elif menu == "📘 Panduan Penggunaan":
    st.title("📘 Panduan Penggunaan")
    st.markdown("""
    **Langkah-langkah Menggunakan Aplikasi:**
    1. Pilih menu **Diagnosis PPOK** di sidebar.  
    2. Masukkan nama dan umur pasien.  
    3. Centang gejala-gejala yang sesuai.  
    4. Klik **Proses Diagnosis** untuk mendapatkan hasil.  
    5. Lihat grafik hasil dan unduh PDF jika diperlukan.  
    """)

# -------------------- HALAMAN TENTANG --------------------
elif menu == "ℹ️ Tentang Aplikasi":
    st.title("ℹ️ Tentang Aplikasi Ini")
    st.markdown("""
    Aplikasi ini dikembangkan untuk membantu analisis awal terhadap kemungkinan **Penyakit Paru Obstruktif Kronis (PPOK)**.  
    Metode yang digunakan: **Dempster-Shafer Evidence Theory**.  

    **Tujuan:**  
    🔹 Membantu tenaga medis dalam skrining awal PPOK.  
    🔹 Memberikan informasi visual dan terukur mengenai tingkat keyakinan diagnosis.  

    ---
    👨‍💻 Pengembang: *Tim Sistem Pakar Paru 2025*  
    🏫 Dibuat untuk penelitian dan edukasi.  
    """)
