import streamlit as st
from streamlit_option_menu import option_menu

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart BMI Calculator", page_icon="⚖️", layout="centered")

# 2. CSS ANTI-DARK MODE & STYLING
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    h1, h2, h3, h4, p, span, label, li, div { color: #000000 !important; }

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
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #007bff;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
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
    
    berat = st.number_input("Berat Badan (kg)", min_value=1.0, value=60.0, step=0.1)
    tinggi = st.number_input("Tinggi Badan (cm)", min_value=1.0, value=165.0, step=0.1)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    
    if st.button("Hitung Sekarang ✨"):
        st.session_state.berat = berat
        st.session_state.tinggi = tinggi
        st.session_state.gender = gender
        st.success("✅ Data tersimpan! Silakan klik menu 'Hasil Perhitungan' di atas.")

# --- HALAMAN 2: HASIL ANALISIS ---
elif selected == "Hasil Perhitungan":
    st.markdown("<h3 style='text-align: center;'>📊 Hasil Perhitungan BMI</h3>", unsafe_allow_html=True)
    
    if "berat" not in st.session_state:
        st.info("💡 Isi data di menu 'Input Data' terlebih dahulu.")
    else:
        # Perhitungan Skor BMI
        tinggi_m = st.session_state.tinggi / 100
        bmi = st.session_state.berat / (tinggi_m ** 2)
        
        # Hitung Batas Berat Ideal (BMI 18.5 - 24.9)
        berat_ideal_min = 18.5 * (tinggi_m ** 2)
        berat_ideal_max = 24.9 * (tinggi_m ** 2)
        
        # Display Skor BMI
        st.markdown(f"""
            <div style="padding:20px; border-radius:15px; background:#ffffff; text-align:center; border:1px solid #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <p style="margin:0; color:#888;">Skor BMI Anda</p>
                <h1 style="margin:0; color:#007bff; font-size:50px;">{bmi:.1f}</h1>
            </div>
        """, unsafe_allow_html=True)

        # Logika Kategori & Saran Berat
        label_risiko = "⚠️ Risiko Kesehatan"
        
        if bmi < 18.5:
            kat = "Kurus (Underweight)"
            selisih = berat_ideal_min - st.session_state.berat
            st.warning(f"⚠️ **Target:** Anda perlu menaikkan berat badan sekitar **{selisih:.1f} kg** untuk mencapai berat ideal ({berat_ideal_min:.1f} kg).")
            risiko = ["Kekurangan nutrisi", "Sistem imun lemah", "Anemia", "Kepadatan tulang rendah"]
            tips = ["Makan porsi kecil tapi sering", "Tambah asupan protein", "Pilih camilan padat kalori", "Olahraga angkat beban"]
            color_bar = 0.2
            
        elif 18.5 <= bmi < 25:
            kat = "Normal (Ideal)"
            st.success(f"🌟 **Hebat!** Berat badan Anda sudah ideal. Pertahankan di rentang **{berat_ideal_min:.1f} kg - {berat_ideal_max:.1f} kg**.")
            label_risiko = "✅ Manfaat Tubuh Ideal"
            risiko = ["Stamina lebih tinggi", "Kualitas tidur lebih baik", "Jantung lebih kuat", "Metabolisme sangat optimal"]
            tips = ["Pertahankan pola makan bergizi", "Olahraga 150 menit/minggu", "Cek kesehatan rutin", "Minum air putih cukup"]
            color_bar = 0.5
            
        elif 25 <= bmi < 30:
            kat = "Gemuk (Overweight)"
            selisih = st.session_state.berat - berat_ideal_max
            st.info(f"ℹ️ **Target:** Anda perlu menurunkan berat badan sekitar **{selisih:.1f} kg** untuk mencapai berat ideal ({berat_ideal_max:.1f} kg).")
            risiko = ["Tekanan darah tinggi", "Kadar kolesterol naik", "Risiko Diabetes tipe 2", "Nyeri sendi"]
            tips = ["Kurangi gula & gorengan", "Perbanyak jalan kaki", "Ganti karbohidrat ke serat", "Puasa berkala (Intermittent Fasting)"]
            color_bar = 0.75
            
        else:
            kat = "Obesitas"
            selisih = st.session_state.berat - berat_ideal_max
            st.error(f"🚨 **Target Kritis:** Anda harus menurunkan minimal **{selisih:.1f} kg** untuk keluar dari zona obesitas.")
            risiko = ["Serangan jantung/Stroke", "Penyumbatan pembuluh darah", "Sleep apnea", "Gagal ginjal"]
            tips = ["Konsultasi dengan dokter/ahli gizi", "Defisit kalori secara ketat", "Olahraga rendah benturan (renang)", "Hindari minuman manis total"]
            color_bar = 1.0

        # Tampilan Kategori & Progress Bar
        st.markdown(f"**Kategori Saat Ini: {kat}**")
        st.progress(color_bar)

        # Tampilan Detail Risiko dan Tips dalam Expander
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander(label_risiko, expanded=True):
                for r in risiko:
                    st.markdown(f"<p style='margin:0; font-size:13px;'>• {r}</p>", unsafe_allow_html=True)
        
        with col2:
            with st.expander("💡 Tips Kesehatan", expanded=True):
                for t in tips:
                    st.markdown(f"<p style='margin:0; font-size:13px;'>• {t}</p>", unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align: center; color: #ccc; font-size: 10px;'>© 2025 BMI Tracker Pro</p>", unsafe_allow_html=True)