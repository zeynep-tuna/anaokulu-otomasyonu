"""
İletişim sayfası.
"""

import streamlit as st

ILETISIM_CSS = """
<style>
    .st-key-iletisim_form_karti {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #FFE3B8;
        margin-bottom: 1rem;
    }

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

    # ---------------- İletişim bilgileri (üstte, başlıksız) ----------------
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

    # ---------------- Bize Yazın (altta, sola yaslı, formla aynı hizada) ----------------
    st.markdown("### 💬 Bize Yazın")
    form_sol, form_sag = st.columns([1.3, 1])
    with form_sol:
        with st.container(key="iletisim_form_karti"):
            with st.form("iletisim_formu"):
                ad_soyad = st.text_input("Ad Soyad")
                mesaj = st.text_area("Mesajınız", height=90)
                gonder = st.form_submit_button("Gönder")
                if gonder:
                    st.success("Mesajınız alındı, en kısa sürede size dönüş yapacağız!")