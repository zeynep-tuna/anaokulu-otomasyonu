"""
Personel Paneli — giriş yapan personel, pozisyonuna göre kendi
görev listesini (temizlik/yemek) ve bilgilerini görür.

Not: Öğretmen/Veli panelleriyle aynı mimari — header'daki nav
linklerinden gelen st.session_state.personel_aktif_bolum değerine
göre içerik gösteriyor. Hangi bölümlerin görüneceği (Temizlik/Yemek)
header.py'de, personelin "pozisyon" alanına göre belirleniyor.

Not: Personel sadece GÖRÜNTÜLER — kayıt ekleme/silme yok, tıpkı
Veli panelindeki gibi.
"""

import time
import streamlit as st
import pandas as pd
from veritabani import listele, calistir

PERSONEL_CSS = """
<style>
    /* Kartlar — key bazlı, garanti çalışan seçici */
    div[class*="st-key-kart_"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EFE4D6 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        border-radius: 10px !important;
    }

    /* Durum filtre butonları — küçük, pill (hap) görünümü */
    .st-key-temizlik_filtre_kutu,
    .st-key-odeme_filtre_kutu {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .st-key-temizlik_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-odeme_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-temizlik_filtre_kutu div[data-testid="stVerticalBlock"],
    .st-key-odeme_filtre_kutu div[data-testid="stVerticalBlock"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    .st-key-temizlik_filtre_kutu .stButton button,
    .st-key-odeme_filtre_kutu .stButton button {
        border-radius: 9999px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.3rem 0.9rem !important;
        white-space: nowrap;
    }
    .st-key-temizlik_filtre_kutu .stButton button[kind="secondary"],
    .st-key-odeme_filtre_kutu .stButton button[kind="secondary"] {
        background-color: #FFF6EC !important;
        border: 1px solid #F0E4D8 !important;
        color: #8A8175 !important;
    }
    .st-key-temizlik_filtre_kutu .stButton button[kind="secondary"]:hover,
    .st-key-odeme_filtre_kutu .stButton button[kind="secondary"]:hover {
        border-color: #FFB86B !important;
        color: #D97B3D !important;
    }
    .st-key-temizlik_filtre_kutu .stButton button[kind="primary"],
    .st-key-odeme_filtre_kutu .stButton button[kind="primary"] {
        background-color: #D97B3D !important;
        border: 1px solid #D97B3D !important;
    }
</style>
"""


def personel_stilleri_yukle():
    st.markdown(PERSONEL_CSS, unsafe_allow_html=True)


def _grid_goster(satirlar, kart_fonksiyonu, satir_basina=4):
    """satirlar: DataFrame satırlarının listesi ([(index, row), ...]).
    Her satırda en fazla `satir_basina` kart olacak şekilde, taşanları
    yeni satıra geçirerek gösterir. Her kart için benzersiz bir index
    (CSS key'i için) kart_fonksiyonu'na iletilir."""
    sayac = 0
    for i in range(0, len(satirlar), satir_basina):
        parca = satirlar[i:i + satir_basina]
        kolonlar = st.columns(satir_basina)
        for kolon, (_, satir) in zip(kolonlar, parca):
            with kolon:
                kart_fonksiyonu(satir, sayac)
                sayac += 1


def personel_paneli_goster():
    personel_stilleri_yukle()

    personel_id = st.session_state.get("personel_id")

    if not personel_id:
        st.error("Bu hesap bir personel kaydına bağlı değil. Lütfen yöneticinizle iletişime geçin.")
        return

    personel_bilgi = listele("SELECT * FROM personel WHERE personel_id = ?", [personel_id])
    if personel_bilgi.empty:
        st.error("Personel kaydı bulunamadı.")
        return

    aktif_bolum = st.session_state.get("personel_aktif_bolum", "bilgilerim")

    # ============================================================
    # BİLGİLERİM
    # ============================================================
    if aktif_bolum == "bilgilerim":
        st.markdown("### 👤 Bilgilerim")
        col_kart, col_bos = st.columns([2, 3])
        with col_kart:
            with st.container(border=True, key="kart_bilgilerim"):
                st.markdown(f"**Ad Soyad:** {personel_bilgi.iloc[0]['ad']} {personel_bilgi.iloc[0]['soyad']}")
                st.markdown(f"**Kullanıcı Adı:** {st.session_state.get('kullanici_adi', '')}")
                st.markdown(f"**Pozisyon:** {personel_bilgi.iloc[0]['pozisyon']}")
                st.markdown(f"**Görev:** {personel_bilgi.iloc[0]['gorev']}")
                st.markdown(f"**İşe Giriş Tarihi:** {personel_bilgi.iloc[0]['ise_giris_tarihi']}")
                st.markdown(f"**Tecrübe:** {personel_bilgi.iloc[0]['tecrube']} yıl")
                st.markdown(f"**Telefon:** {personel_bilgi.iloc[0]['tel_no']}")
                st.markdown(f"**Adres:** {personel_bilgi.iloc[0]['adres']}")
        return

    # ============================================================
    # TEMİZLİK LİSTESİ
    # ============================================================
    if aktif_bolum == "temizlik_listesi":
        st.markdown("### 🧹 Temizlik Listesi")
        kayitlar = listele(
            "SELECT * FROM temizlik_listesi WHERE personel_id = ? ORDER BY tarih DESC",
            [personel_id],
        )

        if kayitlar.empty:
            st.info("Henüz bir temizlik kaydınız bulunmuyor.")
        else:
            # Durum filtresi — Tümü / Yapılacaklar / Tamamlananlar
            filtre_key = "temizlik_filtre_secim"
            if filtre_key not in st.session_state:
                st.session_state[filtre_key] = "Tümü"

            secenekler = ["Tümü", "Yapılacaklar", "Tamamlananlar"]
            with st.container(key="temizlik_filtre_kutu"):
                for secenek in secenekler:
                    if st.button(
                        secenek,
                        key=f"temizlik_filtre_btn_{secenek}",
                        type="primary" if st.session_state[filtre_key] == secenek else "secondary",
                    ):
                        st.session_state[filtre_key] = secenek
                        st.rerun()

            secim = st.session_state[filtre_key]
            if secim == "Yapılacaklar":
                kayitlar = kayitlar[kayitlar["durum"] == "Devam Ediyor"]
            elif secim == "Tamamlananlar":
                kayitlar = kayitlar[kayitlar["durum"] == "Tamamlandı"]

            # Tarih sıralaması
            siralama = st.radio(
                "Sırala", ["Yeniden Eskiye", "Eskiden Yeniye"],
                horizontal=True, key="temizlik_siralama", label_visibility="collapsed",
            )
            kayitlar = kayitlar.sort_values("tarih", ascending=(siralama == "Eskiden Yeniye"))

            if kayitlar.empty:
                st.info("Bu filtreye uygun kayıt bulunamadı.")
            else:
                def _temizlik_karti(kayit, idx):
                    kayit_id = int(kayit["temizlik_listesi_id"])
                    with st.container(border=True, key=f"kart_temizlik_{idx}"):
                        st.markdown(f"### 🧹 {kayit['alan']}")
                        st.markdown(f"**Tarih:** {kayit['tarih']}")

                        durum_secenekleri = ["Tamamlandı", "Devam Ediyor"]
                        mevcut_durum = kayit["durum"]
                        varsayilan_index = (
                            durum_secenekleri.index(mevcut_durum) if mevcut_durum in durum_secenekleri else 0
                        )

                        with st.form(f"form_durum_{kayit_id}"):
                            yeni_durum = st.selectbox(
                                "Durum", durum_secenekleri, index=varsayilan_index, key=f"durum_sec_{kayit_id}"
                            )
                            guncelle = st.form_submit_button("Güncelle")
                            if guncelle:
                                try:
                                    calistir(
                                        "UPDATE temizlik_listesi SET durum = ? WHERE temizlik_listesi_id = ?",
                                        [yeni_durum, kayit_id],
                                    )
                                    st.success("Durum güncellendi.")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Güncellenemedi: {e}")
                _grid_goster(list(kayitlar.iterrows()), _temizlik_karti)
        return

    # ============================================================
    # YEMEK LİSTESİ
    # ============================================================
    if aktif_bolum == "yemek_listesi":
        st.markdown("### 🍴 Yemek Listesi")
        kayitlar = listele(
            "SELECT * FROM yemek_listesi WHERE personel_id = ? ORDER BY tarih DESC",
            [personel_id],
        )
        if kayitlar.empty:
            st.info("Henüz bir yemek kaydınız bulunmuyor.")
        else:
            # Aynı güne ait yemekleri (çorba/ana yemek/yan yemek) TEK bir
            # kartta topluyoruz — her yemek ayrı kart değil, her GÜN ayrı kart.
            tarihler = sorted(kayitlar["tarih"].unique(), reverse=True)
            gunler = [(t, kayitlar[kayitlar["tarih"] == t]) for t in tarihler]

            def _gun_karti(gun_verisi, idx):
                tarih, o_gunun_yemekleri = gun_verisi
                with st.container(border=True, key=f"kart_yemek_{idx}"):
                    st.markdown(f"### 🍴 {tarih}")
                    for _, yemek in o_gunun_yemekleri.iterrows():
                        tur = yemek["yemek_turu"] if "yemek_turu" in yemek.index else None
                        if pd.notna(tur) and str(tur).strip():
                            st.markdown(f"**{tur}:** {yemek['yemek_adi']}")
                        else:
                            st.markdown(f"- {yemek['yemek_adi']}")

            _grid_goster(list(enumerate(gunler)), _gun_karti)
        return

    # ============================================================
    # SAĞLIK TAKİBİ (öğrenci alerji / kronik hastalık / acil durum)
    # ============================================================
    if aktif_bolum == "saglik_listesi":
        st.markdown("### 🩺 Sağlık Takibi")
        kayitlar = listele("""
            SELECT sl.*, o.ad AS ogrenci_ad, o.soyad AS ogrenci_soyad
            FROM saglik_listesi sl
            LEFT JOIN ogrenci o ON sl.ogrenci_id = o.ogrenci_id
        """)
        if kayitlar.empty:
            st.info("Henüz bir sağlık kaydı bulunmuyor.")
        else:
            def _saglik_karti(kayit, idx):
                with st.container(border=True, key=f"kart_saglik_{idx}"):
                    st.markdown(f"### 🧒 {kayit['ogrenci_ad']} {kayit['ogrenci_soyad']}")
                    st.markdown(f"**Alerji:** {kayit['alerji'] or '—'}")
                    st.markdown(f"**Kronik Hastalık:** {kayit['kronik_hastalik'] or '—'}")
                    st.markdown(f"**Acil Durum Notu:** {kayit['acil_durum_notu'] or '—'}")
                    st.markdown(f"**Acil Durum Telefonu:** {kayit['acil_durum_tel'] or '—'}")
            _grid_goster(list(kayitlar.iterrows()), _saglik_karti)
        return

    # ============================================================
    # ÖDEMELER (sekreter/idari personel için)
    # ============================================================
    if aktif_bolum == "odemeler":
        st.markdown("### 💳 Ödemeler")
        kayitlar = listele("""
            SELECT od.*, o.ad AS ogrenci_ad, o.soyad AS ogrenci_soyad
            FROM odemeler od
            LEFT JOIN ogrenci o ON od.ogrenci_id = o.ogrenci_id
            ORDER BY od.tarih DESC
        """)

        if kayitlar.empty:
            st.info("Henüz bir ödeme kaydı bulunmuyor.")
        else:
            # Durum filtresi — Tümü / Bekleyenler / Ödenenler
            filtre_key = "odeme_filtre_secim"
            if filtre_key not in st.session_state:
                st.session_state[filtre_key] = "Tümü"

            secenekler = ["Tümü", "Bekleyenler", "Ödenenler"]
            with st.container(key="odeme_filtre_kutu"):
                for secenek in secenekler:
                    if st.button(
                        secenek,
                        key=f"odeme_filtre_btn_{secenek}",
                        type="primary" if st.session_state[filtre_key] == secenek else "secondary",
                    ):
                        st.session_state[filtre_key] = secenek
                        st.rerun()

            secim = st.session_state[filtre_key]
            if secim == "Bekleyenler":
                kayitlar = kayitlar[kayitlar["odeme_durumu"] == "Bekliyor"]
            elif secim == "Ödenenler":
                kayitlar = kayitlar[kayitlar["odeme_durumu"] == "Ödendi"]

            if kayitlar.empty:
                st.info("Bu filtreye uygun kayıt bulunamadı.")
            else:
                def _odeme_karti(kayit, idx):
                    kayit_id = int(kayit["odemeler_id"])
                    with st.container(border=True, key=f"kart_odeme_{idx}"):
                        st.markdown(f"### 🧒 {kayit['ogrenci_ad']} {kayit['ogrenci_soyad']}")
                        st.markdown(f"**Tarih:** {kayit['tarih']}")
                        st.markdown(f"**Durum:** {kayit['odeme_durumu']}")
                        if kayit["odeme_durumu"] == "Bekliyor":
                            if st.button("✅ Ödendi olarak işaretle", key=f"btn_odendi_{kayit_id}", use_container_width=True):
                                try:
                                    calistir(
                                        "UPDATE odemeler SET odeme_durumu = 'Ödendi' WHERE odemeler_id = ?",
                                        [kayit_id],
                                    )
                                    st.success("Ödeme durumu güncellendi.")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Güncellenemedi: {e}")
                        else:
                            st.markdown(f"**Ödeme Şekli:** {kayit['odeme_sekli']}")
                            st.markdown(f"**Tutar:** {kayit['odeme_tutari']} ₺")
                _grid_goster(list(kayitlar.iterrows()), _odeme_karti)
        return