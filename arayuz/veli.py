"""
Veli Paneli — giriş yapan veli kendi çocuğunun/çocuklarının bilgilerini,
yoklama geçmişini, ödeme durumunu ve sınıf etkinliklerini görür.

Not: Artık sekmeler (tabs) yerine header'daki navigasyon linklerinden
gelen st.session_state.veli_aktif_bolum değerine göre içerik gösteriyor
— hangi bölüm seçiliyse (Çocuklarım, Yoklama, vb.) sadece o gösterilir.

Not: Veli sadece GÖRÜNTÜLER — öğretmenin aksine yoklama girişi yapmaz,
kayıt eklemez/silmez. Tüm görünümler kart formatında, ID sütunu yok.

Kartlar 4'lü grid düzeninde (satır başına en fazla 4 kart, taşan kartlar
yeni satıra geçer).
"""

import streamlit as st
from veritabani import listele, calistir

VELI_CSS = """
<style>
    /* Kartlar — key bazlı, garanti çalışan seçici */
    div[class*="st-key-kart_"] {
        background-color: #BFCEDE !important;
        border: 1px solid #EFE4D6 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        border-radius: 10px !important;
    }

    /* Çocuk filtre butonları — küçük, pill (hap) görünümü, yan yana doğal genişlikte */
    .st-key-odeme_filtre_kutu, .st-key-etkinlik_filtre_kutu,
    .st-key-cocuk_filtre_kutu, .st-key-yoklama_filtre_kutu {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .st-key-odeme_filtre_kutu > div, .st-key-etkinlik_filtre_kutu > div,
    .st-key-cocuk_filtre_kutu > div, .st-key-yoklama_filtre_kutu > div,
    .st-key-odeme_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-etkinlik_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-cocuk_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-yoklama_filtre_kutu div[data-testid="stElementContainer"],
    .st-key-odeme_filtre_kutu div[data-testid="stVerticalBlock"],
    .st-key-etkinlik_filtre_kutu div[data-testid="stVerticalBlock"],
    .st-key-cocuk_filtre_kutu div[data-testid="stVerticalBlock"],
    .st-key-yoklama_filtre_kutu div[data-testid="stVerticalBlock"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    .st-key-odeme_filtre_kutu .stButton button,
    .st-key-etkinlik_filtre_kutu .stButton button,
    .st-key-cocuk_filtre_kutu .stButton button,
    .st-key-yoklama_filtre_kutu .stButton button {
        border-radius: 9999px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.3rem 0.9rem !important;
        white-space: nowrap;
    }
    .st-key-odeme_filtre_kutu .stButton button[kind="secondary"],
    .st-key-etkinlik_filtre_kutu .stButton button[kind="secondary"],
    .st-key-cocuk_filtre_kutu .stButton button[kind="secondary"],
    .st-key-yoklama_filtre_kutu .stButton button[kind="secondary"] {
        background-color: #FFF6EC !important;
        border: 1px solid #F0E4D8 !important;
        color: #8A8175 !important;
    }
    .st-key-odeme_filtre_kutu .stButton button[kind="secondary"]:hover,
    .st-key-etkinlik_filtre_kutu .stButton button[kind="secondary"]:hover,
    .st-key-cocuk_filtre_kutu .stButton button[kind="secondary"]:hover,
    .st-key-yoklama_filtre_kutu .stButton button[kind="secondary"]:hover {
        border-color: #FFB86B !important;
        color: #D97B3D !important;
    }
    .st-key-odeme_filtre_kutu .stButton button[kind="primary"],
    .st-key-etkinlik_filtre_kutu .stButton button[kind="primary"],
    .st-key-cocuk_filtre_kutu .stButton button[kind="primary"],
    .st-key-yoklama_filtre_kutu .stButton button[kind="primary"] {
        background-color: #D97B3D !important;
        border: 1px solid #D97B3D !important;
    }
</style>
"""


def veli_stilleri_yukle():
    st.markdown(VELI_CSS, unsafe_allow_html=True)


def _filtrelenecek_cocuklar(cocuklar, filtre_key):
    """Birden fazla çocuk varsa tıklanabilir 'pill' butonlarla filtre
    gösterir (seçili olan vurgulu), tek çocuk varsa filtre göstermeden
    direkt o çocuğu döndürür."""
    if len(cocuklar) <= 1:
        return cocuklar

    secim_key = f"{filtre_key}_secim"
    if secim_key not in st.session_state:
        st.session_state[secim_key] = "Tümü"

    secenekler = ["Tümü"] + [f"{c['ad']} {c['soyad']}" for _, c in cocuklar.iterrows()]
    with st.container(key=f"{filtre_key}_kutu"):
        for secenek in secenekler:
            if st.button(
                secenek,
                key=f"{filtre_key}_btn_{secenek}",
                type="primary" if st.session_state[secim_key] == secenek else "secondary",
            ):
                st.session_state[secim_key] = secenek
                st.rerun()

    secim = st.session_state[secim_key]
    if secim == "Tümü":
        return cocuklar
    return cocuklar[cocuklar.apply(lambda r: f"{r['ad']} {r['soyad']}" == secim, axis=1)]


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


def veli_paneli_goster():
    veli_stilleri_yukle()

    veli_id = st.session_state.get("veli_id")

    if not veli_id:
        st.error("Bu hesap bir veli kaydına bağlı değil. Lütfen yöneticinizle iletişime geçin.")
        return

    veli_bilgi = listele("SELECT * FROM veli WHERE veli_id = ?", [veli_id])
    if veli_bilgi.empty:
        st.error("Veli kaydı bulunamadı.")
        return

    ad = veli_bilgi.iloc[0]["ad"]
    soyad = veli_bilgi.iloc[0]["soyad"]

    aktif_bolum = st.session_state.get("veli_aktif_bolum", "cocuklarim")

    cocuklar = listele("""
        SELECT o.ogrenci_id, o.ad, o.soyad, o.dogum_tarihi, s.sinif_adi,
               og.ad AS ogretmen_ad, og.soyad AS ogretmen_soyad
        FROM ogrenci o
        LEFT JOIN sinif s ON o.sinif_id = s.sinif_id
        LEFT JOIN ogretmen og ON s.ogretmen_id = og.ogretmen_id
        WHERE o.veli_id = ?
    """, [veli_id])
    cocuk_idler = [int(x) for x in cocuklar["ogrenci_id"].tolist()] if not cocuklar.empty else []

    # ============================================================
    # BİLGİLERİM
    # ============================================================
    if aktif_bolum == "bilgilerim":
        st.markdown("### 👤 Bilgilerim")
        col_kart, col_bos = st.columns([2, 3])
        with col_kart:
            with st.container(border=True, key="kart_bilgilerim"):
                st.markdown(f"**Ad Soyad:** {ad} {soyad}")
                st.markdown(f"**Kullanıcı Adı:** {st.session_state.get('kullanici_adi', '')}")
                st.markdown(f"**Telefon:** {veli_bilgi.iloc[0]['tel_no']}")
                st.markdown(f"**Adres:** {veli_bilgi.iloc[0]['adres']}")
        return

    # ============================================================
    # ÇOCUKLARIM
    # ============================================================
    if aktif_bolum == "cocuklarim":
        st.markdown("### 🧒 Çocuklarım")
        if cocuklar.empty:
            st.info("Sisteme kayıtlı bir çocuğunuz bulunmuyor.")
        else:
            gosterilecek_cocuk = _filtrelenecek_cocuklar(cocuklar, "cocuk_filtre")

            def _cocuk_karti(c, idx):
                with st.container(border=True, key=f"kart_cocuk_{idx}"):
                    st.markdown(f"### 🧒 {c['ad']} {c['soyad']}")
                    st.markdown(f"**Doğum Tarihi:** {c['dogum_tarihi']}")
                    st.markdown(f"**Sınıf:** {c['sinif_adi'] or 'Henüz atanmadı'}")
                    if c["ogretmen_ad"]:
                        st.markdown(f"**Öğretmeni:** {c['ogretmen_ad']} {c['ogretmen_soyad']}")
                    else:
                        st.markdown("**Öğretmeni:** Henüz atanmadı")
            _grid_goster(list(gosterilecek_cocuk.iterrows()), _cocuk_karti)
        return

    # ============================================================
    # YOKLAMA
    # ============================================================
    if aktif_bolum == "yoklama":
        st.markdown("### 📋 Yoklama")
        if not cocuk_idler:
            st.info("Sisteme kayıtlı bir çocuğunuz bulunmuyor.")
        else:
            gosterilecek_yoklama = _filtrelenecek_cocuklar(cocuklar, "yoklama_filtre")

            def _yoklama_ozet_karti(c, idx):
                st.markdown(f"#### 🧒 {c['ad']} {c['soyad']}")
                yoklamalar = listele(
                    "SELECT tarih, durum FROM yoklama WHERE ogrenci_id = ? ORDER BY tarih DESC",
                    [int(c["ogrenci_id"])],
                )
                if yoklamalar.empty:
                    st.info("Kayıt yok.")
                else:
                    for j, (_, y) in enumerate(yoklamalar.iterrows()):
                        durum_renk = {"var": "🟢", "yok": "🔴", "izinli": "🟡"}.get(str(y["durum"]).lower(), "⚪")
                        with st.container(border=True, key=f"kart_yoklama_{idx}_{j}"):
                            st.markdown(f"**{y['tarih']}**")
                            st.markdown(f"{durum_renk} {str(y['durum']).capitalize()}")
            _grid_goster(list(gosterilecek_yoklama.iterrows()), _yoklama_ozet_karti)
        return

    # ============================================================
    # ÖDEMELER
    # ============================================================
    if aktif_bolum == "odemeler":
        st.markdown("### 💳 Ödemeler")
        if not cocuk_idler:
            st.info("Sisteme kayıtlı bir çocuğunuz bulunmuyor.")
        else:
            gosterilecek = _filtrelenecek_cocuklar(cocuklar, "odeme_filtre")

            def _odeme_ozet_karti(c, idx):
                st.markdown(f"#### 🧒 {c['ad']} {c['soyad']}")
                odemeler = listele(
                    "SELECT * FROM odemeler WHERE ogrenci_id = ? ORDER BY tarih DESC",
                    [int(c["ogrenci_id"])],
                )
                if odemeler.empty:
                    st.info("Kayıt yok.")
                else:
                    for j, (_, o) in enumerate(odemeler.iterrows()):
                        with st.container(border=True, key=f"kart_odeme_{idx}_{j}"):
                            st.markdown(f"**Tarih:** {o['tarih']}")
                            st.markdown(f"**Ödeme Şekli:** {o['odeme_sekli']}")
                            st.markdown(f"**Tutar:** {o['odeme_tutari']} ₺")
                            st.markdown(f"**Durum:** {o['odeme_durumu']}")
                            st.markdown(f"**Kalan Tutar:** {o['kalan_tutar']} ₺")
                            st.markdown(f"**Kalan Taksit:** {o['kalan_taksit_sayisi']} / {o['taksit_sayisi']}")
            _grid_goster(list(gosterilecek.iterrows()), _odeme_ozet_karti)
        return

    # ============================================================
    # ETKİNLİKLER
    # ============================================================
    if aktif_bolum == "etkinlikler":
        st.markdown("### 🎉 Etkinlikler")
        if not cocuk_idler:
            st.info("Sisteme kayıtlı bir çocuğunuz bulunmuyor.")
        else:
            gosterilecek = _filtrelenecek_cocuklar(cocuklar, "etkinlik_filtre")

            def _etkinlik_ozet_karti(c, idx):
                st.markdown(f"#### 🧒 {c['ad']} {c['soyad']}")
                etkinlikler = listele("""
                    SELECT e.tarih, e.saat, e.baslik, e.aciklama
                    FROM etkinlik e
                    JOIN ogrenci o ON e.sinif_id = o.sinif_id
                    WHERE o.ogrenci_id = ?
                    ORDER BY e.tarih DESC
                """, [int(c["ogrenci_id"])])
                if etkinlikler.empty:
                    st.info("Kayıt yok.")
                else:
                    for j, (_, e) in enumerate(etkinlikler.iterrows()):
                        with st.container(border=True, key=f"kart_etkinlik_{idx}_{j}"):
                            st.markdown(f"**{e['baslik']}**")
                            st.markdown(f"{e['tarih']} {e['saat']}")
                            if e["aciklama"]:
                                st.markdown(f"{e['aciklama']}")
            _grid_goster(list(gosterilecek.iterrows()), _etkinlik_ozet_karti)
        return