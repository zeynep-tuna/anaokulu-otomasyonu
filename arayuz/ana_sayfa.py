"""
Ana giriş dosyası — streamlit run buradan çalıştırılır.
Yönlendirme (hangi sayfa gösterilecek) burada yapılır; her sayfanın
kendi içeriği kendi dosyasındadır (hakkimizda.py, siniflar.py, iletisim.py, giris.py).
"""

import streamlit as st

from stiller import ortak_stilleri_yukle
from header import header_yukle, header
from footer import footer_yukle, footer
from hakkimizda import hakkimizda_goster
from siniflar import siniflar_stilleri_yukle, siniflar_goster
from iletisim import iletisim_stilleri_yukle, iletisim_goster
from giris import giris_stilleri_yukle, giris_goster

st.set_page_config(page_title="Minik Adımlar Anaokulu", page_icon="🌈", layout="wide")

# --- Tüm stilleri yükle (her dosya kendi CSS'ini getirir) ---
ortak_stilleri_yukle()
header_yukle()
footer_yukle()
siniflar_stilleri_yukle()
iletisim_stilleri_yukle()
giris_stilleri_yukle()

# --- OTURUM DURUMU ---
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
    st.session_state.rol_adi = None
    st.session_state.kullanici_adi = None
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "anasayfa"


def anasayfa_goster():
    st.markdown("""
    <div class="baslik-kutu">
        <h1>🌈 Minik Adımlar Anaokulu</h1>
        <p>Her adım, geleceğe bir başlangıç</p>
    </div>
    """, unsafe_allow_html=True)

    sol_sutun, sag_sutun = st.columns(2, gap="large")

    with sol_sutun:
        st.markdown("""
        <div class="bilgi-karti">
            <h3>💛 Hakkımızda</h3>
            <p>Minik Adımlar Anaokulu olarak, çocuklarımızın güvenli, sevgi
            dolu ve keşfe açık bir ortamda büyümesi için çalışıyoruz.
            2015'ten bu yana Gebze'de faaliyet gösteriyor, deneyimli
            öğretmen kadromuz, modern eğitim materyallerimiz ve güvenli
            tesislerimizle her çocuğun kendi hızında gelişebileceği bir
            eğitim ortamı sunuyoruz. Amacımız sadece bilgi aktarmak değil,
            özgüvenli, meraklı ve mutlu bireyler yetiştirmektir.</p>
        </div>
        """, unsafe_allow_html=True)

    with sag_sutun:
        st.markdown("""
        <div class="bilgi-karti">
            <h3>🌱 Eğitim Felsefemiz</h3>
            <p>Eğitim anlayışımızın merkezinde oyun temelli öğrenme ve
            bireysel gelişim yer alır. Her çocuğun kendine özgü bir öğrenme
            hızı ve tarzı olduğuna inanıyor, sınıflarımızı bu farklılıkları
            destekleyecek şekilde tasarlıyoruz. Çocuklarımızın meraklarını
            keşfetmelerine, sosyal becerilerini geliştirmelerine ve
            özgüvenle kendilerini ifade etmelerine olanak tanıyoruz.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 2.5rem; margin-bottom: 1.2rem;"><h3>✨ Sunduğumuz İmkanlar</h3></div>', unsafe_allow_html=True)

    imkanlar = [
        ("🎵", "Müzik, Resim, İngilizce", "Zenginleştirilmiş branş dersleri"),
        ("🌳", "Güvenli Bahçe", "Geniş açık hava oyun alanı"),
        ("👩‍🏫", "Uzman Kadro", "Deneyimli öğretmenler"),
        ("🍎", "Sağlıklı Beslenme", "Diyetisyen kontrollü menü"),
    ]

    ust_kolonlar = st.columns(2, gap="medium")
    for kolon, (emoji, baslik, aciklama) in zip(ust_kolonlar, imkanlar[:2]):
        with kolon:
            st.markdown(f"""
            <div class="imkan-karti">
                <div class="emoji">{emoji}</div>
                <b>{baslik}</b>
                <p>{aciklama}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)

    alt_kolonlar = st.columns(2, gap="medium")
    for kolon, (emoji, baslik, aciklama) in zip(alt_kolonlar, imkanlar[2:]):
        with kolon:
            st.markdown(f"""
            <div class="imkan-karti">
                <div class="emoji">{emoji}</div>
                <b>{baslik}</b>
                <p>{aciklama}</p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# YÖNLENDİRME
# ============================================================
if st.session_state.sayfa == "giris" and not st.session_state.giris_yapildi:
    # Giriş sayfası — header/footer YOK, kendine özgü tasarım
    giris_goster()

else:
    header()

    with st.container(key="sayfa_icerigi"):

        if st.session_state.giris_yapildi:
            st.markdown(f"""
            <div class="baslik-kutu">
                <h1>Hoş geldiniz, {st.session_state.kullanici_adi}! 🎉</h1>
                <p>Rolünüz: {st.session_state.rol_adi}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Çıkış Yap"):
                st.session_state.giris_yapildi = False
                st.session_state.rol_adi = None
                st.session_state.kullanici_adi = None
                st.session_state.sayfa = "anasayfa"
                st.rerun()
            st.info("Bu rol için özel panel yakında burada olacak.")

        elif st.session_state.sayfa == "hakkimizda":
            hakkimizda_goster()

        elif st.session_state.sayfa == "siniflar":
            siniflar_goster()

        elif st.session_state.sayfa == "iletisim":
            iletisim_goster()

        else:
            anasayfa_goster()

    footer()