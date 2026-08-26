"""
Veritabanı bağlantısı ve yardımcı fonksiyonlar.
Tüm sayfalar bu dosyayı import edip kullanır.
"""

import pyodbc
import pandas as pd


def baglan():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=Anaokulu_Otomasyonu;'
        'Trusted_Connection=yes;'
    )


def listele(sorgu, parametreler=None):
    conn = baglan()
    if parametreler:
        veri = pd.read_sql(sorgu, conn, params=parametreler)
    else:
        veri = pd.read_sql(sorgu, conn)
    conn.close()
    return veri


def calistir(sorgu, parametreler):
    """INSERT/UPDATE/DELETE çalıştırır. Sorgu bir sonuç kümesi döndürüyorsa
    (örn. INSERT ... OUTPUT INSERTED.id_kolonu ile yazıldıysa) o değeri
    döndürür — normal UPDATE/DELETE'te (sonuç kümesi olmadığında) None
    döner. Mevcut çağrıların hiçbiri bu dönüş değerini kullanmak zorunda
    değil, geriye dönük uyumluluk bozulmaz."""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute(sorgu, parametreler)
    sonuc = None
    if cursor.description:
        satir = cursor.fetchone()
        if satir:
            sonuc = satir[0]
    conn.commit()
    conn.close()
    return sonuc