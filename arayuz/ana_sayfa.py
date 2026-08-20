import streamlit as st
import pyodbc
import pandas as pd

st.title("Anaokulu Otomasyonu")

# Veritabanı bağlantısı
baglanti = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=Anaokulu_Otomasyonu;'
    'Trusted_Connection=yes;'
)

st.header("Öğrenciler")

# Öğrencileri çek ve tablo olarak göster
sorgu = "SELECT * FROM ogrenci"
veri = pd.read_sql(sorgu, baglanti)
st.dataframe(veri)

baglanti.close()