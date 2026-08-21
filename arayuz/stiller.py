"""
Birden fazla sayfada ORTAK kullanılan stiller.

Header ve footer'a özel stiller kendi dosyalarında tutulur.
"""

import streamlit as st


ORTAK_CSS = """
<style>

    /* =========================================================
       GENEL SAYFA
       ========================================================= */

    .stApp {
        background-color: #FAFAF7;
    }


    /* =========================================================
       STREAMLIT ÜST BOŞLUKLARI
       ========================================================= */

    div[data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
    }

    div[data-testid="stMain"] {
        padding-top: 0 !important;
    }

    .main .block-container {
        padding-top: 0 !important;
    }

    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"],
    section.main .block-container,
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }


    /* =========================================================
       SAYFA İÇERİĞİ
       ========================================================= */

    .st-key-sayfa_icerigi {
        max-width: none;
        margin: 0 !important;
        padding: 1.5rem 3.5rem 1rem 3.5rem;
    }


    /* =========================================================
       SAYFA BAŞLIK KUTUSU
       ========================================================= */

    .baslik-kutu {
        background: linear-gradient(
            90deg,
            #FFD9A0 0%,
            #FFF4E0 50%,
            #BBDED6 100%
        );

        padding: 1.8rem 2rem;

        border-radius: 18px;

        text-align: center;

        margin: 0 auto 1.5rem auto;

        max-width: 70%;

        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }

    .baslik-kutu h1 {
        color: #3D3D3D;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }

    .baslik-kutu p {
        color: #555;
        font-size: 1.1rem;
        font-style: italic;
    }


    /* =========================================================
       HAKKIMIZDA KART ALANI
       ========================================================= */

    .hakkimizda-kart-alani {
        max-width: 1050px;
        margin: 0 auto;
    }


    /* =========================================================
       HAKKIMIZDA KARTLARI
       ========================================================= */

    .bilgi-karti {
        background-color: #FFFFFF;

        border-radius: 14px;

        padding: 1.4rem 1.5rem;

        min-height: 210px;

        box-sizing: border-box;

        margin: 0 !important;

        box-shadow: 0 4px 14px rgba(0,0,0,0.09);

        border: 1px solid #EFE9DD;

        border-left: 5px solid #FFB86B;

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;

        display: flex;
        flex-direction: column;
    }


    /* =========================================================
       HAKKIMIZDA HOVER
       ========================================================= */

    .bilgi-karti:hover {
        transform: translateY(-6px);

        box-shadow:
            0 10px 24px rgba(0,0,0,0.14);

        border-color: #FFB86B;
    }


    /* =========================================================
       HAKKIMIZDA KART BAŞLIĞI
       ========================================================= */

    .bilgi-karti h3 {
        color: #D97B3D;

        margin-top: 0;
        margin-bottom: 0.6rem;

        font-size: 1.15rem;
    }


    /* =========================================================
       HAKKIMIZDA KART YAZISI
       ========================================================= */

    .bilgi-karti p {
        margin-bottom: 0;

        line-height: 1.5;

        color: #555;
    }


    /* =========================================================
       HAKKIMIZDA SATIRLARI ARASINDA BOŞLUK
       ========================================================= */

    .hakkimizda-satir-boslugu {
        height: 30px;
    }


    /* =========================================================
       ANA SAYFADAKİ "SUNDUĞUMUZ İMKANLAR" KARTLARI
       ========================================================= */

    .imkan-karti {
        background-color: #FFFFFF;

        border-radius: 16px;

        padding: 1.8rem 1.3rem;

        text-align: center;

        box-shadow: 0 4px 14px rgba(0,0,0,0.09);

        border: 1px solid #EFE9DD;

        max-width: 80% !important;

        margin: 0 auto !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .imkan-karti:hover {
        transform: translateY(-5px);

        box-shadow:
            0 10px 24px rgba(0,0,0,0.14);

        border-color: #FFB86B;
    }

    .imkan-karti .emoji {
        font-size: 2.6rem;
        margin-bottom: 0.5rem;
    }

    .imkan-karti b {
        font-size: 1.25rem;
    }

    .imkan-karti p {
        font-size: 1rem;
        color: #777;
        margin: 0.4rem 0 0 0;
    }


    /* =========================================================
       İLETİŞİM KUTUSU
       ========================================================= */

    .iletisim-kutu {
        background-color: #EAF4F1;

        border-radius: 14px;

        padding: 1rem;

        text-align: center;

        margin: 0.5rem auto 0 auto;

        max-width: 650px;
    }

    .iletisim-kutu h3 {
        margin-top: 0;

        color: #3D8C74;
    }


    /* =========================================================
       EXPANDER
       ========================================================= */

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;

        border-radius: 12px;

        border: 2px solid #FFD9A0;
    }


</style>
"""


def ortak_stilleri_yukle():
    """
    Ana dosyada, en başta bir kere çağrılır.
    """
    st.markdown(
        ORTAK_CSS,
        unsafe_allow_html=True
    )