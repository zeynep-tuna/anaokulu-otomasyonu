"""
Öğretmen Paneli — giriş yapan öğretmen kendi sınıfını, öğrencilerini,
yoklamasını, ders programını ve etkinliklerini görür/yönetir.

Not: Artık sekmeler (tabs) yerine header'daki navigasyon linklerinden
gelen st.session_state.ogretmen_aktif_bolum değerine göre içerik
gösteriyor — hangi bölüm seçiliyse (Sınıfım, Yoklama, vb.) sadece o
gösterilir.

Not: Veriler veritabanından her zaman ID'leri içeren tam haliyle çekiliyor
(join sorguları için gerekli), ama EKRANA hiçbir teknik ID sütunu
basılmıyor — her şey kart görünümünde, okunabilir bilgilerle gösteriliyor.

Kartlar artık 4'lü grid düzeninde (satır başına en fazla 4 kart, taşan
kartlar yeni satıra geçer).
"""

import streamlit as st
from datetime import date
from veritabani import listele, calistir

OGRETMEN_CSS = """
<style>
    /* Kartlar — key bazlı, garanti çalışan seçici (data-testid bu Streamlit
       sürümünde tutmuyordu). Her kart "kart_" ile başlayan benzersiz bir key
       alıyor, buradaki kısmi eşleşme (*=) hepsini birden hedefliyor. */
    div[class*="st-key-kart_"] {
        background-color: #BFCEDE !important;
        border: 1px solid #EFE4D6 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        border-radius: 10px !important;
    }

    /* Yoklama: Var / Yok / İzinli butonları — anlamlı renkler */
    div[class*="st-key-btn_var_"] button {
        background-color: #6FCF97 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    div[class*="st-key-btn_var_"] button:hover {
        background-color: #56B980 !important;
    }
    div[class*="st-key-btn_yok_"] button {
        background-color: #EF7B7B !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    div[class*="st-key-btn_yok_"] button:hover {
        background-color: #E05A5A !important;
    }
    div[class*="st-key-btn_izinli_"] button {
        background-color: #FFC069 !important;
        color: #3D3D3D !important;
        border: none !important;
    }
    div[class*="st-key-btn_izinli_"] button:hover {
        background-color: #FFB347 !important;
    }
    /* Seçili olmayan (secondary) durumda soluk göster */
    div[class*="st-key-btn_var_"] button[kind="secondary"],
    div[class*="st-key-btn_yok_"] button[kind="secondary"],
    div[class*="st-key-btn_izinli_"] button[kind="secondary"] {
        background-color: #F1EDE6 !important;
        color: #8A8175 !important;
    }

    /* Yoklamayı Kaydet — yeşil */
    .st-key-yoklama_kaydet_kutu .stButton button {
        background-color: #4CAF7D !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .st-key-yoklama_kaydet_kutu .stButton button:hover {
        background-color: #3F9968 !important;
    }

    /* Tarih seçici — küçük, sabit genişlik */
    .st-key-yoklama_tarih_kutu .stDateInput {
        max-width: 200px;
    }
</style>
"""


def ogretmen_stilleri_yukle():
    st.markdown(OGRETMEN_CSS, unsafe_allow_html=True)


def _yoklama_durum_key(ogrenci_id):
    return f"yoklama_durum_{ogrenci_id}"


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


def ogretmen_paneli_goster():
    ogretmen_stilleri_yukle()

    ogretmen_id = st.session_state.get("ogretmen_id")

    if not ogretmen_id:
        st.error("Bu hesap bir öğretmen kaydına bağlı değil. Lütfen yöneticinizle iletişime geçin.")
        return

    ogretmen_bilgi = listele("SELECT * FROM ogretmen WHERE ogretmen_id = ?", [ogretmen_id])
    if ogretmen_bilgi.empty:
        st.error("Öğretmen kaydı bulunamadı.")
        return

    ad = ogretmen_bilgi.iloc[0]["ad"]
    soyad = ogretmen_bilgi.iloc[0]["soyad"]

    aktif_bolum = st.session_state.get("ogretmen_aktif_bolum", "sinifim")

    # ============================================================
    # BİLGİLERİM
    # ============================================================
    if aktif_bolum == "bilgilerim":
        st.markdown("### 👤 Bilgilerim")
        col_bos1, col_kart, col_bos2 = st.columns([1, 2, 1])
        with col_kart:
            with st.container(border=True, key="kart_bilgilerim"):
                st.markdown(f"**Ad Soyad:** {ad} {soyad}")
                st.markdown(f"**Kullanıcı Adı:** {st.session_state.get('kullanici_adi', '')}")
                st.markdown(f"**İşe Giriş Tarihi:** {ogretmen_bilgi.iloc[0]['ise_giris_tarihi']}")
                st.markdown(f"**Tecrübe:** {ogretmen_bilgi.iloc[0]['tecrube']} yıl")
                st.markdown(f"**Telefon:** {ogretmen_bilgi.iloc[0]['tel_no']}")
                st.markdown(f"**Adres:** {ogretmen_bilgi.iloc[0]['adres']}")
        return

    # Öğretmenin sınıfları — birçok bölümde kullanılacak
    siniflar = listele("SELECT * FROM sinif WHERE ogretmen_id = ?", [ogretmen_id])
    sinif_idler = [int(x) for x in siniflar["sinif_id"].tolist()] if not siniflar.empty else []

    # ============================================================
    # SINIFIM
    # ============================================================
    if aktif_bolum == "sinifim":
        st.markdown("### 🏫 Sınıfım")
        if siniflar.empty:
            st.info("Henüz size atanmış bir sınıf bulunmuyor.")
        else:
            def _sinif_karti(sinif, idx):
                with st.container(border=True, key=f"kart_sinif_{idx}"):
                    st.markdown(f"### 🏫 {sinif['sinif_adi']}")
                    st.markdown(f"**Yaş Grubu:** {sinif['yas_grubu']}")
                    st.markdown(f"**Kapasite:** {sinif['kapasite']}")
            _grid_goster(list(siniflar.iterrows()), _sinif_karti)
        return

    # ============================================================
    # ÖĞRENCİLERİM
    # ============================================================
    if aktif_bolum == "ogrencilerim":
        st.markdown("### 🧒 Öğrencilerim")
        if not sinif_idler:
            st.info("Sınıfınız olmadığı için öğrenci listesi gösterilemiyor.")
        else:
            yer_tutucular = ", ".join("?" for _ in sinif_idler)
            ogrenciler_detay = listele(f"""
                SELECT o.ad, o.soyad, o.dogum_tarihi, s.sinif_adi,
                       v.ad AS veli_ad, v.soyad AS veli_soyad, v.tel_no AS veli_tel
                FROM ogrenci o
                LEFT JOIN sinif s ON o.sinif_id = s.sinif_id
                LEFT JOIN veli v ON o.veli_id = v.veli_id
                WHERE o.sinif_id IN ({yer_tutucular})
            """, sinif_idler)
            if ogrenciler_detay.empty:
                st.info("Sınıfınızda henüz kayıtlı öğrenci yok.")
            else:
                def _ogrenci_karti(ogr, idx):
                    with st.container(border=True, key=f"kart_ogrenci_{idx}"):
                        st.markdown(f"### 📖 {ogr['ad']} {ogr['soyad']}")
                        st.markdown(f"**Doğum Tarihi:** {ogr['dogum_tarihi']}")
                        st.markdown(f"**Sınıf:** {ogr['sinif_adi']}")
                        st.markdown(f"**Veli:** {ogr['veli_ad']} {ogr['veli_soyad']}")
                        st.markdown(f"**Veli Telefon:** {ogr['veli_tel']}")
                _grid_goster(list(ogrenciler_detay.iterrows()), _ogrenci_karti)
        return

    # ============================================================
    # YOKLAMA
    # ============================================================
    if aktif_bolum == "yoklama":
        st.markdown("### 📋 Yoklama")
        if sinif_idler:
            yer_tutucular = ", ".join("?" for _ in sinif_idler)
            ogrenciler = listele(f"SELECT * FROM ogrenci WHERE sinif_id IN ({yer_tutucular})", sinif_idler)
        else:
            ogrenciler = None

        if not sinif_idler:
            st.info("Sınıfınız olmadığı için yoklama alınamıyor.")
        elif ogrenciler.empty:
            st.info("Sınıfınızda henüz kayıtlı öğrenci yok.")
        else:
            with st.container(key="yoklama_tarih_kutu"):
                secilen_tarih = st.date_input("Tarih", value=date.today(), key="yoklama_tarih")
            st.markdown("")

            def _yoklama_karti(ogrenci, idx):
                o_id = int(ogrenci["ogrenci_id"])
                durum_key = _yoklama_durum_key(o_id)
                if durum_key not in st.session_state:
                    st.session_state[durum_key] = "var"

                with st.container(border=True, key=f"kart_yoklama_{idx}"):
                    st.markdown(f"**{ogrenci['ad']} {ogrenci['soyad']}**")
                    if st.button(
                        "Var", key=f"btn_var_{o_id}", use_container_width=True,
                        type="primary" if st.session_state[durum_key] == "var" else "secondary",
                    ):
                        st.session_state[durum_key] = "var"
                        st.rerun()
                    if st.button(
                        "Yok", key=f"btn_yok_{o_id}", use_container_width=True,
                        type="primary" if st.session_state[durum_key] == "yok" else "secondary",
                    ):
                        st.session_state[durum_key] = "yok"
                        st.rerun()
                    if st.button(
                        "İzinli", key=f"btn_izinli_{o_id}", use_container_width=True,
                        type="primary" if st.session_state[durum_key] == "izinli" else "secondary",
                    ):
                        st.session_state[durum_key] = "izinli"
                        st.rerun()

            _grid_goster(list(ogrenciler.iterrows()), _yoklama_karti)

            st.markdown("")
            with st.container(key="yoklama_kaydet_kutu"):
                col_kaydet, col_bos = st.columns([1, 4])
                with col_kaydet:
                    kaydet_tiklandi = st.button("💾 Kaydet")
            if kaydet_tiklandi:
                try:
                    for _, ogrenci in ogrenciler.iterrows():
                        o_id = int(ogrenci["ogrenci_id"])
                        durum = st.session_state.get(_yoklama_durum_key(o_id), "var")
                        mevcut = listele(
                            "SELECT * FROM yoklama WHERE ogrenci_id = ? AND tarih = ?",
                            [o_id, secilen_tarih],
                        )
                        if mevcut.empty:
                            calistir(
                                "INSERT INTO yoklama (ogrenci_id, tarih, durum) VALUES (?, ?, ?)",
                                [o_id, secilen_tarih, durum],
                            )
                        else:
                            calistir(
                                "UPDATE yoklama SET durum = ? WHERE ogrenci_id = ? AND tarih = ?",
                                [durum, o_id, secilen_tarih],
                            )
                    st.success("Yoklama kaydedildi.")
                except Exception as e:
                    st.error(f"Yoklama kaydedilemedi. ({e})")
        return

    # ============================================================
    # DERS PROGRAMI
    # ============================================================
    if aktif_bolum == "ders_programi":
        st.markdown("### 📅 Ders Programı")
        dersler = listele("""
            SELECT d.ders_adi, d.baslangic_saati, d.bitis_saati, s.sinif_adi
            FROM ders d
            LEFT JOIN sinif s ON d.sinif_id = s.sinif_id
            WHERE d.ogretmen_id = ?
        """, [ogretmen_id])
        if dersler.empty:
            st.info("Henüz size atanmış bir ders bulunmuyor.")
        else:
            def _ders_karti(ders, idx):
                with st.container(border=True, key=f"kart_ders_{idx}"):
                    st.markdown(f"### 📚 {ders['ders_adi']}")
                    st.markdown(f"**Saat:** {ders['baslangic_saati']} - {ders['bitis_saati']}")
                    st.markdown(f"**Sınıf:** {ders['sinif_adi']}")
            _grid_goster(list(dersler.iterrows()), _ders_karti)
        return

    # ============================================================
    # ETKİNLİKLER
    # ============================================================
    if aktif_bolum == "etkinlikler":
        st.markdown("### 🎉 Etkinlikler")
        etkinlikler = listele("""
            SELECT e.tarih, e.saat, e.baslik, e.aciklama, s.sinif_adi
            FROM etkinlik e
            LEFT JOIN sinif s ON e.sinif_id = s.sinif_id
            WHERE e.ogretmen_id = ?
        """, [ogretmen_id])
        if etkinlikler.empty:
            st.info("Henüz bir etkinlik eklenmemiş.")
        else:
            def _etkinlik_karti(etk, idx):
                with st.container(border=True, key=f"kart_etkinlik_{idx}"):
                    st.markdown(f"### 🎉 {etk['baslik']}")
                    st.markdown(f"**Tarih:** {etk['tarih']} {etk['saat']}")
                    st.markdown(f"**Sınıf:** {etk['sinif_adi']}")
                    if etk['aciklama']:
                        st.markdown(f"{etk['aciklama']}")
            _grid_goster(list(etkinlikler.iterrows()), _etkinlik_karti)
        return