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
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute(sorgu, parametreler)
    conn.commit()
    conn.close()
