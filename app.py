import streamlit as st

# ==========================================
# 1. KNOWLEDGE BASE & INFERENCE ENGINE
# ==========================================
def cek_aturan(fakta, inferred):
    aturan_terpicu = False

    # ----------------------------------------
    # ATURAN UNTUK PRC (Packed Red Cells)
    # ----------------------------------------
    if fakta["komponen"] == "PRC":
        # Aturan Golongan Darah ABO (PRC)
        if fakta["pasien_abo"] == "O" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["O"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "A" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["A", "O"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "B" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["B", "O"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "AB" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["AB", "A", "B", "O"]
            aturan_terpicu = True

        # Aturan Rhesus (PRC) - Sangat Ketat
        if fakta["pasien_rh"] == "Negatif" and not inferred["donor_rh_valid"]:
            inferred["donor_rh_valid"] = ["Negatif"]
            aturan_terpicu = True
        elif fakta["pasien_rh"] == "Positif" and not inferred["donor_rh_valid"]:
            inferred["donor_rh_valid"] = ["Positif", "Negatif"]
            aturan_terpicu = True

    # ----------------------------------------
    # ATURAN UNTUK FFP (Fresh Frozen Plasma)
    # ----------------------------------------
    elif fakta["komponen"] == "FFP":
        # Aturan Golongan Darah ABO (FFP) - Kebalikan dari PRC
        if fakta["pasien_abo"] == "O" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["O", "A", "B", "AB"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "A" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["A", "AB"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "B" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["B", "AB"]
            aturan_terpicu = True
        elif fakta["pasien_abo"] == "AB" and not inferred["donor_abo_valid"]:
            inferred["donor_abo_valid"] = ["AB"]
            aturan_terpicu = True

        # Aturan Rhesus (FFP) - Bebas / Tidak Terikat Rhesus
        if not inferred["donor_rh_valid"]:
            inferred["donor_rh_valid"] = ["Positif", "Negatif"] # Bisa terima keduanya
            aturan_terpicu = True

    return aturan_terpicu

def jalankan_forward_chaining(fakta):
    inferred = {"donor_abo_valid": [], "donor_rh_valid": []}
    loop_aktif = True
    
    while loop_aktif:
        loop_aktif = cek_aturan(fakta, inferred)
        
    return inferred

# ==========================================
# 2. ANTARMUKA PENGGUNA (UI) STREAMLIT
# ==========================================

st.set_page_config(page_title="BloodBridge", page_icon="🩸")

st.title("🩸 BloodBridge")
st.subheader("Sistem Verifikasi Kompatibilitas Darah Berbasis Pengetahuan")
st.markdown("""
Sistem ini menggunakan metode **Forward Chaining** untuk memverifikasi kompatibilitas donor. 
Aturan (_rules_) yang diterapkan diambil dari pedoman klinis transfusi darah (mencakup perbedaan logika antara antigen seluler dan antibodi plasma).
""")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("### Data Pasien")
    pasien_abo = st.selectbox("Golongan Darah Pasien (ABO):", ["A", "B", "AB", "O"])
    pasien_rh = st.selectbox("Status Rhesus (Rh):", ["Positif", "Negatif"])

with col2:
    st.write("### Kebutuhan Transfusi")
    # Menambahkan FFP ke dalam pilihan dropdown
    komponen = st.selectbox("Jenis Komponen Darah:", ["PRC (Packed Red Cells)", "FFP (Fresh Frozen Plasma)"])

# Ekstraksi kode komponen murni (mengambil 3 huruf pertama)
kode_komponen = komponen.split(" ")[0]

if st.button("Verifikasi Kompatibilitas Donor", type="primary", use_container_width=True):
    
    fakta_awal = {
        "komponen": kode_komponen, 
        "pasien_abo": pasien_abo,
        "pasien_rh": pasien_rh
    }
    
    with st.spinner('Mengevaluasi basis pengetahuan medis...'):
        hasil = jalankan_forward_chaining(fakta_awal)
        
        komponen_valid = []
        for abo in hasil["donor_abo_valid"]:
            for rh in hasil["donor_rh_valid"]:
                komponen_valid.append(f"{abo} {rh}")
    
    st.success("✅ Inferensi Selesai!")
    st.write(f"Pasien dengan profil **{pasien_abo} {pasien_rh}** yang membutuhkan **{kode_komponen}** dapat menerima darah dari donor berikut:")
    
    # Render pill/tag
    html_tags = " ".join([f"<span style='background-color: #ff4b4b; color: white; padding: 5px 10px; border-radius: 15px; margin-right: 5px; font-weight: bold;'>{darah}</span>" for darah in komponen_valid])
    st.markdown(html_tags, unsafe_allow_html=True)

    # Tambahan penjelasan dinamis untuk edukasi
    if kode_komponen == "PRC":
        st.info("💡 **Traceability PRC:** Untuk *Packed Red Cells*, sistem memastikan tidak ada **antigen** asing yang masuk ke tubuh pasien. Rhesus dicocokkan secara ketat.")
    elif kode_komponen == "FFP":
        st.warning("💡 **Traceability FFP:** Untuk *Plasma*, aturan berbalik karena kita mencegah masuknya **antibodi** asing. Faktor Rhesus umumnya tidak memberikan reaksi klinis signifikan pada transfusi FFP sehingga semua Rhesus diizinkan.")