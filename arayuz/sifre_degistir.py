"""
Şifre Değiştirme sayfası — header'daki kullanıcı menüsünden erişilir.
"""

import streamlit as st
from veritabani import listele, calistir

SIFRE_DEGISTIR_CSS = """
<style>
    .st-key-sifre_karti {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 2.5rem 2.5rem 1.5rem 2.5rem;
        box-shadow: 0 10px 35px rgba(0,0,0,0.12);
        max-width: 430px;
        margin: 5rem auto !important;
        border: 1px solid #FFE3B8;
    }
    .sifre-baslik {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        color: #D97B3D;
        margin-bottom: 1.5rem;
    }
    .st-key-sifre_karti .stButton button {
        background-color: #FFB86B;
        color: #3D3D3D;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    .st-key-sifre_karti .stButton button:hover {
        background-color: #E17B8C;
        color: white;
    }
    .st-key-sifre_geri_link button {
        background-color: transparent !important;
        color: #888 !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        box-shadow: none !important;
    }
    .st-key-sifre_geri_link button:hover {
        color: #D97B3D !important;
        background-color: transparent !important;
    }
</style>
"""


def sifre_degistir_stilleri_yukle():
    st.markdown(SIFRE_DEGISTIR_CSS, unsafe_allow_html=True)


def sifre_degistir_goster():
    sifre_degistir_stilleri_yukle()
    kullanici_adi = st.session_state.get("kullanici_adi")

    with st.container(key="sifre_karti"):
        st.markdown('<div class="sifre-baslik">🔑 Şifre Değiştir</div>', unsafe_allow_html=True)

        with st.form("sifre_degistir_formu"):
            mevcut_sifre = st.text_input("Mevcut Şifre", type="password")
            yeni_sifre = st.text_input("Yeni Şifre", type="password")
            yeni_sifre_tekrar = st.text_input("Yeni Şifre (Tekrar)", type="password")
            gonder = st.form_submit_button("Şifreyi Güncelle")
            if gonder:
                dogrulama = listele(
                    "SELECT * FROM kullanici WHERE kullanici_adi = ? AND sifre_hash = ?",
                    [kullanici_adi, mevcut_sifre],
                )
                if dogrulama.empty:
                    st.error("Mevcut şifreniz hatalı.")
                elif not yeni_sifre:
                    st.error("Yeni şifre boş olamaz.")
                elif yeni_sifre != yeni_sifre_tekrar:
                    st.error("Yeni şifreler eşleşmiyor.")
                else:
                    try:
                        calistir(
                            "UPDATE kullanici SET sifre_hash = ? WHERE kullanici_adi = ?",
                            [yeni_sifre, kullanici_adi],
                        )
                        st.success("Şifreniz güncellendi.")
                    except Exception as e:
                        st.error(f"Güncellenemedi. ({e})")

        with st.container(key="sifre_geri_link"):
            if st.button("← Ana Sayfaya Dön"):
                st.session_state.sayfa = "anasayfa"
                st.rerun()
