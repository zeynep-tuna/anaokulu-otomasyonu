import streamlit as st
from veritabani import listele

# ============================================================
# RENK PALETİ — her sınıfa otomatik ve sırayla atanır
# ============================================================
RENK_PALETI = [
    {"arka_plan": "linear-gradient(135deg, #FFE0EC 0%, #FFFFFF 70%)", "kenar": "#FF9EBB", "vurgu": "#E1547E"},
    {"arka_plan": "linear-gradient(135deg, #FFF9D9 0%, #FFFFFF 70%)", "kenar": "#E8D44D", "vurgu": "#B89B1A"},
    {"arka_plan": "linear-gradient(135deg, #DFF3E3 0%, #FFFFFF 70%)", "kenar": "#7FC495", "vurgu": "#3D8C58"},
    {"arka_plan": "linear-gradient(135deg, #E0ECFF 0%, #FFFFFF 70%)", "kenar": "#8FB4F0", "vurgu": "#4A73B8"},
    {"arka_plan": "linear-gradient(135deg, #F3E0FF 0%, #FFFFFF 70%)", "kenar": "#C48FE8", "vurgu": "#8A4CB8"},
]

SINIFLAR_ORTAK_CSS = """
<style>
    .siniflar-baslik-kutu {
        background: linear-gradient(120deg, #FFF4E0 0%, #DFF3E3 100%);
        padding: 1.8rem 2rem;
        border-radius: 18px;
        text-align: center;
        margin: 0 auto 1.8rem auto;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }
    .siniflar-baslik-kutu h1 { color: #3D3D3D; font-size: 2.2rem; margin-bottom: 0.2rem; }
    .siniflar-baslik-kutu p { color: #555; font-size: 1.05rem; font-style: italic; }
</style>
"""


def _sinif_css(sinif_id, renk):
    """Butonun kendisini büyük, kart görünümlü hale getirir."""
    return f"""
    <style>
        .st-key-kart_{sinif_id} button {{
            background: {renk['arka_plan']} !important;
            border: 2px solid {renk['kenar']} !important;
            border-radius: 18px !important;
            aspect-ratio: 70 / 30 !important;
            max-width: 500px !important;
            width: 100% !important;
            margin: 0 auto !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: pre-line !important;
            color: {renk['vurgu']} !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            line-height: 1.7 !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }}
        .st-key-kart_{sinif_id} button:hover {{
            transform: translateY(-6px);
            box-shadow: 0 12px 26px rgba(0,0,0,0.15);
            border-color: {renk['vurgu']} !important;
            color: {renk['vurgu']} !important;
        }}
        .st-key-kart_{sinif_id} button p {{
            font-size: inherit !important;
        }}
        .st-key-kart_{sinif_id} button::first-line {{
            font-size: 3rem !important;
        }}
    </style>
    """


def siniflar_stilleri_yukle():
    st.markdown(SINIFLAR_ORTAK_CSS, unsafe_allow_html=True)
    siniflar_veri = listele("SELECT sinif_id FROM sinif")
    for i, (_, satir) in enumerate(siniflar_veri.iterrows()):
        renk = RENK_PALETI[i % len(RENK_PALETI)]
        st.markdown(_sinif_css(satir["sinif_id"], renk), unsafe_allow_html=True)


@st.dialog("Sınıf Detayı", width="large")
def sinif_detay_goster(sinif_adi, yas_grubu, kapasite, sinif_id):
    st.markdown(f"## 🎨 {sinif_adi} Sınıfı")
    st.caption(f"Hedef Yaş: {yas_grubu} | Sınıf Kapasitesi: {kapasite} Kişi")
    st.markdown("### 🕒 Günlük Ders Programı")

    dersler = listele(
        """
        SELECT d.ders_adi, d.baslangic_saati, d.bitis_saati, o.ad AS ogretmen_adi, o.soyad AS ogretmen_soyadi
        FROM ders d
        LEFT JOIN ogretmen o ON d.ogretmen_id = o.ogretmen_id
        WHERE d.sinif_id = ?
        ORDER BY d.baslangic_saati
        """,
        [sinif_id]
    )

    if dersler.empty:
        st.info("Bu sınıf için henüz ders programı eklenmemiş.")
    else:
        for _, ders in dersler.iterrows():
            c1, c2, c3 = st.columns([1.3, 2, 1.5])
            with c1:
                st.markdown(f"**🕒 {ders['baslangic_saati']}–{ders['bitis_saati']}**")
            with c2:
                st.markdown(ders["ders_adi"])
            with c3:
                if ders["ogretmen_adi"] and str(ders["ogretmen_adi"]) != "nan":
                    st.markdown(f"👩‍🏫 {ders['ogretmen_adi']} {ders['ogretmen_soyadi']}")


def siniflar_goster():
    st.markdown("""
    <div class="siniflar-baslik-kutu">
        <h1>🏫 Sınıflarımız</h1>
        <p>Bir sınıfa tıklayarak günlük ders programını görebilirsiniz</p>
    </div>
    """, unsafe_allow_html=True)

    siniflar_veri = listele("SELECT sinif_id, sinif_adi, yas_grubu, kapasite FROM sinif")

    if siniflar_veri.empty:
        st.info("Henüz sınıf bilgisi eklenmemiş.")
        return

    kolonlar = st.columns(len(siniflar_veri), gap="small")
    for kolon, (_, satir) in zip(kolonlar, siniflar_veri.iterrows()):
        sinif_id = satir["sinif_id"]
        etiket = f"🎨\n{satir['sinif_adi']} Sınıfı\n{satir['yas_grubu']} · Kapasite: {satir['kapasite']}"
        with kolon:
            with st.container(key=f"kart_{sinif_id}"):
                if st.button(etiket, key=f"btn_{sinif_id}"):
                    sinif_detay_goster(satir['sinif_adi'], satir['yas_grubu'], satir['kapasite'], sinif_id)