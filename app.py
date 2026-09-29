import streamlit as st
from html import escape


# ==========================================
# 1. BASIS PENGETAHUAN
# ==========================================

ABO_RULES = {
    "PRC": {
        "O": ["O"],
        "A": ["A", "O"],
        "B": ["B", "O"],
        "AB": ["AB", "A", "B", "O"],
    },
    "FFP": {
        "O": ["O", "A", "B", "AB"],
        "A": ["A", "AB"],
        "B": ["B", "AB"],
        "AB": ["AB"],
    },
}


# ==========================================
# 2. MESIN INFERENSI
# ==========================================

def cek_aturan(fakta, inferred):
    aturan_terpicu = False

    # Terapkan aturan ABO jika belum diperoleh.
    if not inferred["donor_abo_valid"]:
        inferred["donor_abo_valid"] = (
            ABO_RULES[fakta["komponen"]][fakta["pasien_abo"]].copy()
        )
        aturan_terpicu = True

    # Terapkan aturan Rhesus jika belum diperoleh.
    if not inferred["donor_rh_valid"]:
        if (
            fakta["komponen"] == "PRC"
            and fakta["pasien_rh"] == "Negatif"
        ):
            inferred["donor_rh_valid"] = ["Negatif"]
        else:
            inferred["donor_rh_valid"] = ["Positif", "Negatif"]

        aturan_terpicu = True

    return aturan_terpicu


def jalankan_forward_chaining(fakta):
    # Validasi juga dilakukan pada mesin inferensi.
    if (
        fakta.get("komponen") not in ABO_RULES
        or fakta.get("pasien_abo") not in ("A", "B", "AB", "O")
        or fakta.get("pasien_rh") not in ("Positif", "Negatif")
    ):
        raise ValueError(
            "Golongan darah, Rhesus, atau komponen tidak valid."
        )

    inferred = {
        "donor_abo_valid": [],
        "donor_rh_valid": [],
    }

    # Berhenti ketika tidak ada fakta baru.
    while cek_aturan(fakta, inferred):
        pass

    return inferred


# ==========================================
# 3. LABEL DONOR
# ==========================================

def tampilkan_label(daftar_donor):
    # Setiap kelompok berisi maksimal empat label.
    html = (
        '<div style="display:flex;flex-direction:column;'
        'gap:8px;margin:10px 0 16px;">'
    )

    for i in range(0, len(daftar_donor), 4):
        html += (
            '<div style="display:flex;flex-wrap:wrap;gap:8px;">'
        )

        for donor in daftar_donor[i:i + 4]:
            # Menggunakan &nbsp; untuk HTML non-breaking space
            label = escape(donor).replace(" ", "&nbsp;")

            html += (
                '<span style="'
                'display:inline-flex;'
                'flex:0 0 auto;'
                'white-space:nowrap;'
                'align-items:center;'
                'background-color:#ff4b4b;'
                'color:white;'
                'padding:5px 10px;'
                'border-radius:15px;'
                'font-weight:700;'
                'line-height:1.5;'
                '">'
                f'{label}'
                '</span>'
            )

        html += '</div>'

    html += '</div>'

    st.html(html)


# ==========================================
# 4. ANTARMUKA STREAMLIT
# ==========================================

def main():
    st.set_page_config(
        page_title="BloodBridge",
        page_icon="🩸",
    )

    st.title("🩸 BloodBridge")
    st.subheader(
        "Sistem Verifikasi Kompatibilitas Darah Berbasis Pengetahuan"
    )

    st.markdown(
        "Sistem ini menggunakan metode **Forward Chaining** "
        "untuk memverifikasi kompatibilitas berdasarkan aturan "
        "**ABO**, **Rhesus**, dan jenis komponen darah "
        "**PRC** atau **FFP**."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Data Pasien")

        pasien_abo = st.selectbox(
            "Golongan Darah Pasien (ABO):",
            ["A", "B", "AB", "O"],
            index=None,
            placeholder="Pilih kategori yang sesuai",
        )

        pasien_rh = st.selectbox(
            "Status Rhesus (Rh):",
            ["Positif", "Negatif"],
            index=None,
            placeholder="Pilih kategori yang sesuai",
        )

    with col2:
        st.write("### Kebutuhan Transfusi")

        komponen = st.selectbox(
            "Jenis Komponen Darah:",
            ["PRC", "FFP"],
            index=None,
            placeholder="Pilih kategori yang sesuai",
            format_func=lambda kode: {
                "PRC": "PRC (Packed Red Cells)",
                "FFP": "FFP (Fresh Frozen Plasma)",
            }[kode],
        )

    tombol_verifikasi = st.button(
        "Verifikasi Kompatibilitas Donor",
        type="primary",
        use_container_width=True,
    )

    if tombol_verifikasi:
        if (
            pasien_abo is None
            or pasien_rh is None
            or komponen is None
        ):
            st.warning(
                "⚠️ Harap pilih Golongan Darah, Rhesus, "
                "dan Komponen terlebih dahulu."
            )

        else:
            fakta = {
                "komponen": komponen,
                "pasien_abo": pasien_abo,
                "pasien_rh": pasien_rh,
            }

            with st.spinner("Mengevaluasi basis pengetahuan..."):
                hasil = jalankan_forward_chaining(fakta)

                daftar_donor = [
                    f"{abo} {rh}"
                    for abo in hasil["donor_abo_valid"]
                    for rh in hasil["donor_rh_valid"]
                ]

            st.success("✅ Inferensi Selesai!")

            st.write(
                f"Untuk pasien **{pasien_abo} {pasien_rh}** "
                f"yang membutuhkan **{komponen}**, "
                "profil donor yang sesuai dengan aturan "
                "ABO dan Rh dalam sistem ini adalah:"
            )

            tampilkan_label(daftar_donor)

            if komponen == "PRC":
                st.info(
                    "💡 **Traceability PRC:** "
                    "Sistem menerapkan aturan ABO untuk sel darah merah. "
                    "Dalam aturan sistem ini, pasien Rh negatif "
                    "dipasangkan dengan donor Rh negatif, sedangkan "
                    "pasien Rh positif memiliki pilihan donor "
                    "Rh positif maupun negatif."
                )

            else:
                st.warning(
                    "💡 **Traceability FFP:** "
                    "Sistem menggunakan aturan ABO untuk plasma "
                    "yang berkebalikan dengan PRC. "
                    "Dalam aturan FFP pada aplikasi ini, "
                    "Rhesus tidak menjadi pembatas pilihan donor."
                )

    st.caption(
        "Aplikasi edukasi: hasil hanya mencakup aturan ABO dan Rh, "
        "bukan penetapan kelayakan transfusi klinis."
    )


if __name__ == "__main__":
    main()
