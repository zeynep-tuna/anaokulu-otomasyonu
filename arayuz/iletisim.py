"""
İletişim sayfası.
"""

import streamlit as st

ILETISIM_CSS = """
<style>
    /* İletişim bilgi kartlarına hover */
    .iletisim-kutu {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .iletisim-kutu:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }

    /* Bu sayfaya özel: başlık kutusunun üstünde/altında ekstra boşluk */
    .iletisim-baslik-bosluk-ust { margin-top: 1rem; }
    .iletisim-baslik-bosluk-alt { margin-bottom: 2rem; }
</style>
"""


def iletisim_stilleri_yukle():
    st.markdown(ILETISIM_CSS, unsafe_allow_html=True)


def iletisim_goster():
    st.markdown('<div class="iletisim-baslik-bosluk-ust"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="baslik-kutu">
        <h1>📍 İletişim</h1>
        <p>Bize ulaşın, sorularınızı yanıtlayalım</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="iletisim-baslik-bosluk-alt"></div>', unsafe_allow_html=True)

    # ---------------- İletişim bilgileri ----------------
    sol, sag = st.columns(2)
    with sol:
        st.markdown("""
        <div class="iletisim-kutu">
            <h3>Adres</h3>
            <p>Güzeller Mahallesi, Bahar Caddesi No: 12<br>Gebze / Kocaeli</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="iletisim-kutu">
            <h3>Telefon</h3>
            <p>📞 0262 123 45 67</p>
        </div>
        """, unsafe_allow_html=True)
    with sag:
        st.markdown("""
        <div class="iletisim-kutu">
            <h3>E-posta</h3>
            <p>✉️ info@minikadimlar.com.tr</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="iletisim-kutu">
            <h3>Çalışma Saatleri</h3>
            <p>Hafta içi: 08:00 - 18:00<br>Hafta sonu: Kapalı</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="margin-bottom: 3rem;"></div>', unsafe_allow_html=True)