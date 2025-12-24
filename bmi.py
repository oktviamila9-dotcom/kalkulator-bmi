import streamlit as st
from streamlit_option_menu import option_menu

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart BMI Calculator", page_icon="⚖️", layout="centered")

# 2. CSS ANTI-DARK MODE & STYLING (Paling Aman)
st.markdown("""
    <style>
    /* Dasar Putih & Teks Hitam */
    .stApp { background-color: white !important; }
    h1, h2, h3, h4, p, span, label, li, div { color: #000000 !important; }

    /* Container Header (Gambar & Tulisan Sejajar) */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        border: 1px solid #eeeeee;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .header-container img { width: 60px; height: auto; }
    .header-container h2 { margin: 0; font-size: 22px; font-weight: bold; }

    [data-testid="stSidebar"] { display: none; }
    
    /* Tombol Biru */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #007bff;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER (Gambar & Judul Sejajar)
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/3843/3843184.png">
        <h2>Menu Utama</h2>
    </div>
    """, unsafe_allow_html=True)

# 4. MENU NAVIGASI
selected = option_menu(
    menu_title=None, 
    options=["Input Data", "Hasil Perhitungan"],
    icons=['pencil-square', 'activity'],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f8f9fa", "border-radius": "10px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "color": "#333"},
        "nav-link-selected": {"background-color": "#007bff", "color": "white !important"},
    }
)

st.divider()

# --- HALAMAN 1: INPUT DATA ---
if selected == "Input Data":
    st.markdown("<h3 style='text-align: center;'>📝 Form Input Data</h3>", unsafe_allow_html=True)
    
    # Input Vertikal (Tinggi di bawah Berat)
    berat = st.number_input("Berat Badan (kg)", min_value=1.0, value=1.0, step=0.1)
    tinggi = st.number_input("Tinggi Badan (cm)", min_value=1.0, value=1.0, step=0.1)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    
    if st.button("Hitung Sekarang ✨"):
        st.session_state.berat = berat
        st.session_state.tinggi = tinggi
        st.success("✅ Data tersimpan! Klik menu 'Hasil Analisis' di atas.")

# --- HALAMAN 2: HASIL ANALISIS ---
elif selected == "Hasil Perhitungan":
    st.markdown("<h3 style='text-align: center;'>📊 hasil perhitungan BMI</h3>", unsafe_allow_html=True)
    
    if "berat" not in st.session_state:
        st.info("💡 Isi data di 'Input Data' terlebih dahulu.")
    else:
        # Perhitungan Skor
        bmi = st.session_state.berat / ((st.session_state.tinggi / 100) ** 2)
        
        st.markdown(f"""
            <div style="padding:20px; border-radius:15px; background:#ffffff; text-align:center; border:1px solid #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <p style="margin:0; color:#888;">Skor BMI Anda</p>
                <h1 style="margin:0; color:#007bff; font-size:50px;">{bmi:.1f}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Logika Kategori, Risiko, dan Tips
        if bmi < 18.5:
            kat = "Kurus (Underweight)"
            risiko = ["Kekurangan nutrisi", "Sistem imun lemah", "Anemia", "Gangguan kesuburan", "Kepadatan tulang rendah"]
            tips = ["Makan porsi kecil tapi sering", "Tambah asupan protein", "Pilih camilan padat kalori (kacang, alpukat)", "Olahraga angkat beban", "Istirahat cukup"]
        elif 18.5 <= bmi < 25:
            kat = "Normal (Ideal)"
            risiko = ["Risiko penyakit rendah", "Tekanan darah stabil", "Gula darah normal", "Metabolisme lancar", "Jantung sehat"]
            tips = ["Pertahankan pola makan bergizi", "Olahraga 150 menit/minggu", "Minum air putih cukup", "Cek kesehatan rutin", "Kelola stres"]
        elif 25 <= bmi < 30:
            kat = "Gemuk (Overweight)"
            risiko = ["Tekanan darah tinggi", "Kadar kolesterol naik", "Risiko Diabetes tipe 2", "Nyeri sendi lutut", "Gangguan pernapasan"]
            tips = ["Kurangi konsumsi gula & gorengan", "Perbanyak jalan kaki", "Ganti nasi putih ke merah/gandum", "Puasa berkala (intermittent)", "Perbanyak makan sayur"]
        else:
            kat = "Obesitas"
            risiko = ["Serangan jantung/Stroke", "Penyumbatan pembuluh darah", "Sleep apnea (sesak saat tidur)", "Kerusakan hati", "Gagal ginjal"]
            tips = ["Konsultasi dengan dokter", "Defisit kalori secara ketat", "Hindari minuman manis/soda", "Olahraga renang atau jalan cepat", "Cek profil lipid/lemak darah"]

        st.markdown(f"**Kategori: {kat}**")
        st.progress(0.2 if bmi < 18.5 else 0.5 if bmi < 25 else 0.75 if bmi < 30 else 1.0)

        # --- TAMPILAN RISIKO DAN TIPS (DIPISAH) ---
        with st.expander("⚠️ Risiko Kesehatan", expanded=True):
            for r in risiko:
                st.markdown(f"<p style='margin:0; color:black;'>• {r}</p>", unsafe_allow_html=True)

        with st.expander("💡 Tips Kesehatan", expanded=True):
            for t in tips:
                st.markdown(f"<p style='margin:0; color:black;'>• {t}</p>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #ccc; font-size: 10px;'>© 2025 BMI Tracker Pro</p>", unsafe_allow_html=True)