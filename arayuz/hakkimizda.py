"""
Hakkımızda sayfası.
"""

import streamlit as st


def hakkimizda_goster():

    # =========================================================
    # BAŞLIK
    # =========================================================

    st.markdown("""
    <div class="baslik-kutu">
        <h1>💛 Hakkımızda</h1>
        <p>Minik Adımlar Anaokulu'nu tanıyın</p>
    </div>
    """, unsafe_allow_html=True)


    # =========================================================
    # KART ALANI
    # =========================================================

    # Kartları sağdan ve soldan biraz içeri almak için
    st.markdown("""
    <div class="hakkimizda-kart-alani">
    """, unsafe_allow_html=True)


    # =========================================================
    # 1. SATIR
    # =========================================================

    ust_sol, ust_sag = st.columns(2, gap="large")

    with ust_sol:
        st.markdown("""
        <div class="bilgi-karti hakkimizda-karti">
            <h3>👶 Kim Olduğumuz</h3>
            <p>
                Minik Adımlar Anaokulu, 2015 yılından bu yana Gebze'de
                faaliyet gösteren, çocuk merkezli eğitim anlayışını
                benimseyen bir kurumdur. Deneyimli öğretmen kadromuz ve
                güvenli tesislerimizle, çocuklarınızın gelişimine değer
                katmayı hedefliyoruz.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with ust_sag:
        st.markdown("""
        <div class="bilgi-karti hakkimizda-karti">
            <h3>🌱 Eğitim Felsefemiz</h3>
            <p>
                Eğitim anlayışımızın merkezinde oyun temelli öğrenme ve
                bireysel gelişim yer alır. Çocuklarımızın meraklarını
                keşfetmelerine ve özgüvenle kendilerini ifade etmelerine
                olanak tanıyoruz.
            </p>
        </div>
        """, unsafe_allow_html=True)


    # =========================================================
    # SATIRLAR ARASI BOŞLUK
    # =========================================================

    st.markdown("""
    <div class="hakkimizda-satir-boslugu"></div>
    """, unsafe_allow_html=True)


    # =========================================================
    # 2. SATIR
    # =========================================================

    alt_sol, alt_sag = st.columns(2, gap="large")

    with alt_sol:
        st.markdown("""
        <div class="bilgi-karti hakkimizda-karti">
            <h3>🎯 Misyonumuz</h3>
            <p>
                Her çocuğun kendine özgü hızında, güvenli ve sevgi dolu
                bir ortamda gelişebileceği; merak, keşif ve oyunun iç içe
                geçtiği bir eğitim deneyimi sunmak.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with alt_sag:
        st.markdown("""
        <div class="bilgi-karti hakkimizda-karti">
            <h3>👩‍🏫 Ekibimiz</h3>
            <p>
                Alanında deneyimli, çocuk gelişimi ve okul öncesi eğitim
                konusunda uzmanlaşmış öğretmen kadromuz, her çocuğa özel
                ilgi gösterecek şekilde sınıf mevcutlarını sınırlı
                tutuyoruz.
            </p>
        </div>
        """, unsafe_allow_html=True)


    # Kart alanını kapat
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)