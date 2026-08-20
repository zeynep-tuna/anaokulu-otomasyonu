import pyodbc

# 1. Kurulu SQL Server driver'larını listele
print("Kurulu SQL Server driver'ları:")
drivers = [driver for driver in pyodbc.drivers() if 'SQL Server' in driver]
print(drivers)

# 2. Bağlantıyı dene
try:
    baglanti = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=Anaokulu_Otomasyonu;'
        'Trusted_Connection=yes;'
    )
    print("\nBağlantı başarılı!")
    baglanti.close()
except Exception as e:
    print("\nBağlantı hatası:")
    print(e)