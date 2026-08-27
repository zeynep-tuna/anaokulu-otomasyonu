"""
Admin Paneli — Modern ve Optimize Edilmiş Tasarım
Renkler Ana Sayfa'nın paletiyle uyumlu: turuncu (#D97B3D/#FFB86B), krem (#FAFAF7)

Her tablo İKİ sorgu kullanır:
  - "goruntuleme_sorgusu": ekranda gösterilen, ID YOK, JOIN'lerle isimlendirilmiş sorgu
  - "gosterge_sorgusu": silme işleminde, kaydı TANIYAN bir metne göre (örn. "Ecrin Yılmaz")
    seçim yapmak için — kullanıcı hiçbir zaman ID görmüyor/girmiyor.

TÜM tablolar tek bir genel fonksiyonla (genel_tablo_yonet) yönetiliyor —
her kayıt kart görünümünde, ✏️ Güncelle butonuyla satır bazlı düzenlenebiliyor.
Her tablonun "alanlar" listesindeki ilişkisel sütunlar (veli_id, sinif_id,
ogretmen_id, personel_id, rol_id gibi) "iliski" tipiyle tanımlanır — kullanıcı
ham ID yazmak yerine isimden seçer, opsiyonel ilişkilerde "— Yok —" seçeneği
gerçek NULL gönderir (yanlışlıkla geçersiz bir ID/0 girilmesini önler).
"""

import datetime
import time
import streamlit as st
from veritabani import listele, calistir

ADMIN_CSS = """
<style>
    /* 1. Üst Boşlukları ve Streamlit Araç Çubuklarını Sıfırla */
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

    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewBlockContainer"],
    .main .block-container,
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        background-color: #FFFFFF !important;
    }

    /* ============ HEADER ALANI ============ */
    .st-key-admin_header_cubugu {
        background-color: #5C6B7A;
        padding: 0.75rem 2.2rem;
        border-bottom: 1px solid #4A5766;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        margin: 0 !important;
        margin-top: -2.2rem !important;
    }

    /* Tablo Renginde Google Tarzı Arama Çubuğu */
    .st-key-admin_header_cubugu .stTextInput,
    .st-key-admin_header_cubugu div[data-testid="stTextInputRootElement"],
    .st-key-admin_header_cubugu div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .st-key-admin_header_cubugu .stTextInput input {
        background-color: #CDDAE7 !important;
        color: #2D3748 !important;
        border: 1px solid #B8C7D6 !important;
        border-radius: 9999px !important;
        padding: 0.55rem 1.25rem 0.55rem 2.6rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%235C6B7A"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>') !important;
        background-repeat: no-repeat !important;
        background-position: 0.85rem center !important;
        background-size: 1.25rem 1.25rem !important;
    }
    .st-key-admin_header_cubugu .stTextInput input::placeholder {
        color: #5C6B7A !important;
    }

    /* Bildirim butonu */
    .st-key-header_bildirim button,
    div[data-testid="stButton"].st-key-header_bildirim > button {
        background-color: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
        padding: 0.45rem 0.6rem !important;
        font-size: 0.95rem !important;
        color: #FFFFFF !important;
        box-shadow: none !important;
        width: 100% !important;
    }
    .st-key-header_bildirim button:hover {
        background-color: rgba(255,255,255,0.22) !important;
        border-color: rgba(255,255,255,0.4) !important;
    }

    /* Şifre Değiştir + Çıkış Yap Butonları */
    .st-key-admin_sifre button {
        background-color: rgba(255,255,255,0.12) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        padding: 0.45rem 0.6rem !important;
        width: 100% !important;
    }
    .st-key-admin_sifre button:hover {
        background-color: rgba(255,255,255,0.22) !important;
    }
    .st-key-admin_cikis button {
        background-color: rgba(255,255,255,0.12) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.45rem 0.9rem !important;
        width: 100% !important;
    }
    .st-key-admin_cikis button:hover {
        background-color: rgba(255,255,255,0.22) !important;
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background-color: #5C6B7A !important;
        border-right: 1px solid #4A5766 !important;
        padding: 0 !important;
    }

    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"] .block-container,
    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
        margin-top: -1.6rem !important;
        width: 100% !important;
    }

    /* Gökkuşağı + Minik Adımlar */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.8rem;
        padding: 0.6rem 0.4rem 1rem 0.4rem !important;
        margin: 0 0 1.1rem 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        width: 100% !important;
    }
    .brand-logo-icon {
        font-size: 3rem;
        line-height: 1;
        display: flex;
        align-items: center;
    }
    .brand-title-text {
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
        color: #FFFFFF !important;
        font-weight: 800;
        line-height: 1.12;
    }
    .brand-title-text .part-1,
    .brand-title-text .part-2 {
        font-size: 1.85rem;
    }

    /* Sidebar Menü Butonları */
    section[data-testid="stSidebar"] div[data-testid="stElementContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton {
        padding: 0 !important;
        margin-bottom: 0.35rem !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        background-color: transparent;
        color: #CDDAE7;
        border: none !important;
        border-radius: 12px;
        padding: 0.85rem 1rem !important;
        font-size: 1.18rem !important;
        font-weight: 600 !important;
        transition: all 0.15s ease-in-out;
    }
    section[data-testid="stSidebar"] .stButton button > div {
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton button p {
        font-size: 1.18rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255,255,255,0.12);
        color: #FFFFFF;
    }

    /* Seçili Menü Butonu */
    section[data-testid="stSidebar"] .st-key-menu_aktif .stButton button {
        background-color: #CDDAE7 !important;
        color: #5C6B7A !important;
        font-weight: 800 !important;
    }

    /* ============ İÇERİK ALANI ============ */
    .st-key-admin_icerik_alani {
        padding: 1.8rem 2.2rem;
        background-color: #FFFFFF;
    }
    .admin-icerik-baslik {
        color: #D97B3D;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #B8C7D6 !important;
        border-radius: 12px !important;
        background-color: #CDDAE7 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #F0E4D8 !important;
        border-radius: 12px !important;
    }
    /* Tüm tabloların kayıt kartları — key bazlı, garanti çalışan seçici */
    div[class*="st-key-kart_"] {
        background-color: #CDDAE7 !important;
        border: 1px solid #B8C7D6 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
</style>
"""


def admin_stilleri_yukle():
    st.markdown(ADMIN_CSS, unsafe_allow_html=True)


# ============================================================
# HER TABLONUN TANIMI
#   goruntuleme_sorgusu: ID İÇERMEYEN, JOIN'lerle isimlendirilmiş SELECT
#   gosterge_sorgusu: silme seçimi için (id_kolon + tek bir "gosterge" metni)
#   alanlar: "Yeni Kayıt Ekle" formu için (ham tablo sütunları, INSERT için)
# ============================================================
TABLO_TANIMLARI = {
    "ogrenci": {
        "isim": "Öğrenciler",
        "ikon": "👥",
        "id_kolon": "ogrenci_id",
        "goruntuleme_sorgusu": """
            SELECT o.ad AS "Ad", o.soyad AS "Soyad",
                   o.dogum_tarihi AS "Doğum Tarihi", o.kayit_tarihi AS "Kayıt Tarihi",
                   v.ad AS "Veli Adı", v.soyad AS "Veli Soyadı",
                   s.sinif_adi AS "Sınıf"
            FROM ogrenci o
            LEFT JOIN veli v ON o.veli_id = v.veli_id
            LEFT JOIN sinif s ON o.sinif_id = s.sinif_id
        """,
        "gosterge_sorgusu": "SELECT ogrenci_id, ad + ' ' + soyad AS gosterge FROM ogrenci",
        "alanlar": [
            ("ad", "text", "Ad", None),
            ("soyad", "text", "Soyad", None),
            ("dogum_tarihi", "date", "Doğum Tarihi", None),
            ("kayit_tarihi", "date", "Kayıt Tarihi", None),
            ("veli_id", "iliski", "Veli", {"tablo": "veli", "id_kolon": "veli_id", "format": "{ad} {soyad}", "zorunlu": True}),
            ("sinif_id", "iliski", "Sınıf", {"tablo": "sinif", "id_kolon": "sinif_id", "format": "{sinif_adi}", "zorunlu": False}),
        ],
    },
    "veli": {
        "isim": "Veliler",
        "ikon": "👨‍👩‍👧",
        "id_kolon": "veli_id",
        "goruntuleme_sorgusu": """
            SELECT ad AS "Ad", soyad AS "Soyad", tel_no AS "Telefon No", adres AS "Adres"
            FROM veli
        """,
        "gosterge_sorgusu": "SELECT veli_id, ad + ' ' + soyad AS gosterge FROM veli",
        "alanlar": [
            ("ad", "text", "Ad", None),
            ("soyad", "text", "Soyad", None),
            ("tel_no", "text", "Telefon No", None),
            ("adres", "text", "Adres", None),
        ],
    },
    "ogretmen": {
        "isim": "Öğretmenler",
        "ikon": "🩺",
        "id_kolon": "ogretmen_id",
        "goruntuleme_sorgusu": """
            SELECT ad AS "Ad", soyad AS "Soyad", tel_no AS "Telefon No", adres AS "Adres",
                   ise_giris_tarihi AS "İşe Giriş Tarihi", tecrube AS "Tecrübe (yıl)"
            FROM ogretmen
        """,
        "gosterge_sorgusu": "SELECT ogretmen_id, ad + ' ' + soyad AS gosterge FROM ogretmen",
        "alanlar": [
            ("ad", "text", "Ad", None),
            ("soyad", "text", "Soyad", None),
            ("tel_no", "text", "Telefon No", None),
            ("adres", "text", "Adres", None),
            ("ise_giris_tarihi", "date", "İşe Giriş Tarihi", None),
            ("tecrube", "number", "Tecrübe (yıl)", None),
        ],
    },
    "sinif": {
        "isim": "Sınıflar",
        "ikon": "🏫",
        "id_kolon": "sinif_id",
        "goruntuleme_sorgusu": """
            SELECT s.sinif_adi AS "Sınıf Adı", s.yas_grubu AS "Yaş Grubu",
                   s.kapasite AS "Kapasite",
                   og.ad AS "Öğretmen Adı", og.soyad AS "Öğretmen Soyadı"
            FROM sinif s
            LEFT JOIN ogretmen og ON s.ogretmen_id = og.ogretmen_id
        """,
        "gosterge_sorgusu": "SELECT sinif_id, sinif_adi AS gosterge FROM sinif",
        "alanlar": [
            ("sinif_adi", "text", "Sınıf Adı", None),
            ("yas_grubu", "text", "Yaş Grubu", None),
            ("kapasite", "number", "Kapasite", None),
            ("ogretmen_id", "iliski", "Öğretmen", {"tablo": "ogretmen", "id_kolon": "ogretmen_id", "format": "{ad} {soyad}", "zorunlu": False}),
        ],
    },
    "odemeler": {
        "isim": "Ödemeler",
        "ikon": "💳",
        "id_kolon": "odemeler_id",
        "goruntuleme_sorgusu": """
            SELECT o.ad AS "Öğrenci Adı", o.soyad AS "Öğrenci Soyadı",
                   od.odeme_tutari AS "Ödeme Tutarı", od.tarih AS "Tarih",
                   od.odeme_sekli AS "Ödeme Şekli", od.odeme_durumu AS "Durum",
                   od.toplam_tutar AS "Toplam Tutar", od.kalan_tutar AS "Kalan Tutar",
                   od.taksit_sayisi AS "Taksit Sayısı", od.kalan_taksit_sayisi AS "Kalan Taksit"
            FROM odemeler od
            LEFT JOIN ogrenci o ON od.ogrenci_id = o.ogrenci_id
        """,
        "gosterge_sorgusu": """
            SELECT od.odemeler_id, o.ad + ' ' + o.soyad + ' - ' + CONVERT(varchar, od.tarih) AS gosterge
            FROM odemeler od
            LEFT JOIN ogrenci o ON od.ogrenci_id = o.ogrenci_id
        """,
        "alanlar": [
            ("odeme_tutari", "decimal", "Ödeme Tutarı", None),
            ("tarih", "date", "Tarih", None),
            ("odeme_sekli", "text", "Ödeme Şekli", None),
            ("odeme_durumu", "text", "Ödeme Durumu", None),
            ("toplam_tutar", "decimal", "Toplam Tutar", None),
            ("kalan_tutar", "decimal", "Kalan Tutar", None),
            ("taksit_sayisi", "number", "Taksit Sayısı", None),
            ("kalan_taksit_sayisi", "number", "Kalan Taksit Sayısı", None),
            ("ogrenci_id", "iliski", "Öğrenci", {"tablo": "ogrenci", "id_kolon": "ogrenci_id", "format": "{ad} {soyad}", "zorunlu": True}),
            ("personel_id", "iliski", "Personel", {"tablo": "personel", "id_kolon": "personel_id", "format": "{ad} {soyad}", "zorunlu": False}),
        ],
    },
    "ders": {
        "isim": "Ders Programı",
        "ikon": "📅",
        "id_kolon": "ders_id",
        "goruntuleme_sorgusu": """
            SELECT d.ders_adi AS "Ders Adı", d.baslangic_saati AS "Başlangıç",
                   d.bitis_saati AS "Bitiş",
                   og.ad AS "Öğretmen Adı", og.soyad AS "Öğretmen Soyadı",
                   s.sinif_adi AS "Sınıf"
            FROM ders d
            LEFT JOIN ogretmen og ON d.ogretmen_id = og.ogretmen_id
            LEFT JOIN sinif s ON d.sinif_id = s.sinif_id
        """,
        "gosterge_sorgusu": "SELECT ders_id, ders_adi AS gosterge FROM ders",
        "alanlar": [
            ("ders_adi", "text", "Ders Adı", None),
            ("baslangic_saati", "time", "Başlangıç Saati", None),
            ("bitis_saati", "time", "Bitiş Saati", None),
            ("ogretmen_id", "iliski", "Öğretmen", {"tablo": "ogretmen", "id_kolon": "ogretmen_id", "format": "{ad} {soyad}", "zorunlu": True}),
            ("sinif_id", "iliski", "Sınıf", {"tablo": "sinif", "id_kolon": "sinif_id", "format": "{sinif_adi}", "zorunlu": True}),
        ],
    },
    "etkinlik": {
        "isim": "Etkinlikler",
        "ikon": "📄",
        "id_kolon": "etkinlik_id",
        "goruntuleme_sorgusu": """
            SELECT e.tarih AS "Tarih", e.saat AS "Saat", e.baslik AS "Başlık",
                   e.aciklama AS "Açıklama",
                   og.ad AS "Öğretmen Adı", og.soyad AS "Öğretmen Soyadı",
                   s.sinif_adi AS "Sınıf"
            FROM etkinlik e
            LEFT JOIN ogretmen og ON e.ogretmen_id = og.ogretmen_id
            LEFT JOIN sinif s ON e.sinif_id = s.sinif_id
        """,
        "gosterge_sorgusu": "SELECT etkinlik_id, baslik + ' - ' + CONVERT(varchar, tarih) AS gosterge FROM etkinlik",
        "alanlar": [
            ("tarih", "date", "Tarih", None),
            ("saat", "time", "Saat", None),
            ("baslik", "text", "Başlık", None),
            ("aciklama", "textarea", "Açıklama", None),
            ("ogretmen_id", "iliski", "Öğretmen (varsa)", {"tablo": "ogretmen", "id_kolon": "ogretmen_id", "format": "{ad} {soyad}", "zorunlu": False}),
            ("sinif_id", "iliski", "Sınıf (varsa)", {"tablo": "sinif", "id_kolon": "sinif_id", "format": "{sinif_adi}", "zorunlu": False}),
        ],
    },
    "yoklama": {
        "isim": "Yoklama",
        "ikon": "📊",
        "id_kolon": "yoklama_id",
        "goruntuleme_sorgusu": """
            SELECT o.ad AS "Öğrenci Adı", o.soyad AS "Öğrenci Soyadı",
                   y.tarih AS "Tarih", y.durum AS "Durum"
            FROM yoklama y
            LEFT JOIN ogrenci o ON y.ogrenci_id = o.ogrenci_id
        """,
        "gosterge_sorgusu": """
            SELECT y.yoklama_id, o.ad + ' ' + o.soyad + ' - ' + CONVERT(varchar, y.tarih) AS gosterge
            FROM yoklama y
            LEFT JOIN ogrenci o ON y.ogrenci_id = o.ogrenci_id
        """,
        "alanlar": [
            ("ogrenci_id", "iliski", "Öğrenci", {"tablo": "ogrenci", "id_kolon": "ogrenci_id", "format": "{ad} {soyad}", "zorunlu": True}),
            ("tarih", "date", "Tarih", None),
            ("durum", "text", "Durum (var/yok/izinli)", None),
        ],
    },
    "personel": {
        "isim": "Personel",
        "ikon": "👥",
        "id_kolon": "personel_id",
        "goruntuleme_sorgusu": """
            SELECT ad AS "Ad", soyad AS "Soyad", tel_no AS "Telefon No", adres AS "Adres",
                   tecrube AS "Tecrübe (yıl)", ise_giris_tarihi AS "İşe Giriş Tarihi",
                   pozisyon AS "Pozisyon", gorev AS "Görev"
            FROM personel
        """,
        "gosterge_sorgusu": "SELECT personel_id, ad + ' ' + soyad AS gosterge FROM personel",
        "alanlar": [
            ("ad", "text", "Ad", None),
            ("soyad", "text", "Soyad", None),
            ("tel_no", "text", "Telefon No", None),
            ("adres", "text", "Adres", None),
            ("tecrube", "number", "Tecrübe (yıl)", None),
            ("ise_giris_tarihi", "date", "İşe Giriş Tarihi", None),
            ("pozisyon", "text", "Pozisyon", None),
            ("gorev", "text", "Görev", None),
        ],
    },
    "saglik_listesi": {
        "isim": "Sağlık Takibi",
        "ikon": "🩺",
        "id_kolon": "saglik_listesi_id",
        "goruntuleme_sorgusu": """
            SELECT o.ad AS "Öğrenci Adı", o.soyad AS "Öğrenci Soyadı",
                   sl.alerji AS "Alerji", sl.kronik_hastalik AS "Kronik Hastalık",
                   sl.acil_durum_notu AS "Acil Durum Notu", sl.acil_durum_tel AS "Acil Durum Telefonu"
            FROM saglik_listesi sl
            LEFT JOIN ogrenci o ON sl.ogrenci_id = o.ogrenci_id
        """,
        "gosterge_sorgusu": """
            SELECT sl.saglik_listesi_id, o.ad + ' ' + o.soyad AS gosterge
            FROM saglik_listesi sl
            LEFT JOIN ogrenci o ON sl.ogrenci_id = o.ogrenci_id
        """,
        "alanlar": [
            ("alerji", "text", "Alerji", None),
            ("kronik_hastalik", "text", "Kronik Hastalık", None),
            ("acil_durum_notu", "textarea", "Acil Durum Notu", None),
            ("acil_durum_tel", "text", "Acil Durum Telefonu", None),
            ("ogrenci_id", "iliski", "Öğrenci", {"tablo": "ogrenci", "id_kolon": "ogrenci_id", "format": "{ad} {soyad}", "zorunlu": True}),
            ("personel_id", "iliski", "Personel (varsa)", {"tablo": "personel", "id_kolon": "personel_id", "format": "{ad} {soyad}", "zorunlu": False}),
        ],
    },
    "yemek_listesi": {
        "isim": "Yemek Listesi",
        "ikon": "🍴",
        "id_kolon": "yemek_listesi_id",
        "goruntuleme_sorgusu": """
            SELECT yl.yemek_adi AS "Yemek Adı", yl.yemek_turu AS "Yemek Türü", yl.tarih AS "Tarih",
                   p.ad AS "Sorumlu Adı", p.soyad AS "Sorumlu Soyadı"
            FROM yemek_listesi yl
            LEFT JOIN personel p ON yl.personel_id = p.personel_id
        """,
        "gosterge_sorgusu": "SELECT yemek_listesi_id, yemek_adi + ' - ' + CONVERT(varchar, tarih) AS gosterge FROM yemek_listesi",
        "alanlar": [
            ("yemek_adi", "text", "Yemek Adı", None),
            ("yemek_turu", "text", "Yemek Türü", None),
            ("tarih", "date", "Tarih", None),
            ("personel_id", "iliski", "Personel", {"tablo": "personel", "id_kolon": "personel_id", "format": "{ad} {soyad}", "zorunlu": True}),
        ],
    },
    "temizlik_listesi": {
        "isim": "Temizlik Takibi",
        "ikon": "🧹",
        "id_kolon": "temizlik_listesi_id",
        "goruntuleme_sorgusu": """
            SELECT tl.alan AS "Alan", tl.tarih AS "Tarih", tl.durum AS "Durum",
                   p.ad AS "Sorumlu Adı", p.soyad AS "Sorumlu Soyadı"
            FROM temizlik_listesi tl
            LEFT JOIN personel p ON tl.personel_id = p.personel_id
        """,
        "gosterge_sorgusu": "SELECT temizlik_listesi_id, alan + ' - ' + CONVERT(varchar, tarih) AS gosterge FROM temizlik_listesi",
        "alanlar": [
            ("alan", "text", "Alan", None),
            ("tarih", "date", "Tarih", None),
            ("durum", "text", "Durum", None),
            ("personel_id", "iliski", "Personel", {"tablo": "personel", "id_kolon": "personel_id", "format": "{ad} {soyad}", "zorunlu": True}),
        ],
    },
    "kullanici": {
        "isim": "Kullanıcılar",
        "ikon": "⚙️",
        "id_kolon": "kullanici_id",
        "goruntuleme_sorgusu": """
            SELECT k.kullanici_adi AS "Kullanıcı Adı", k.tel_no AS "Telefon No",
                   r.rol_adi AS "Rol"
            FROM kullanici k
            LEFT JOIN rol r ON k.rol_id = r.rol_id
        """,
        "gosterge_sorgusu": "SELECT kullanici_id, kullanici_adi AS gosterge FROM kullanici",
        "alanlar": [
            ("kullanici_adi", "text", "Kullanıcı Adı", None),
            ("sifre_hash", "password", "Şifre", None),
            ("tel_no", "text", "Telefon No", None),
            ("rol_id", "iliski", "Rol", {"tablo": "rol", "id_kolon": "rol_id", "format": "{rol_adi}", "zorunlu": True}),
            ("ogretmen_id", "iliski", "Öğretmen (varsa)", {"tablo": "ogretmen", "id_kolon": "ogretmen_id", "format": "{ad} {soyad}", "zorunlu": False}),
            ("veli_id", "iliski", "Veli (varsa)", {"tablo": "veli", "id_kolon": "veli_id", "format": "{ad} {soyad}", "zorunlu": False}),
            ("personel_id", "iliski", "Personel (varsa)", {"tablo": "personel", "id_kolon": "personel_id", "format": "{ad} {soyad}", "zorunlu": False}),
        ],
    },
    "rol": {
        "isim": "Roller",
        "ikon": "⚙️",
        "id_kolon": "rol_id",
        "goruntuleme_sorgusu": "SELECT rol_adi AS \"Rol Adı\" FROM rol",
        "gosterge_sorgusu": "SELECT rol_id, rol_adi AS gosterge FROM rol",
        "alanlar": [
            ("rol_adi", "text", "Rol Adı", None),
        ],
    },
}

# Bir kayıt silinince, ona doğrudan bağlı ("yaprak" niteliğindeki, başka
# hiçbir tabloya referans vermeyen) kayıtların da otomatik silinmesi için
# harita. Sadece öğrenci ve personel için tanımlı — veli/öğretmen/sınıf gibi
# daha "üst" kayıtlar hâlâ korumalı (bağlı kaydı varsa silinemez), çünkü
# onları silmek daha büyük, zincirleme bir etkiye yol açabilir.
CASCADE_SILME_HARITASI = {
    "ogrenci": [
        ("yoklama", "ogrenci_id"),
        ("odemeler", "ogrenci_id"),
        ("saglik_listesi", "ogrenci_id"),
    ],
    "personel": [
        ("yemek_listesi", "personel_id"),
        ("temizlik_listesi", "personel_id"),
        ("odemeler", "personel_id"),
        ("saglik_listesi", "personel_id"),
    ],
}


def _alan_gir(kolon, tip, etiket, key_on_ek, mevcut_deger=None, iliski=None):
    """mevcut_deger verilmezse (None) boş bir 'Yeni Kayıt Ekle' alanı,
    verilirse o değerle önceden doldurulmuş bir 'Güncelle' alanı oluşturur.
    tip == "iliski" ise, ham ID yazmak yerine kullanıcıya isimden bir
    seçim (selectbox) sunar — opsiyonel ilişkilerde "— Yok —" seçeneği
    de vardır, seçilirse veritabanına gerçek NULL gönderilir (0 değil)."""
    key = f"{key_on_ek}_{kolon}"

    if tip == "iliski":
        tablo = iliski["tablo"]
        id_kolon = iliski["id_kolon"]
        format_str = iliski["format"]
        zorunlu = iliski.get("zorunlu", True)

        kayitlar = listele(f"SELECT * FROM {tablo}")
        secenekler = {}
        if not zorunlu:
            secenekler["— Yok —"] = None
        for _, satir in kayitlar.iterrows():
            try:
                etiket_metin = format_str.format(**satir.to_dict())
            except Exception:
                etiket_metin = str(satir[id_kolon])
            secenekler[etiket_metin] = int(satir[id_kolon])

        secenek_listesi = list(secenekler.keys())
        if not secenek_listesi:
            st.warning(f"{etiket} için seçilebilecek kayıt bulunamadı.")
            return None

        varsayilan_index = 0
        if mevcut_deger is not None:
            for i, (_, v) in enumerate(secenekler.items()):
                if v == mevcut_deger:
                    varsayilan_index = i
                    break

        secilen = st.selectbox(etiket, secenek_listesi, index=varsayilan_index, key=key)
        return secenekler[secilen]

    if tip == "text":
        return st.text_input(etiket, value=mevcut_deger if mevcut_deger is not None else "", key=key)
    if tip == "textarea":
        return st.text_area(etiket, value=mevcut_deger if mevcut_deger is not None else "", key=key)
    if tip == "date":
        # Takvim yerine, sadece sayı kabul eden 3 ayrı kutu: Gün / Ay / Yıl —
        # takvimde yıl/ay başlığından hızlı geçiş güvenilir çalışmadığı,
        # serbest metin kutusu ise harf girişine izin verdiği için tercih edildi.
        bugun = datetime.date.today()
        varsayilan_gun, varsayilan_ay, varsayilan_yil = bugun.day, bugun.month, bugun.year
        if mevcut_deger is not None:
            try:
                varsayilan_gun = mevcut_deger.day
                varsayilan_ay = mevcut_deger.month
                varsayilan_yil = mevcut_deger.year
            except Exception:
                pass
        st.markdown(f"**{etiket}**")
        c_gun, c_ay, c_yil = st.columns(3)
        with c_gun:
            gun = st.number_input("Gün", min_value=1, max_value=31, value=varsayilan_gun, step=1, key=f"{key}_gun")
        with c_ay:
            ay = st.number_input("Ay", min_value=1, max_value=12, value=varsayilan_ay, step=1, key=f"{key}_ay")
        with c_yil:
            yil = st.number_input("Yıl", min_value=1900, max_value=2100, value=varsayilan_yil, step=1, key=f"{key}_yil")
        try:
            return datetime.date(int(yil), int(ay), int(gun))
        except ValueError:
            st.error(f"{etiket}: Geçersiz tarih (bu ay bu kadar gün içermiyor).")
            return None
    if tip == "time":
        if mevcut_deger is not None:
            return st.time_input(etiket, value=mevcut_deger, key=key)
        return st.time_input(etiket, key=key)
    if tip == "number":
        return st.number_input(
            etiket, value=int(mevcut_deger) if mevcut_deger is not None else 0,
            min_value=0, step=1, key=key,
        )
    if tip == "decimal":
        return st.number_input(
            etiket, value=float(mevcut_deger) if mevcut_deger is not None else 0.0,
            min_value=0.0, step=0.01, key=key,
        )
    if tip == "password":
        return st.text_input(etiket, value="", type="password", key=key)
    return st.text_input(etiket, value=mevcut_deger if mevcut_deger is not None else "", key=key)


def _ekle_kaydet(tablo_adi, tanim, id_kolon, degerler):
    kolon_isimleri = ", ".join(k for k, _, _, _ in tanim["alanlar"])
    yer_tutucular = ", ".join("?" for _ in tanim["alanlar"])
    sorgu = f"INSERT INTO {tablo_adi} ({kolon_isimleri}) OUTPUT INSERTED.{id_kolon} VALUES ({yer_tutucular})"
    parametreler = [degerler[k] for k, _, _, _ in tanim["alanlar"]]
    yeni_id = calistir(sorgu, parametreler)
    # Yeni bir öğrenci eklendiğinde, otomatik olarak "Bekliyor" durumunda
    # bir ödeme kaydı oluştur — sekreter artık elle ödeme kaydı girmiyor.
    if tablo_adi == "ogrenci" and yeni_id:
        calistir(
            """INSERT INTO odemeler
               (odeme_tutari, tarih, odeme_sekli, odeme_durumu,
                toplam_tutar, kalan_tutar, taksit_sayisi,
                kalan_taksit_sayisi, ogrenci_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [0, degerler.get("kayit_tarihi"), "Belirtilmedi", "Bekliyor", 0, 0, 0, 0, yeni_id],
        )


@st.dialog("➕ Yeni Kayıt Ekle")
def _yeni_kayit_dialog(tablo_adi):
    """Modal pencere olarak açılır — arka plandaki kart listesi hiç
    kaymaz/kaydırılmaz, sadece bu pencere ekranın ortasında görünür."""
    tanim = TABLO_TANIMLARI[tablo_adi]
    id_kolon = tanim["id_kolon"]
    st.markdown(f"**{tanim['isim']}**")
    with st.form(f"form_ekle_{tablo_adi}"):
        degerler = {}
        for kolon, tip, etiket, iliski in tanim["alanlar"]:
            degerler[kolon] = _alan_gir(kolon, tip, etiket, f"ekle_{tablo_adi}", None, iliski)
        gonder = st.form_submit_button("Ekle")
        if gonder:
            try:
                _ekle_kaydet(tablo_adi, tanim, id_kolon, degerler)
                st.success("Kayıt eklendi.")
                st.rerun()
            except Exception as e:
                st.error(f"Kayıt eklenemedi: {e}")


@st.dialog("🗑️ Kayıt Sil")
def _kayit_sil_dialog(tablo_adi):
    """Modal pencere olarak açılır — arka plandaki kart listesi hiç
    kaymaz/kaydırılmaz, sadece bu pencere ekranın ortasında görünür."""
    tanim = TABLO_TANIMLARI[tablo_adi]
    id_kolon = tanim["id_kolon"]
    st.markdown(f"**{tanim['isim']}**")
    gosterge_veri = listele(tanim["gosterge_sorgusu"])
    if gosterge_veri.empty:
        st.info("Silinecek kayıt yok.")
    else:
        secenekler = {
            str(row["gosterge"]): int(row[id_kolon]) for _, row in gosterge_veri.iterrows()
        }
        with st.form(f"form_sil_{tablo_adi}"):
            secilen_gosterge = st.selectbox(
                "Silinecek kaydı seçin", list(secenekler.keys()), key=f"sil_sec_{tablo_adi}"
            )
            sil_gonder = st.form_submit_button("Sil")
            if sil_gonder:
                secilen_id = secenekler[secilen_gosterge]
                try:
                    # Önce (varsa) doğrudan bağlı yaprak kayıtları temizle
                    for bagli_tablo, sutun in CASCADE_SILME_HARITASI.get(tablo_adi, []):
                        calistir(f"DELETE FROM {bagli_tablo} WHERE {sutun} = ?", [secilen_id])
                    calistir(f"DELETE FROM {tablo_adi} WHERE {id_kolon} = ?", [secilen_id])
                    st.success("Kayıt silindi.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Silinemedi — bu kayda bağlı başka kayıtlar olabilir. ({e})")


@st.dialog("✏️ Kaydı Güncelle")
def _kayit_guncelle_dialog(tablo_adi, kayit_id, ham):
    """Modal pencere olarak açılır — popover'ın aksine, formun Kaydet
    butonuna basılıp st.rerun() çağrıldığında kesinlikle kapanır."""
    tanim = TABLO_TANIMLARI[tablo_adi]
    id_kolon = tanim["id_kolon"]
    st.markdown(f"**{tanim['isim']}**")
    with st.form(f"form_guncelle_{tablo_adi}_{kayit_id}"):
        yeni_degerler = {}
        for kolon, tip, etiket, iliski in tanim["alanlar"]:
            mevcut_deger = ham[kolon] if kolon in ham.index else None
            yeni_degerler[kolon] = _alan_gir(
                kolon, tip, etiket, f"guncelle_{tablo_adi}_{kayit_id}",
                mevcut_deger, iliski,
            )
        kaydet = st.form_submit_button("Kaydet")
        if kaydet:
            # "password" tipindeki alanlar (şifre), güncelleme formunda
            # güvenlik amacıyla her zaman boş açılır — mevcut şifre ekranda
            # gösterilmez. Kullanıcı yeni bir şifre yazmadan Kaydet'e
            # basarsa, o boş değeri veritabanına yazıp eski şifreyi SİLMEK
            # yerine, o alanı güncellemeden (dokunmadan) atlıyoruz.
            guncellenecek_alanlar = [
                (k, t) for k, t, _, _ in tanim["alanlar"]
                if not (t == "password" and not str(yeni_degerler[k]).strip())
            ]
            set_ifadesi = ", ".join(f"{k}=?" for k, _ in guncellenecek_alanlar)
            parametreler = [yeni_degerler[k] for k, _ in guncellenecek_alanlar] + [kayit_id]
            try:
                calistir(
                    f"UPDATE {tablo_adi} SET {set_ifadesi} WHERE {id_kolon}=?",
                    parametreler,
                )
                st.success("Güncellendi.")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Güncellenemedi: {e}")


def genel_tablo_yonet(tablo_adi, arama_metni=""):
    tanim = TABLO_TANIMLARI[tablo_adi]
    id_kolon = tanim["id_kolon"]

    st.markdown(
        f'<div class="admin-icerik-baslik">{tanim.get("ikon", "")} {tanim["isim"]}</div>',
        unsafe_allow_html=True,
    )

    # ============ EKLE / SİL — modal pencere açan butonlar, sayfayı kaydırmaz ============
    kol_ekle, kol_sil = st.columns(2)
    with kol_ekle:
        if st.button("➕ Yeni Kayıt Ekle", use_container_width=True, key=f"btn_ac_ekle_{tablo_adi}"):
            _yeni_kayit_dialog(tablo_adi)
    with kol_sil:
        if st.button("🗑️ Kayıt Sil", use_container_width=True, key=f"btn_ac_sil_{tablo_adi}"):
            _kayit_sil_dialog(tablo_adi)

    st.markdown("")

    # ============ KAYITLAR (kartlar) ============
    # Kart içeriği için: isimli (join'li) görünüm
    goruntu_veri = listele(tanim["goruntuleme_sorgusu"])
    # Güncelleme formu ve ID eşleştirme için: ham veri (id dahil, tüm sütunlar)
    ham_veri = listele(f"SELECT * FROM {tablo_adi}")

    if arama_metni and arama_metni.strip() and not goruntu_veri.empty:
        arama_kucuk = arama_metni.strip().lower()
        maske = goruntu_veri.apply(
            lambda satir: satir.astype(str).str.lower().str.contains(arama_kucuk, regex=False).any(),
            axis=1,
        )
        goruntu_veri = goruntu_veri[maske.values]
        ham_veri = ham_veri[maske.values]

    if goruntu_veri.empty:
        st.info("Kayıt bulunamadı.")
    else:
        goruntu_satirlar = list(goruntu_veri.iterrows())
        ham_satirlar = list(ham_veri.iterrows())
        for i in range(0, len(goruntu_satirlar), 4):
            parca_g = goruntu_satirlar[i:i + 4]
            parca_h = ham_satirlar[i:i + 4]
            kolonlar = st.columns(4)
            for kolon, (_, gosterim), (_, ham) in zip(kolonlar, parca_g, parca_h):
                kayit_id = int(ham[id_kolon])
                with kolon:
                    with st.container(border=True, key=f"kart_{tablo_adi}_{kayit_id}"):
                        for sutun_adi, deger in gosterim.items():
                            deger_str = "—" if deger is None or str(deger).lower() == "nan" else deger
                            st.markdown(f"**{sutun_adi}:** {deger_str}")

                        if st.button("✏️ Güncelle", key=f"btn_guncelle_{tablo_adi}_{kayit_id}", use_container_width=True):
                            _kayit_guncelle_dialog(tablo_adi, kayit_id, ham)

    # Scroll: bir işlem sonrası ilgili bölüme kaydır (deneysel — Streamlit'in
    # resmi olarak desteklemediği bir JavaScript tekniği, garantili değildir)
    if st.session_state.get("admin_scroll_hedef"):
        hedef = st.session_state["admin_scroll_hedef"]
        st.session_state["admin_scroll_hedef"] = None
        st.markdown(f"""
        <script>
            setTimeout(function() {{
                var el = window.parent.document.querySelector('.st-key-{hedef}');
                if (el) {{ el.scrollIntoView({{behavior: 'smooth', block: 'center'}}); }}
            }}, 300);
        </script>
        """, unsafe_allow_html=True)


def admin_paneli_goster():
    admin_stilleri_yukle()

    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="brand-logo-icon">🌈</div>
                <div class="brand-title-text">
                    <span class="part-1">Minik</span>
                    <span class="part-2">Adımlar</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for anahtar, tanim in TABLO_TANIMLARI.items():
            aktif = st.session_state.get("admin_secili_tablo", "ogrenci") == anahtar
            container_key = "menu_aktif" if aktif else f"menu_{anahtar}"
            with st.container(key=container_key):
                etiket = f"{tanim.get('ikon', '•')}  {tanim['isim']}"
                if st.button(etiket, key=f"menu_btn_{anahtar}"):
                    st.session_state.admin_secili_tablo = anahtar
                    st.rerun()

    # ============ HEADER ============
    with st.container(key="admin_header_cubugu"):
        ust_sol, ust_bosluk, ust_zil, ust_menu = st.columns([2.8, 4.4, 0.6, 2.6])

        with ust_sol:
            arama = st.text_input(
                "Arama yap...",
                placeholder="Ara...",
                key="header_arama",
                label_visibility="collapsed",
            )

        with ust_zil:
            with st.container(key="header_bildirim"):
                st.button("🔔", key="btn_bildirim", help="Bildirimler")

        with ust_menu:
            kol_sifre, kol_cikis = st.columns([1, 2])
            with kol_sifre:
                with st.container(key="admin_sifre"):
                    if st.button("🔑", key="btn_admin_sifre", help="Şifre Değiştir"):
                        st.session_state.sayfa = "sifre_degistir"
                        st.rerun()
            with kol_cikis:
                with st.container(key="admin_cikis"):
                    if st.button("🚪 Çıkış Yap", key="btn_admin_cikis"):
                        st.session_state.giris_yapildi = False
                        st.session_state.rol_adi = None
                        st.session_state.kullanici_adi = None
                        st.session_state.sayfa = "anasayfa"
                        st.rerun()

    # ============ İÇERİK ALANI ============
    with st.container(key="admin_icerik_alani"):
        genel_tablo_yonet(st.session_state.get("admin_secili_tablo", "ogrenci"), arama)