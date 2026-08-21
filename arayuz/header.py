"""
Üst menü (header). Sadece header'a ÖZEL kod ve stiller burada.
"""

import streamlit as st

HEADER_CSS = """
<style>
    .st-key-site_header {
        background-color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        padding: 1.3rem 3.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 9999;
        width: 100vw !important;
        left: 50%;
        transform: translateX(-50%);
    }
    .st-key-site_header .logo-yazi {
        font-size: 1.5rem;
        font-weight: 700;
        color: #D97B3D;
        padding-top: 0.3rem;
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
    .st-key-nav_linkler .stButton button {
        background-color: transparent;
        color: #3D3D3D;
        border: none;
        font-weight: 600;
        font-size: 1.25rem;
        box-shadow: none;
        padding: 0.6rem 1.1rem;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        white-space: nowrap;
    }
    .st-key-nav_linkler .stButton button:hover {
        color: #D97B3D;
        border-bottom: 2px solid #D97B3D;
        background-color: transparent;
    }

    .st-key-btn_giris button {
        background-color: #FFB86B !important;
        color: #3D3D3D !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        border: none !important;
        padding: 0.6rem 1.3rem !important;
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


def header():
    """
    Gerçek Streamlit butonlarından oluşan üst menü (sayfa hiç yenilenmeden çalışır).
    """
    with st.container(key="site_header"):
        kol_logo, kol_bosluk, kol_nav, kol_giris = st.columns([2.2, 2.5, 3.3, 1.2])

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
            # NOT: şimdilik işlevsiz — giriş sayfası kendi dosyasında (giris.py) ayrıca ele alınacak
            st.button("🔑 Giriş Yap", key="btn_giris")
