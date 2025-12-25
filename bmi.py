import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart BMI Calculator", page_icon="⚖️", layout="centered")

# 2. Inisialisasi Status Halaman
if 'step' not in st.session_state:
    st.session_state.step = "input"

# 3. CSS CUSTOM
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    h1, h2, h3, h4, p, span, label, li, div { color: #000000 !important; }

    .header-box {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        margin-bottom: 25px;
    }
    .header-box img { width: 60px; height: auto; }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #007bff;
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px;
    }
    
    .quote-box {
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        background-color: #f0f7ff;
        font-style: italic;
        margin-bottom: 20px;
    }

    .bmi-bar-container {
        width: 100%;
        background-color: #eee;
        border-radius: 10px;
        height: 12px;
        display: flex;
        overflow: hidden;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HALAMAN 1: INPUT DATA ---
if st.session_state.step == "input":
    st.markdown("""
        <div class="header-box">
            <img src="https://cdn-icons-png.flaticon.com/512/3843/3843184.png">
            <div>
                <h2 style="margin:0;">Smart BMI Tracker</h2>
                <p style="margin:0; font-size:14px; color:#666 !important;">Analisis tubuh Anda secara instan</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container(border=True):
        berat = st.number_input("Berat Badan (kg)", min_value=1.0, value=60.0, step=0.1)
        tinggi = st.number_input("Tinggi Badan (cm)", min_value=1.0, value=160.0, step=0.1)
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        
        st.write("")
        if st.button("Hitung Sekarang ✨"):
            st.session_state.berat = berat
            st.session_state.tinggi = tinggi
            st.session_state.step = "hasil"
            st.rerun()

# --- HALAMAN 2: HASIL ---
elif st.session_state.step == "hasil":
    st.markdown("""
        <div class="header-box">
            <img src="https://cdn-icons-png.flaticon.com/512/3843/3843204.png">
            <h2 style="margin:0;">Hasil Analisis</h2>
        </div>
        """, unsafe_allow_html=True)
    
    tinggi_m = st.session_state.tinggi / 100
    bmi = st.session_state.berat / (tinggi_m ** 2)
    berat_min = 18.5 * (tinggi_m ** 2)
    berat_max = 24.9 * (tinggi_m ** 2)
    air_minum = st.session_state.berat * 0.033
    
    # Kotak Skor Utama
    st.markdown(f"""
        <div style="padding:25px; border-radius:20px; background:#ffffff; text-align:center; border:1px solid #eee; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 25px;">
            <p style="margin:0; color:#888; font-weight:500;">Skor BMI Anda</p>
            <h1 style="margin:0; color:#007bff; font-size:65px;">{bmi:.1f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Dashboard Angka Ideal
    m1, m2 = st.columns(2)
    m1.metric("Kebutuhan Air", f"{air_minum:.1f} L/Hari")
    m2.metric("Rentang Ideal", f"{berat_min:.0f}-{berat_max:.0f} kg")

    # Logika Kategori (Risiko/Manfaat & Tips 5 Poin)
    is_normal = False
    if bmi < 18.5:
        kat, color, bar_w = "Underweight", "#f39c12", "20%"
        msg = f"Anda perlu naik sekitar **{berat_min - st.session_state.berat:.1f} kg** untuk ideal."
        quote = "Jangan cuma asal makan! Fokus pada nutrisi berkualitas agar tubuhmu jadi lebih berisi, kuat, dan bertenaga!"
        info_list = ["Sistem imun tubuh melemah", "Risiko anemia & kurang darah", "Kepadatan tulang menurun", "Gangguan pertumbuhan rambut/kuku", "Mudah merasa lelah & lemas"]
        tips = ["Tambah asupan protein & karbo", "Makan porsi kecil namun sering", "Konsumsi camilan sehat (kacang/buah)", "Latihan beban untuk masa otot", "Pastikan istirahat cukup 7-8 jam"]
        
    elif 18.5 <= bmi < 25:
        kat, color, bar_w = "Normal (Ideal)", "#27ae60", "50%"
        is_normal = True
        st.balloons()
        msg = "Selamat! Berat badan Anda sudah berada di titik **Sangat Ideal**."
        quote = "Mempertahankan itu hebat! Pertahankan pola hidup sehatmu sebagai investasi jangka panjang!"
        info_list = ["Kinerja jantung lebih efisien", "Kualitas tidur lebih nyenyak", "Risiko penyakit kronis sangat rendah", "Metabolisme tubuh sangat lancar", "Mood lebih stabil & ceria"]
        tips = ["Jaga pola makan gizi seimbang", "Olahraga rutin 150 menit/minggu", "Cukupi hidrasi air putih harian", "Kelola stres dengan meditasi", "Cek kesehatan secara berkala"]
        
    elif 25 <= bmi < 30:
        kat, color, bar_w = "Overweight", "#2980b9", "75%"
        msg = f"Anda perlu turun sekitar **{st.session_state.berat - berat_max:.1f} kg** untuk ideal."
        quote = "Nggak perlu drastis, yang penting rutin! Setiap pilihan sehatmu hari ini adalah langkah nyata menuju badan ideal!"
        info_list = ["Tekanan darah mulai meningkat", "Beban berlebih pada sendi lutut", "Risiko kolesterol tinggi", "Napas terasa lebih pendek", "Mudah lelah saat beraktivitas"]
        tips = ["Kurangi asupan gula & gorengan", "Jalan kaki minimal 10.000 langkah", "Perbanyak serat dari sayuran", "Hindari makan sebelum tidur", "Lakukan intermittent fasting"]
        
    else:
        kat, color, bar_w = "Obesitas", "#e74c3c", "100%"
        msg = f"Turunkan minimal **{st.session_state.berat - berat_max:.1f} kg** demi kesehatan."
        quote = "Jangan lihat jauhnya, mulai saja dulu! Setiap perubahan kecil adalah kemenangan untuk kesehatanmu di masa depan!"
        info_list = ["Risiko serangan jantung & stroke", "Gangguan napas saat tidur", "Diabetes melitus tipe 2", "Masalah mobilitas & pergerakan", "Beban organ dalam terlalu berat"]
        tips = ["Konsultasi dengan ahli gizi", "Terapkan defisit kalori disiplin", "Olahraga ringan rendah benturan", "Hapus makanan olahan (junk food)", "Siapkan jadwal makan yang ketat"]

    # Bar Visual & Status
    
    st.write(f"**Status: <span style='color:{color}'>{kat}</span>**", unsafe_allow_html=True)
    st.markdown(f'<div class="bmi-bar-container"><div style="width: {bar_w}; background-color: {color}; transition: width 1s;"></div></div>', unsafe_allow_html=True)
    
    st.info(msg)
    st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)

    # Info Detail (Expander)
    c1, c2 = st.columns(2)
    with c1:
        header = "✨ Manfaat Tubuh Ideal" if is_normal else "⚠️ Risiko Kesehatan"
        with st.expander(header, expanded=True):
            for item in info_list: st.write(f"• {item}")
    with c2:
        with st.expander("💡 Tips Langkah Sehat", expanded=True):
            for t in tips: st.write(f"• {t}")

    st.divider()

    # Tombol Reset
    if st.button("⬅️ Hitung Ulang Data Baru"):
        st.session_state.step = "input"
        st.rerun()

st.markdown("<p style='text-align: center; color: #bbb; font-size: 11px; margin-top:50px;'>© 2025 Smart BMI Tracker Pro</p>", unsafe_allow_html=True)