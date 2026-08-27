"""
Giriş sayfası (header/footer'sız). Şimdilik basit tutuldu — ayrıca
düzenlenecek.
"""

import streamlit as st
import pandas as pd
from veritabani import listele

GIRIS_CSS = """
<style>
    /* Üst araç çubuklarını gizle */
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

    /* Sayfanın üst boşluklarını tamamen kaldır */
    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"],
    .main .block-container,
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }

    /* Giriş kartını yukarı taşır */
    .st-key-giris_karti {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 2.2rem 2.5rem 1.5rem 2.5rem;
        box-shadow: 0 10px 35px rgba(0,0,0,0.12);
        max-width: 430px;
        margin: -6rem auto 1rem auto !important; /* Kartı belirgin şekilde yukarı çeker */
        border: 1px solid #FFE3B8;
        position: relative;
        z-index: 10;
    }
    .giris-logo {
        text-align: center;
        font-size: 1.7rem;
        font-weight: 700;
        color: #D97B3D;
        margin-bottom: 0.3rem;
    }
    .giris-alt-yazi {
        text-align: center;
        color: #888;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    .st-key-giris_karti .stButton button {
        background-color: #FFB86B;
        color: #3D3D3D;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    .st-key-giris_karti .stButton button:hover {
        background-color: #E17B8C;
        color: white;
    }
    .st-key-donus_linki button {
        background-color: transparent !important;
        color: #888 !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        box-shadow: none !important;
    }
    .st-key-donus_linki button:hover {
        color: #D97B3D !important;
        background-color: transparent !important;
    }
</style>
"""


def giris_stilleri_yukle():
    st.markdown(GIRIS_CSS, unsafe_allow_html=True)


def giris_goster():
    with st.container(key="giris_karti"):
        st.markdown('<div class="giris-logo">🌈 Minik Adımlar Anaokulu</div>', unsafe_allow_html=True)
        st.markdown('<div class="giris-alt-yazi">Veli, öğretmen veya personel hesabınızla giriş yapın</div>', unsafe_allow_html=True)

        with st.form("giris_formu"):
            kullanici_adi_giris = st.text_input("Kullanıcı Adı")
            sifre_giris = st.text_input("Şifre", type="password")
            giris_buton = st.form_submit_button("Giriş Yap")
            if giris_buton:
                sorgu = """
                    SELECT k.kullanici_adi, r.rol_adi, k.ogretmen_id, k.veli_id, k.personel_id
                    FROM kullanici k
                    JOIN rol r ON k.rol_id = r.rol_id
                    WHERE k.kullanici_adi = ? AND k.sifre_hash = ?
                """
                sonuc = listele(sorgu, [kullanici_adi_giris, sifre_giris])
                if not sonuc.empty:
                    st.session_state.giris_yapildi = True
                    st.session_state.rol_adi = sonuc.iloc[0]["rol_adi"]
                    st.session_state.kullanici_adi = sonuc.iloc[0]["kullanici_adi"]

                    def _guvenli_int(deger):
                        return int(deger) if pd.notna(deger) else None

                    st.session_state.ogretmen_id = _guvenli_int(sonuc.iloc[0]["ogretmen_id"])
                    st.session_state.veli_id = _guvenli_int(sonuc.iloc[0]["veli_id"])
                    st.session_state.personel_id = _guvenli_int(sonuc.iloc[0]["personel_id"])
                    st.session_state.sayfa = "anasayfa"
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre hatalı.")

        with st.container(key="donus_linki"):
            if st.button("← Ana Sayfaya Dön"):
                st.session_state.sayfa = "anasayfa"
                st.rerun()