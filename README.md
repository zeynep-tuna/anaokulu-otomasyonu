# 🌈 Minik Adımlar Anaokulu — Otomasyon Sistemi

Bir anaokulunun günlük operasyonlarını (öğrenci takibi, yoklama, ödemeler,
personel yönetimi, ders programı vb.) dijitalleştiren, dört farklı kullanıcı
rolüne özel arayüzler sunan tam kapsamlı bir web uygulaması. 9 günlük bir
staj programı kapsamında sıfırdan geliştirilmiştir.

## 🛠️ Kullanılan Teknolojiler

- **Python** — uygulama dili
- **Streamlit** — web arayüzü
- **Microsoft SQL Server** — veritabanı
- **pyodbc** — veritabanı bağlantısı
- **pandas** — veri işleme

## 👥 Roller ve Özellikler

Sistem, giriş yapan kullanıcının rolüne göre tamamen farklı bir deneyim sunar.

### 🔑 Admin
- Veritabanındaki 14 tablonun tamamını (Öğrenciler, Veliler, Öğretmenler,
  Sınıflar, Ödemeler, Ders Programı, Etkinlikler, Yoklama, Personel, Sağlık
  Takibi, Yemek Listesi, Temizlik Takibi, Kullanıcılar, Roller) tek bir
  panelden yönetir
- Her tabloda kart görünümünde listeleme; ilişkisel alanlar (veli, sınıf,
  öğretmen vb.) ham ID yerine isimden seçilerek doldurulur
- Modal pencereler üzerinden Ekle / Sil / Güncelle işlemleri
- Bir öğrenci veya personel silindiğinde, ona bağlı tüm kayıtlar (yoklama,
  ödeme, sağlık, yemek, temizlik) otomatik olarak temizlenir
- Yeni bir öğrenci eklendiğinde otomatik olarak "Bekliyor" durumunda bir
  ödeme kaydı oluşturulur

### 👩‍🏫 Öğretmen
- Sınıfım, Öğrencilerim, Yoklama (günlük kayıt), Ders Programı, Etkinlikler,
  Bilgilerim

### 👨‍👩‍👧 Veli
- Çocuklarım, Yoklama (görüntüleme), Ödemeler, Etkinlikler, Bilgilerim

### 🧹 Personel
- Görünen bölümler, personelin pozisyonuna göre otomatik belirlenir:
  - **Temizlikçi** → Temizlik Listesi (durum güncelleme, Tümü/Yapılacaklar/
    Tamamlananlar filtresi, tarih sıralama)
  - **Aşçı** → Yemek Listesi (aynı güne ait yemekler tek kartta gruplanır)
  - **Sekreter / İdari** → Sağlık Takibi, Ödemeler (bekleyen ödemeleri
    "Ödendi" olarak işaretleyebilir)

### 🌐 Herkese Açık Sayfalar
Giriş yapmadan da erişilebilen Ana Sayfa, Hakkımızda, Sınıflar ve İletişim
sayfaları mevcuttur. Sınıflar sayfası veritabanından canlı veri çeker.

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.x
- Microsoft SQL Server (ODBC Driver 17 ile)
- Gerekli Python paketleri: `streamlit`, `pyodbc`, `pandas`

### Adımlar

1. Projeyi klonlayın:
   ```
   git clone <repo-linki>
   cd anaokulu_otomasyonu
   ```

2. Gerekli paketleri kurun:
   ```
   pip install streamlit pyodbc pandas
   ```

3. `arayuz/veritabani.py` içindeki bağlantı bilgilerini kendi SQL Server
   ayarlarınıza göre düzenleyin (sunucu adı, veritabanı adı).

4. `Anaokulu_Otomasyonu` veritabanını ve 14 tabloyu SQL Server üzerinde
   oluşturun.

5. Uygulamayı başlatın:
   ```
   streamlit run arayuz/ana_sayfa.py
   ```

6. Tarayıcınızda otomatik olarak açılacaktır (varsayılan adres:
   `http://localhost:8501`).

## 📁 Proje Yapısı

```
arayuz/
├── ana_sayfa.py         # Giriş noktası, sayfa yönlendirme
├── header.py             # Ortak üst menü (role göre dinamik)
├── footer.py              # Ortak alt bilgi
├── stiller.py              # Genel CSS
├── giris.py                 # Giriş sayfası
├── sifre_degistir.py         # Şifre değiştirme
├── hakkimizda.py               # Hakkımızda sayfası
├── siniflar.py                  # Sınıflar sayfası (herkese açık)
├── iletisim.py                    # İletişim sayfası
├── admin.py                        # Admin paneli
├── ogretmen.py                      # Öğretmen paneli
├── veli.py                           # Veli paneli
├── personel.py                        # Personel paneli
└── veritabani.py                       # Veritabanı bağlantı fonksiyonları
```

## 🗄️ Veritabanı

Proje, MS SQL Server üzerinde 14 ilişkisel tablodan oluşan bir şema
kullanır: `ogrenci`, `veli`, `ogretmen`, `sinif`, `odemeler`, `ders`,
`etkinlik`, `yoklama`, `personel`, `saglik_listesi`, `yemek_listesi`,
`temizlik_listesi`, `kullanici`, `rol`.
