"""
Üst menü (header). Sadece header'a ÖZEL kod ve stiller burada.

Giriş yapılmamışsa (ya da admin girişse — admin kendi ayrı arayüzünü
kullanır, bu header hiç görünmez), normal halka açık site menüsü.

Giriş yapılmışsa (veli/öğretmen), header o role özgü bir navigasyon
menüsüne dönüşür: logo yerine "Hoş geldiniz, Ad Soyad!" yazısı, ve
Ana Sayfa/Hakkımızda gibi linkler yerine role özgü bölüm linkleri
(Çocuklarım, Ödemeler, vb.) — tıklanan bölüm session_state üzerinden
ilgili panele (veli.py / ogretmen.py) iletilir.

Not: Eski "kullanıcı adı + dropdown" mekanizması TAMAMEN kaldırıldı —
Bilgilerim ve Şifre Değiştir artık doğrudan görünür linkler, dropdown
olmadığı için header'ın "büyüme" sorunu da kökünden ortadan kalkıyor.
"""

import streamlit as st
from veritabani import listele

HEADER_CSS = """
<style>
    /* Streamlit'in üst araç çubuğunu (Deploy/⋮) tamamen gizle — admin
       panelinde bulup kalıcı olarak kaydettiğimiz aynı çözüm */
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

    /* Ana kutunun boşluğunu tüm yönlerden sıfırla — header'ın tam yukarıdan
       ve kenardan kenara başlaması için */
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
        padding: 0.55rem 3.5rem 0.4rem 3.5rem !important;
        margin-bottom: 1.5rem;
        margin-top: -9rem !important;
        position: relative;
        z-index: 9999;
        width: 100vw !important;
        left: 50%;
        transform: translateX(-50%);
    }
    .st-key-site_header .logo-yazi {
        font-size: 1.75rem;
        font-weight: 700;
        color: #D97B3D;
        padding-top: 0.6rem;
        white-space: nowrap;
    }

    /* Nav linkleri: tek satırda, sağa yaslı, buton görünümü kaldırılmış */
    div.st-key-nav_linkler {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 0.5rem !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    div.st-key-nav_linkler > div {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    div.st-key-nav_linkler div[data-testid="stElementContainer"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    .st-key-nav_linkler .stButton button,
    .st-key-nav_linkler .stButton button p,
    .st-key-nav_linkler .stButton button div {
        background-color: transparent;
        color: #3D3D3D;
        border: none;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: none;
        padding: 0.6rem 0.9rem;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        white-space: nowrap;
    }
    .st-key-nav_linkler .stButton button:hover {
        color: #D97B3D;
        border-bottom: 2px solid #D97B3D;
        background-color: transparent;
    }
    /* Aktif (seçili) bölüm linki */
    .st-key-nav_linkler .st-key-nav_aktif .stButton button {
        color: #D97B3D;
        border-bottom: 2px solid #D97B3D;
    }

    .st-key-btn_giris button,
    .st-key-btn_giris button p,
    .st-key-btn_giris button div {
        background-color: #FFB86B !important;
        color: #3D3D3D !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        padding: 0.45rem 0.9rem !important;
    }
    .st-key-btn_giris button:hover {
        background-color: #E17B8C !important;
        color: #FFFFFF !important;
        border: none !important;
    }
</style>
"""


def header_yukle():
    st.markdown(HEADER_CSS, unsafe_allow_html=True)


def git(sayfa_adi):
    st.session_state.sayfa = sayfa_adi
    st.rerun()


def _rol_ozel_menu():
    """Giriş yapan veli/öğretmen için (rol, ad_soyad, bölüm_listesi) döndürür.
    Giriş yapılmamışsa ya da admin ise (None, None, None) döner — o durumda
    normal halka açık site menüsü gösterilir."""
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

    return None, None, None


def header():
    """
    Gerçek Streamlit butonlarından oluşan üst menü (sayfa hiç yenilenmeden çalışır).
    """
    rol, ad_soyad, bolumler = _rol_ozel_menu()

    with st.container(key="site_header"):
        kol_logo, kol_bosluk, kol_nav, kol_giris = st.columns([2.2, 2.0, 3.5, 1.8])

        with kol_logo:
            if rol:
                st.markdown(f'<div class="logo-yazi">👋 Hoş geldiniz, {ad_soyad}!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="logo-yazi">🌈 Minik Adımlar Anaokulu</div>', unsafe_allow_html=True)

        with kol_nav:
            with st.container(key="nav_linkler"):
                if rol:
                    aktif_key = f"{rol}_aktif_bolum"
                    if aktif_key not in st.session_state:
                        st.session_state[aktif_key] = bolumler[0][0]
                    for bolum_key, etiket in bolumler:
                        aktif = st.session_state[aktif_key] == bolum_key
                        container_key = "nav_aktif" if aktif else f"nav_{bolum_key}_dis"
                        with st.container(key=container_key):
                            if st.button(etiket, key=f"nav_{bolum_key}"):
                                st.session_state[aktif_key] = bolum_key
                                st.rerun()
                else:
                    if st.button("Ana Sayfa", key="nav_anasayfa"):
                        git("anasayfa")
                    if st.button("Hakkımızda", key="nav_hakkimizda"):
                        git("hakkimizda")
                    if st.button("Sınıflar", key="nav_siniflar"):
                        git("siniflar")
                    if st.button("İletişim", key="nav_iletisim"):
                        git("iletisim")

        with kol_giris:
            if st.session_state.get("giris_yapildi"):
                kol_sifre, kol_cikis = st.columns([1, 2])
                with kol_sifre:
                    if st.button("🔑", key="btn_sifre_degistir", help="Şifre Değiştir"):
                        git("sifre_degistir")
                with kol_cikis:
                    if st.button("🚪 Çıkış Yap", key="btn_giris"):
                        st.session_state.giris_yapildi = False
                        st.session_state.rol_adi = None
                        st.session_state.kullanici_adi = None
                        git("anasayfa")
            else:
                if st.button("🔑 Giriş Yap", key="btn_giris"):
                    git("giris")