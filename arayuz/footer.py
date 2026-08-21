"""
Alt bilgi (footer). Sadece footer'a ÖZEL kod ve stiller burada.
"""

import streamlit as st
from header import git

FOOTER_CSS = """
<style>
    .st-key-site_footer {
        background-color: #3D3D3D;
        padding: 2rem 3rem 1.2rem 3rem;
        margin-top: 2rem;
        width: 100vw !important;
        left: 50%;
        position: relative;
        transform: translateX(-50%);
    }
    .st-key-site_footer p, .st-key-site_footer h4, .st-key-site_footer .footer-logo {
        color: #EAEAEA;
    }
    .st-key-site_footer h4 {
        color: #FFD9A0;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .st-key-site_footer .footer-logo {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFD9A0 !important;
        margin-bottom: 0.3rem;
    }
    .st-key-site_footer .stButton button {
        background-color: transparent;
        color: #CFCFCF;
        border: none;
        box-shadow: none;
        padding: 0.15rem 0;
        font-size: 0.88rem;
        text-align: left;
        font-weight: 400;
    }
    .st-key-site_footer .stButton button:hover {
        color: #FFD9A0;
        background-color: transparent;
    }
    .footer-alt {
        text-align: center;
        font-size: 0.8rem;
        color: #999;
        padding-top: 1rem;
        margin-top: 1rem;
        border-top: 1px solid #555;
    }
</style>
"""


def footer_yukle():
    st.markdown(FOOTER_CSS, unsafe_allow_html=True)


def footer():
    """Koyu renkli, gerçek Streamlit butonlarıyla çalışan alt bilgi alanı."""
    with st.container(key="site_footer"):
        kol1, kol2, kol3 = st.columns([1.3, 1, 1.3])

        with kol1:
            st.markdown('<div class="footer-logo">🌈 Minik Adımlar</div>', unsafe_allow_html=True)
            st.markdown('<p>Her adım, geleceğe bir başlangıç.</p>', unsafe_allow_html=True)

        with kol2:
            st.markdown("#### Hızlı Erişim")
            if st.button("Ana Sayfa", key="footer_anasayfa"):
                git("anasayfa")
            if st.button("Hakkımızda", key="footer_hakkimizda"):
                git("hakkimizda")
            if st.button("Sınıflar", key="footer_siniflar"):
                git("siniflar")

        with kol3:
            st.markdown("#### İletişim")
            st.markdown("<p>📍 Gebze, Kocaeli</p>", unsafe_allow_html=True)
            st.markdown("<p>📞 0262 123 45 67</p>", unsafe_allow_html=True)
            st.markdown("<p>✉️ info@minikadimlar.com.tr</p>", unsafe_allow_html=True)

        st.markdown('<div class="footer-alt">© 2026 Minik Adımlar Anaokulu — Tüm hakları saklıdır.</div>', unsafe_allow_html=True)
