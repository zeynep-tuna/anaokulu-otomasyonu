"""
Üst menü (header). Sadece header'a ÖZEL kod ve stiller burada.
"""

import streamlit as st
from veritabani import listele

HEADER_CSS = """
<style>
    /* Streamlit'in üst araç çubuğunu gizle */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    /* Ana kutu boşluk sıfırlama */
    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"],
    .main .block-container,
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    .st-key-site_header {
        background-color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        padding: 0.55rem 3.5rem 0.2rem 3.5rem !important;
        margin-bottom: 1.5rem;
        margin-top: -10rem !important;
        position: relative;
        z-index: 9999;
        width: 100vw !important;
        left: 50%;
        transform: translateX(-50%);
    }
    .st-key-site_header .logo-yazi {
        font-size: __LOGO_FONT_BOYUTU__;
        font-weight: 700;
        color: #D97B3D;
        padding-top: 0;
        white-space: nowrap;
    }
    /* Logo (Hoş geldiniz) sabit kalır — sağdaki grup buna göre dikey
       ortalanır. Hem üst düzey satıra hem panel_sag_grup'un kendi
       satırına aynı hizalamayı garanti altına alıyoruz. */
    .st-key-site_header div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    /* Sütunların kendisini de flex yapıp içeriklerini dikey ortalıyoruz
       — sadece üst satırın hizalanması yetmedi, her sütunun kendi
       içeriği de "Hoş geldiniz" yazısının tam ortasına gelmeli. */
    .st-key-site_header div[data-testid="column"],
    .st-key-site_header div[data-testid="stColumn"] {
        display: flex !important;
        align-items: center !important;
    }

    /* --- ANA SAYFA: İlk attığın orijinal CSS --- */
    div.st-key-nav_linkler {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 0.05rem !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        margin-top: 0.6rem !important; /* Sadece nav linkleri aşağı kayar, logo etkilenmez */
    }
    div.st-key-nav_linkler > div,
    div.st-key-nav_linkler div[data-testid="stElementContainer"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }

    /* --- ROL PANELİ: Linkler ve Butonlar Arasında Eşit Boşluk --- */
    div.st-key-panel_sag_grup {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 0.8rem !important; /* Tüm öğeler arasında eşit boşluk */
        width: 100% !important;
        flex-wrap: nowrap !important;
        margin-top: 0.6rem !important; /* Sadece bu grup aşağı kayar, logo etkilenmez */
    }
    div.st-key-panel_sag_grup > div,
    div.st-key-panel_sag_grup div[data-testid="stElementContainer"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }

    /* Buton ve Link Ortak Stilleri */
    .st-key-nav_linkler .stButton button,
    .st-key-nav_linkler .stButton button p,
    .st-key-nav_linkler .stButton button div,
    .st-key-panel_sag_grup .stButton button,
    .st-key-panel_sag_grup .stButton button p,
    .st-key-panel_sag_grup .stButton button div {
        background-color: transparent;
        color: #3D3D3D;
        border: none;
        font-weight: 600 !important;
        font-size: __NAV_FONT_BOYUTU__ !important;
        box-shadow: none;
        padding: 0.5rem 0.3rem !important;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        white-space: nowrap;
    }
    .st-key-nav_linkler .stButton button:hover,
    .st-key-panel_sag_grup .stButton button:hover {
        color: #D97B3D;
        border-bottom: 2px solid #D97B3D;
        background-color: transparent;
    }
    .st-key-panel_sag_grup .st-key-nav_aktif .stButton button {
        color: #D97B3D;
        border-bottom: 2px solid #D97B3D;
    }

    /* Şifre Butonu — daha kompakt, kare bir ikon butonu gibi */
    .st-key-panel_sag_grup .st-key-btn_sifre_degistir button,
    .st-key-btn_sifre_degistir button {
        border-radius: 6px !important;
        font-size: 0.8rem !important;
        padding: 0.2rem 0.4rem !important;
        min-width: 0 !important;
        width: auto !important;
        border: 1px solid #E0E0E0 !important;
    }
    .st-key-panel_sag_grup .st-key-btn_sifre_degistir button p,
    .st-key-panel_sag_grup .st-key-btn_sifre_degistir button div,
    .st-key-btn_sifre_degistir button p,
    .st-key-btn_sifre_degistir button div {
        font-size: 0.8rem !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Çıkış Yap / Giriş Yap Butonu */
    .st-key-btn_giris button,
    .st-key-btn_giris button p,
    .st-key-btn_giris button div {
        background-color: #FFB86B !important;
        color: #3D3D3D !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: __GIRIS_FONT_BOYUTU__ !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: __GIRIS_PADDING__ !important;
        white-space: nowrap !important;
    }
    .st-key-btn_giris button:hover {
        background-color: #E17B8C !important;
        color: #FFFFFF !important;
        border: none !important;
    }
</style>
"""


def header_yukle():
    rol = (st.session_state.get("rol_adi") or "").strip().lower()
    girisli = rol in ("ogretmen", "veli", "personel")

    nav_font_boyutu = "1.05rem" if girisli else "1.1rem"
    giris_font_boyutu = "0.72rem" if girisli else "0.95rem"
    giris_padding = "0.25rem 0.55rem" if girisli else "0.45rem 0.9rem"
    logo_font_boyutu = "1.25rem" if girisli else "1.75rem"

    css = HEADER_CSS.replace("__NAV_FONT_BOYUTU__", nav_font_boyutu)
    css = css.replace("__GIRIS_FONT_BOYUTU__", giris_font_boyutu)
    css = css.replace("__GIRIS_PADDING__", giris_padding)
    css = css.replace("__LOGO_FONT_BOYUTU__", logo_font_boyutu)
    st.markdown(css, unsafe_allow_html=True)


def git(sayfa_adi):
    st.session_state.sayfa = sayfa_adi
    st.rerun()


def _rol_ozel_menu():
    rol = (st.session_state.get("rol_adi") or "").strip().lower()

    if rol == "veli":
        veli_id = st.session_state.get("veli_id")
        veli_bilgi = listele("SELECT ad, soyad FROM veli WHERE veli_id = ?", [veli_id]) if veli_id else None
        ad_soyad = (
            f"{veli_bilgi.iloc[0]['ad']} {veli_bilgi.iloc[0]['soyad']}"
            if veli_bilgi is not None and not veli_bilgi.empty
            else st.session_state.get("kullanici_adi", "")
        )
        bolumler = [
            ("cocuklarim", "🧒 Çocuklarım"),
            ("yoklama", "📋 Yoklama"),
            ("odemeler", "💳 Ödemeler"),
            ("etkinlikler", "🎉 Etkinlikler"),
            ("bilgilerim", "👤 Bilgilerim"),
        ]
        return "veli", ad_soyad, bolumler

    if rol == "ogretmen":
        ogretmen_id = st.session_state.get("ogretmen_id")
        ogretmen_bilgi = listele("SELECT ad, soyad FROM ogretmen WHERE ogretmen_id = ?", [ogretmen_id]) if ogretmen_id else None
        ad_soyad = (
            f"{ogretmen_bilgi.iloc[0]['ad']} {ogretmen_bilgi.iloc[0]['soyad']}"
            if ogretmen_bilgi is not None and not ogretmen_bilgi.empty
            else st.session_state.get("kullanici_adi", "")
        )
        bolumler = [
            ("sinifim", "🏫 Sınıfım"),
            ("ogrencilerim", "🧒 Öğrencilerim"),
            ("yoklama", "📋 Yoklama"),
            ("ders_programi", "📅 Ders Programı"),
            ("etkinlikler", "🎉 Etkinlikler"),
            ("bilgilerim", "👤 Bilgilerim"),
        ]
        return "ogretmen", ad_soyad, bolumler

    if rol == "personel":
        personel_id = st.session_state.get("personel_id")
        personel_bilgi = (
            listele("SELECT ad, soyad, pozisyon FROM personel WHERE personel_id = ?", [personel_id])
            if personel_id else None
        )
        if personel_bilgi is not None and not personel_bilgi.empty:
            ad_soyad = f"{personel_bilgi.iloc[0]['ad']} {personel_bilgi.iloc[0]['soyad']}"
            pozisyon = (personel_bilgi.iloc[0]["pozisyon"] or "").strip().lower()
        else:
            ad_soyad = st.session_state.get("kullanici_adi", "")
            pozisyon = ""

        bolumler = []
        if any(k in pozisyon for k in ["temizlik"]):
            bolumler.append(("temizlik_listesi", "🧹 Temizlik Listesi"))
        if any(k in pozisyon for k in ["aşçı", "asci", "mutfak", "yemek"]):
            bolumler.append(("yemek_listesi", "🍴 Yemek Listesi"))
        if any(k in pozisyon for k in ["sağlık", "saglik", "idari", "sekreter"]):
            bolumler.append(("saglik_listesi", "🩺 Sağlık Takibi"))
        if any(k in pozisyon for k in ["sekreter", "idari"]):
            bolumler.append(("odemeler", "💳 Ödemeler"))
        bolumler.append(("bilgilerim", "👤 Bilgilerim"))
        return "personel", ad_soyad, bolumler

    return None, None, None


def header():
    rol, ad_soyad, bolumler = _rol_ozel_menu()

    with st.container(key="site_header"):
        if rol:
            # Sola: Hoş geldiniz | Sağa: Tüm linkler + butonlar tek blokta
            kol_logo, kol_sag = st.columns([2.5, 7.5])

            with kol_logo:
                st.markdown(f'<div class="logo-yazi">👋 Hoş geldiniz, {ad_soyad}!</div>', unsafe_allow_html=True)

            with kol_sag:
                with st.container(key="panel_sag_grup"):
                    # 1. Menü Linkleri
                    aktif_key = f"{rol}_aktif_bolum"
                    gecerli_bolumler = [b[0] for b in bolumler]
                    if aktif_key not in st.session_state or st.session_state[aktif_key] not in gecerli_bolumler:
                        st.session_state[aktif_key] = bolumler[0][0]
                    for bolum_key, etiket in bolumler:
                        aktif = st.session_state[aktif_key] == bolum_key
                        container_key = "nav_aktif" if aktif else f"nav_{bolum_key}_dis"
                        with st.container(key=container_key):
                            if st.button(etiket, key=f"nav_{bolum_key}"):
                                st.session_state[aktif_key] = bolum_key
                                st.rerun()

                    # 2. Şifre Değiştir Butonu
                    with st.container(key="btn_sifre_kutu"):
                        if st.button("🔑", key="btn_sifre_degistir", help="Şifre Değiştir"):
                            git("sifre_degistir")

                    # 3. Çıkış Yap Butonu
                    with st.container(key="btn_cikis_kutu"):
                        if st.button("🚪 Çıkış Yap", key="btn_giris"):
                            st.session_state.giris_yapildi = False
                            st.session_state.rol_adi = None
                            st.session_state.kullanici_adi = None
                            git("anasayfa")
        else:
            # Ana sayfa: İlk attığın 4 kolonlu orijinal düzen
            kol_logo, kol_bosluk, kol_nav, kol_giris = st.columns([2.2, 2.0, 3.5, 1.8])

            with kol_logo:
                st.markdown('<div class="logo-yazi">🌈 Minik Adımlar Anaokulu</div>', unsafe_allow_html=True)

            with kol_nav:
                with st.container(key="nav_linkler"):
                    if st.button("Ana Sayfa", key="nav_anasayfa"):
                        git("anasayfa")
                    if st.button("Hakkımızda", key="nav_hakkimizda"):
                        git("hakkimizda")
                    if st.button("Sınıflar", key="nav_siniflar"):
                        git("siniflar")
                    if st.button("İletişim", key="nav_iletisim"):
                        git("iletisim")

            with kol_giris:
                if st.button("🔑 Giriş Yap", key="btn_giris"):
                    git("giris")