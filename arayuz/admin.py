"""
Admin Paneli — Modern ve Optimize Edilmiş Tasarım
Renkler Ana Sayfa'nın paletiyle uyumlu: turuncu (#D97B3D/#FFB86B), krem (#FAFAF7)

Her tablo İKİ sorgu kullanır:
  - "goruntuleme_sorgusu": ekranda gösterilen, ID YOK, JOIN'lerle isimlendirilmiş sorgu
  - "gosterge_sorgusu": silme işleminde, kaydı TANIYAN bir metne göre (örn. "Ecrin Yılmaz")
    seçim yapmak için — kullanıcı hiçbir zaman ID görmüyor/girmiyor.

Öğrenciler tablosu ayrıca özel bir kart görünümüne sahip (ogrenciler_yonet),
her kartta ✏️ Güncelle butonu ile satır bazlı düzenleme yapılabiliyor.
"""

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
            ("ad", "text", "Ad"),
            ("soyad", "text", "Soyad"),
            ("dogum_tarihi", "date", "Doğum Tarihi"),
            ("kayit_tarihi", "date", "Kayıt Tarihi"),
            ("veli_id", "number", "Veli ID"),
            ("sinif_id", "number", "Sınıf ID"),
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
            ("ad", "text", "Ad"),
            ("soyad", "text", "Soyad"),
            ("tel_no", "text", "Telefon No"),
            ("adres", "text", "Adres"),
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
            ("ad", "text", "Ad"),
            ("soyad", "text", "Soyad"),
            ("tel_no", "text", "Telefon No"),
            ("adres", "text", "Adres"),
            ("ise_giris_tarihi", "date", "İşe Giriş Tarihi"),
            ("tecrube", "number", "Tecrübe (yıl)"),
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
            ("sinif_adi", "text", "Sınıf Adı"),
            ("yas_grubu", "text", "Yaş Grubu"),
            ("kapasite", "number", "Kapasite"),
            ("ogretmen_id", "number", "Öğretmen ID"),
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
            ("odeme_tutari", "decimal", "Ödeme Tutarı"),
            ("tarih", "date", "Tarih"),
            ("odeme_sekli", "text", "Ödeme Şekli"),
            ("odeme_durumu", "text", "Ödeme Durumu"),
            ("toplam_tutar", "decimal", "Toplam Tutar"),
            ("kalan_tutar", "decimal", "Kalan Tutar"),
            ("taksit_sayisi", "number", "Taksit Sayısı"),
            ("kalan_taksit_sayisi", "number", "Kalan Taksit Sayısı"),
            ("ogrenci_id", "number", "Öğrenci ID"),
            ("personel_id", "number", "Personel ID"),
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
            ("ders_adi", "text", "Ders Adı"),
            ("baslangic_saati", "time", "Başlangıç Saati"),
            ("bitis_saati", "time", "Bitiş Saati"),
            ("ogretmen_id", "number", "Öğretmen ID"),
            ("sinif_id", "number", "Sınıf ID"),
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
            ("tarih", "date", "Tarih"),
            ("saat", "time", "Saat"),
            ("baslik", "text", "Başlık"),
            ("aciklama", "textarea", "Açıklama"),
            ("ogretmen_id", "number", "Öğretmen ID (varsa)"),
            ("sinif_id", "number", "Sınıf ID (varsa)"),
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
            ("ogrenci_id", "number", "Öğrenci ID"),
            ("tarih", "date", "Tarih"),
            ("durum", "text", "Durum (var/yok/izinli)"),
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
            ("ad", "text", "Ad"),
            ("soyad", "text", "Soyad"),
            ("tel_no", "text", "Telefon No"),
            ("adres", "text", "Adres"),
            ("tecrube", "number", "Tecrübe (yıl)"),
            ("ise_giris_tarihi", "date", "İşe Giriş Tarihi"),
            ("pozisyon", "text", "Pozisyon"),
            ("gorev", "text", "Görev"),
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
            ("alerji", "text", "Alerji"),
            ("kronik_hastalik", "text", "Kronik Hastalık"),
            ("acil_durum_notu", "textarea", "Acil Durum Notu"),
            ("acil_durum_tel", "text", "Acil Durum Telefonu"),
            ("ogrenci_id", "number", "Öğrenci ID"),
            ("personel_id", "number", "Personel ID"),
        ],
    },
    "yemek_listesi": {
        "isim": "Yemek Listesi",
        "ikon": "🍴",
        "id_kolon": "yemek_listesi_id",
        "goruntuleme_sorgusu": """
            SELECT yl.yemek_adi AS "Yemek Adı", yl.tarih AS "Tarih",
                   p.ad AS "Sorumlu Adı", p.soyad AS "Sorumlu Soyadı"
            FROM yemek_listesi yl
            LEFT JOIN personel p ON yl.personel_id = p.personel_id
        """,
        "gosterge_sorgusu": "SELECT yemek_listesi_id, yemek_adi + ' - ' + CONVERT(varchar, tarih) AS gosterge FROM yemek_listesi",
        "alanlar": [
            ("yemek_adi", "text", "Yemek Adı"),
            ("tarih", "date", "Tarih"),
            ("personel_id", "number", "Personel ID"),
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
            ("alan", "text", "Alan"),
            ("tarih", "date", "Tarih"),
            ("durum", "text", "Durum"),
            ("personel_id", "number", "Personel ID"),
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
            ("kullanici_adi", "text", "Kullanıcı Adı"),
            ("sifre_hash", "password", "Şifre"),
            ("tel_no", "text", "Telefon No"),
            ("rol_id", "number", "Rol ID"),
            ("ogretmen_id", "number", "Öğretmen ID (varsa)"),
            ("veli_id", "number", "Veli ID (varsa)"),
            ("personel_id", "number", "Personel ID (varsa)"),
        ],
    },
    "rol": {
        "isim": "Roller",
        "ikon": "⚙️",
        "id_kolon": "rol_id",
        "goruntuleme_sorgusu": "SELECT rol_adi AS \"Rol Adı\" FROM rol",
        "gosterge_sorgusu": "SELECT rol_id, rol_adi AS gosterge FROM rol",
        "alanlar": [
            ("rol_adi", "text", "Rol Adı"),
        ],
    },
}


def _alan_gir(kolon, tip, etiket, key_on_ek, mevcut_deger=None):
    """mevcut_deger verilmezse (None) boş bir 'Yeni Kayıt Ekle' alanı,
    verilirse o değerle önceden doldurulmuş bir 'Güncelle' alanı oluşturur."""
    key = f"{key_on_ek}_{kolon}"
    if tip == "text":
        return st.text_input(etiket, value=mevcut_deger if mevcut_deger is not None else "", key=key)
    if tip == "textarea":
        return st.text_area(etiket, value=mevcut_deger if mevcut_deger is not None else "", key=key)
    if tip == "date":
        if mevcut_deger is not None:
            return st.date_input(etiket, value=mevcut_deger, key=key)
        return st.date_input(etiket, key=key)
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


def genel_tablo_yonet(tablo_adi, arama_metni=""):
    tanim = TABLO_TANIMLARI[tablo_adi]
    id_kolon = tanim["id_kolon"]

    st.markdown(
        f'<div class="admin-icerik-baslik">{tanim.get("ikon", "")} {tanim["isim"]}</div>',
        unsafe_allow_html=True,
    )

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

                        duzenle_key = f"{tablo_adi}_duzenle_{kayit_id}"
                        if st.button("✏️ Güncelle", key=f"btn_duzenle_{tablo_adi}_{kayit_id}", use_container_width=True):
                            st.session_state[duzenle_key] = not st.session_state.get(duzenle_key, False)
                            st.session_state["admin_scroll_hedef"] = f"kart_{tablo_adi}_{kayit_id}"
                            st.rerun()

                        if st.session_state.get(duzenle_key, False):
                            with st.form(f"form_guncelle_{tablo_adi}_{kayit_id}"):
                                yeni_degerler = {}
                                for kolon, tip, etiket in tanim["alanlar"]:
                                    mevcut_deger = ham[kolon] if kolon in ham.index else None
                                    yeni_degerler[kolon] = _alan_gir(
                                        kolon, tip, etiket, f"guncelle_{tablo_adi}_{kayit_id}", mevcut_deger
                                    )
                                kaydet = st.form_submit_button("Kaydet")
                                if kaydet:
                                    set_ifadesi = ", ".join(f"{k}=?" for k, _, _ in tanim["alanlar"])
                                    parametreler = [yeni_degerler[k] for k, _, _ in tanim["alanlar"]] + [kayit_id]
                                    try:
                                        calistir(
                                            f"UPDATE {tablo_adi} SET {set_ifadesi} WHERE {id_kolon}=?",
                                            parametreler,
                                        )
                                        st.session_state[duzenle_key] = False
                                        st.session_state["admin_scroll_hedef"] = f"kart_{tablo_adi}_{kayit_id}"
                                        st.success("Güncellendi.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Güncellenemedi: {e}")

    st.markdown("")
    kol_ekle, kol_sil = st.columns(2)

    with kol_ekle:
        with st.container(key=f"ekle_bolumu_{tablo_adi}"):
            with st.expander("➕ Yeni Kayıt Ekle"):
                with st.form(f"form_ekle_{tablo_adi}"):
                    degerler = {}
                    for kolon, tip, etiket in tanim["alanlar"]:
                        degerler[kolon] = _alan_gir(kolon, tip, etiket, f"ekle_{tablo_adi}")
                    gonder = st.form_submit_button("Ekle")
                    if gonder:
                        kolon_isimleri = ", ".join(k for k, _, _ in tanim["alanlar"])
                        yer_tutucular = ", ".join("?" for _ in tanim["alanlar"])
                        sorgu = f"INSERT INTO {tablo_adi} ({kolon_isimleri}) VALUES ({yer_tutucular})"
                        parametreler = [degerler[k] for k, _, _ in tanim["alanlar"]]
                        try:
                            calistir(sorgu, parametreler)
                            st.session_state["admin_scroll_hedef"] = f"ekle_bolumu_{tablo_adi}"
                            st.success("Kayıt eklendi.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Kayıt eklenemedi: {e}")

    with kol_sil:
        with st.container(key=f"sil_bolumu_{tablo_adi}"):
            with st.expander("🗑️ Kayıt Sil"):
                gosterge_veri = listele(tanim["gosterge_sorgusu"])
                if gosterge_veri.empty:
                    st.info("Silinecek kayıt yok.")
                else:
                    secenekler = {
                        str(row["gosterge"]): int(row[id_kolon])
                        for _, row in gosterge_veri.iterrows()
                    }
                    with st.form(f"form_sil_{tablo_adi}"):
                        secilen_gosterge = st.selectbox(
                            "Silinecek kaydı seçin", list(secenekler.keys()), key=f"sil_sec_{tablo_adi}"
                        )
                        sil_gonder = st.form_submit_button("Sil")
                        if sil_gonder:
                            secilen_id = secenekler[secilen_gosterge]
                            try:
                                calistir(f"DELETE FROM {tablo_adi} WHERE {id_kolon} = ?", [secilen_id])
                                st.session_state["admin_scroll_hedef"] = f"sil_bolumu_{tablo_adi}"
                                st.success("Kayıt silindi.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Silinemedi — bu kayda bağlı başka kayıtlar olabilir. ({e})")

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