use Anaokulu_Otomasyonu
go

create table ogrenci(
	ogrenci_id int identity(1,1) primary key,
	ad nvarchar(50) not null ,
	soyad nvarchar(50) not null ,
	dogum_tarihi date not null ,
	kayit_tarihi date not null ,
	veli_id int not null ,
	sinif_id int 

);

create table veli(
	veli_id int identity(1,1) primary key ,
	ad nvarchar(50) not null ,
	soyad nvarchar(50) not null ,
	tel_no nvarchar(15) not null ,
	adres nvarchar(200) not null

);

create table ogretmen(
	ogretmen_id int identity(1,1) primary key ,
	ad nvarchar(50) not null , 
	soyad nvarchar(50) not null ,
	tel_no nvarchar(50) not null ,
	adres nvarchar(200) ,
	ise_giris_tarihi date ,
	tecrube int

);

create table sinif(
	sinif_id int identity(1,1) primary key ,
	sinif_adi nvarchar(10) not null ,
	yas_grubu nvarchar(10) not null ,
	kapasite int not null ,
	ogretmen_id int 

);

create table personel(
	personel_id int identity(1,1) primary key ,
	ad nvarchar(50) not null ,
	soyad nvarchar(50) not null ,
	tel_no nvarchar(15) not null ,
	adres nvarchar(200) not null ,
	tecrube int ,
	ise_giris_tarihi date ,
	pozisyon nvarchar(50) not null ,
	gorev nvarchar(50)

);

create table kullanici(
	kullanici_id int identity(1,1) primary key ,
	kullanici_adi nvarchar(50) not null ,
	sifre_hash nvarchar(50) not null ,
	tel_no nvarchar(15) not null ,
	rol_id int ,
	ogretmen_id int ,
	veli_id int ,
	personel_id int 

);

create table rol(
	rol_id int identity(1,1) primary key ,
	rol_adi nvarchar(50) not null 

);

create table yoklama(
	yoklama_id int identity(1,1) primary key ,
	ogrenci_id int not null ,
	tarih date not null ,
	durum nvarchar(6) not null

);

create table odemeler(
	odemeler_id int identity(1,1) primary key ,
	odeme_tutari decimal(8,2) not null ,
	tarih date not null ,
	odeme_sekli nvarchar(15) ,
	odeme_durumu nvarchar(10) ,
	toplam_tutar decimal(8,2) not null ,
	kalan_tutar decimal(8,2) not null ,
	taksit_sayisi int not null ,
	kalan_taksit_sayisi int not null ,
	ogrenci_id int ,
	personel_id int

);

create table ders(
	ders_id int identity(1,1) primary key ,
	ders_adi nvarchar(50) ,
	baslangic_saati time not null ,
	bitis_saati time not null ,
	ogretmen_id int ,
	sinif_id int 

);

create table yemek_listesi(
	yemek_listesi_id int identity(1,1) primary key ,
	yemek_adi nvarchar(50) not null ,
	tarih date not null ,
	personel_id int 

);

create table temizlik_listesi(
	temizlik_listesi_id int identity(1,1) primary key ,
	alan nvarchar(50) not null ,
	tarih date not null ,
	durum nvarchar(50) not null ,
	personel_id int 

);

create table etkinlik(
	etkinlik_id int identity(1,1) primary key ,
	tarih date ,
	saat time ,
	baslik nvarchar(200) ,
	aciklama nvarchar(500) ,
	ogretmen_id int ,
	sinif_id int 

);

create table saglik_listesi(
	saglik_listesi_id int identity(1,1) primary key ,
	alerji nvarchar(200) ,
	kronik_hastalik nvarchar(200) ,
	acil_durum_notu nvarchar(500) ,
	acil_durum_tel nvarchar(15) ,
	ogrenci_id int,
	personel_id int

);

alter table ogrenci add constraint fk_ogrenci_veli
	foreign key (veli_id) references veli(veli_id);

alter table ogrenci add constraint fk_ogrenci_sinif
	foreign key (sinif_id) references sinif(sinif_id);

alter table sinif add constraint fk_sinif_ogretmen
	foreign key (ogretmen_id) references ogretmen(ogretmen_id);

alter table kullanici add constraint fk_kullanici_personel
	foreign key (personel_id) references personel(personel_id);

alter table kullanici add constraint fk_kullanici_ogretmen
	foreign key (ogretmen_id) references ogretmen(ogretmen_id);

alter table kullanici add constraint fk_kullanici_veli
	foreign key (veli_id) references veli(veli_id);

alter table kullanici add constraint fk_kullanici_rol
	foreign key (rol_id) references rol(rol_id);

alter table yoklama add constraint fk_yoklama_ogrenci
	foreign key (ogrenci_id) references ogrenci(ogrenci_id);

alter table odemeler add constraint fk_odemeler_ogrenci
	foreign key (ogrenci_id) references ogrenci(ogrenci_id);

alter table odemeler add constraint fk_odemeler_personel
	foreign key (personel_id) references personel(personel_id);

alter table ders add constraint fk_ders_ogretmen
	foreign key (ogretmen_id) references ogretmen(ogretmen_id);

alter table ders add constraint fk_ders_sinif
	foreign key (sinif_id) references sinif(sinif_id);

alter table yemek_listesi add constraint fk_yemek_personel
	foreign key (personel_id) references personel(personel_id);

alter table temizlik_listesi add constraint fk_temizlik_personel
	foreign key (personel_id) references personel(personel_id);

alter table etkinlik add constraint fk_etkinlik_ogretmen
	foreign key (ogretmen_id) references ogretmen(ogretmen_id);

alter table etkinlik add constraint fk_etkinlik_sinif
	foreign key (sinif_id) references sinif(sinif_id);

alter table saglik_listesi add constraint fk_saglik_ogrenci
	foreign key (ogrenci_id) references ogrenci(ogrenci_id);

alter table saglik_listesi add constraint fk_saglik_personel
	foreign key (personel_id) references personel(personel_id);



	----------------------- VERİ EKLEME ----------------
use Anaokulu_Otomasyonu;
go

insert into ogretmen (ad, soyad, tel_no, adres, ise_giris_tarihi, tecrube) values
('Zeynep', 'Aydin', '05334445566', 'Gebze, Kocaeli', '2022-09-01', 4),
('Elif', 'Sahin', '05335556677', 'Gebze, Kocaeli', '2023-02-15', 2);

insert into veli (ad, soyad, tel_no, adres) values
('Ahmet', 'Yilmaz', '05551112233', 'Gebze, Kocaeli'),
('Ayse', 'Demir', '05552223344', 'Gebze, Kocaeli'),
('Mehmet', 'Kaya', '05553334455', 'Gebze, Kocaeli');

insert into personel (ad, soyad, tel_no, adres, tecrube, ise_giris_tarihi, pozisyon, gorev) values
('Fatma', 'Celik', '05336667788', 'Gebze, Kocaeli', 5, '2021-05-10', 'Sekreter', 'İdari İşler'),
('Ali', 'Ozturk', '05337778899', 'Gebze, Kocaeli', 3, '2022-11-20', 'Temizlikçi', 'Temizlik');

insert into rol (rol_adi) values
('admin'), ('ogretmen'), ('veli'), ('personel');

insert into sinif (sinif_adi, yas_grubu, kapasite, ogretmen_id) values
('Kelebekler', '3-4 Yas', 15, 1),
('Papatyalar', '4-5 Yas', 18, 2);

insert into kullanici (kullanici_adi, sifre_hash, tel_no, rol_id, ogretmen_id, veli_id, personel_id) values
('admin1', 'HASHLENMIS_SIFRE_1', '05551234567', 1, NULL, NULL, NULL),
('zeynep.aydin', 'HASHLENMIS_SIFRE_2', '05334445566', 2, 1, NULL, NULL),
('ahmet.yilmaz', 'HASHLENMIS_SIFRE_3', '05551112233', 3, NULL, 1, NULL);

insert into ogrenci (ad, soyad, dogum_tarihi, kayit_tarihi, veli_id, sinif_id) values
('Ecrin', 'Yilmaz', '2021-03-15', '2025-09-01', 1, 1),
('Kerem', 'Demir', '2020-07-22', '2025-09-01', 2, 2),
('Defne', 'Kaya', '2021-01-10', '2025-09-01', 3, 1);

insert into yoklama (ogrenci_id, tarih, durum) values
(1, '2026-08-19', 'var'),
(2, '2026-08-19', 'yok'),
(3, '2026-08-19', 'var');

insert into odemeler (odeme_tutari, tarih, odeme_sekli, odeme_durumu, toplam_tutar, kalan_tutar, taksit_sayisi, kalan_taksit_sayisi, ogrenci_id, personel_id) values
(1500.00, '2026-08-01', 'Nakit', 'Odendi', 9000.00, 7500.00, 6, 5, 1, 1),
(1500.00, '2026-08-01', 'Kredi Karti', 'Odendi', 9000.00, 7500.00, 6, 5, 2, 1);

insert into ders (ders_adi, baslangic_saati, bitis_saati, ogretmen_id, sinif_id) values
('Muzik', '10:00', '10:40', 1, 1),
('Resim', '11:00', '11:40', 2, 2);

insert into yemek_listesi (yemek_adi, tarih, personel_id) values
('Tavuklu Pilav', '2026-08-19', 1),
('Mercimek Corbasi', '2026-08-20', 1);

insert into temizlik_listesi (alan, tarih, durum, personel_id) values
('Mutfak', '2026-08-19', 'Yapildi', 2),
('Kelebekler Sinifi', '2026-08-19', 'Yapildi', 2);

insert into etkinlik (tarih, saat, baslik, aciklama, ogretmen_id, sinif_id) values
('2026-09-15', '14:00', 'Veli Toplantisi', 'Donem baslangici veli toplantisi', 1, 1),
('2026-10-29', '10:00', '29 Ekim Gosterisi', 'Tum okul katilimiyla kutlama', NULL, NULL);

insert into saglik_listesi (alerji, kronik_hastalik, acil_durum_notu, acil_durum_tel, ogrenci_id, personel_id) values
('Findik alerjisi', NULL, 'Astim spreyi cantasinda', '05559998877', 1, 1),
(NULL, NULL, NULL, '05558887766', 2, 1);



--------- Tabloları Görme 

select * from ogretmen;
select * from veli;
select * from personel;
select * from rol;
select * from sinif;
select * from kullanici;
select * from ogrenci;
select * from yoklama;
select * from odemeler;
select * from ders;
select * from yemek_listesi;
select * from temizlik_listesi;
select * from etkinlik;
select * from saglik_listesi;
