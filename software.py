import os
import tkinter
import sqlite3

index=999
sqlconnection=sqlite3.connect('softwarehomeworkdb.db')
sqlcursor=sqlconnection.cursor()
if sqlcursor:
    print("connection successfull")
else:
    print("connection failed")
def guncelle(zorluk,dTarih,dGorus,denetID,soruId):
    sqlcursor.execute("UPDATE soru SET zorluk=? , denetleme_tarihi=? , denetleyici_id=? , denetleyici_gorus=? WHERE Id=?" ,(zorluk,dTarih,denetID,dGorus,soruId))
    sqlconnection.commit()

def soruekleme():
    metin=input("soru metnini giriniz: ")
    yazar=str(input("yazar adi:"))
    tc=sqlcursor.execute("SELECT tc_no FROM yazar WHERE adi=?",(yazar,))
    tc = tc.fetchone()[0]

    cevap=input("cevap giriniz: ")
    zorluk=int(input("1-5 zorluk seviyesi giriniz: "))
    altkonu=str(input("altkonu adi:"))
    alt_konu_id=sqlcursor.execute("SELECT id FROM alt_konu WHERE adi=?",(altkonu,))
    alt_konu_id = alt_konu_id.fetchone()[0]
    denet_tarih=input("Denetleme tarihi: ")
    denetleyici=str(input("Denetleyici : "))

    denet_id=sqlcursor.execute("SELECT tc_no FROM denetleyici WHERE adi=?",(denetleyici,))
    denet_id = denet_id.fetchone()[0]

    denet_gorus=input("Denetleyici gorusu: ")
    sqlcursor.execute("INSERT INTO soru (metin,yazar_id,cevap,zorluk,alt_konu_id,denetleme_tarihi,denetleyici_id,denetleyici_gorus)"
                      " VALUES (?,?,?,?,?,?,?,?)",(metin,tc,cevap,zorluk,alt_konu_id,denet_tarih,denet_id,denet_gorus))

def konuekleme():
    konu=input("Lutfen konu basligini giriniz: ")
    sqlcursor.execute("INSERT INTO konu (adi) VALUES (?)",(konu,))

def kursekleme():
    ad=input("Kursun Adi: ")
    baslangic=input("Baslangic tarihi: ")
    sure=int(input("Kursun suresi: "))
    sqlcursor.execute("INSERT INTO kurs (adi,baslangic_tarih,sure) VALUES (?,?,?)",(ad,baslangic,sure))

def uniekleme():
    adi=input("Universite Adi: ")
    sqlcursor.execute("INSERT INTO universite (adi) VALUES (?)",(adi,))

def altkonuekleme():
    sql = "SELECT * FROM konu"
    listeleme(sql)
    konuadi=str(input("konu basligi seciniz: "))
    alt_konu=input("alt konu basligi: ")
    id=sqlcursor.execute("SELECT id FROM konu WHERE adi=?",(konuadi,))
    id = id.fetchone()[0]
    sqlcursor.execute("INSERT INTO alt_konu (adi,konu_id) VALUES (?,?)",(alt_konu,id))

def yazarekleme():
    tcNo=int(input("TC kimlik: "))
    mezuniyet=int(input("Mezuniyet: "))
    ad=input("Adi:")
    soyad=input("Soyadi:")
    adres=input("adres:")
    cinsiyet=input("Cinsiyet:")
    uzmanlik=input("Uzmanlik:")
    sqlcursor.execute("INSERT INTO yazar (tc_no,adi,soyadi,cinsiyet,adres,mezuniyet_yili,uzmanlik_alani) VALUES (?,?,?,?,?,?,?)",(tcNo,ad,soyad,cinsiyet,adres,mezuniyet,uzmanlik))

def denetleyiciekleme():
    tcNo=int(input("TC kimlik: "))
    ad=input("Adi:")
    soyad=input("Soyadi:")
    cinsiyet=input("Cinsiyet:")
    adres=input("adres:")
    akademik=input("Akademik: ")
    uzmanlik=input("Uzmanlik:")

    uni=str(input("Universite adi:"))
    id=sqlcursor.execute("SELECT id FROM universite WHERE adi=?",(uni,))
    id = id.fetchone()[0]

    sqlcursor.execute("INSERT INTO denetleyici (tc_no,adi,soyadi,cinsiyet,adres,akademik_unvan,uzmanlik_alani,uni_id) VALUES (?,?,?,?,?,?,?,?)",(tcNo,ad,soyad,cinsiyet,adres,akademik,uzmanlik,id))

def listeleme(sql):
    sqlcursor.execute(sql)
    result = sqlcursor.fetchall()
    for rs in result:
        print(rs)

def sorudenetleme():
    sql = "SELECT * FROM soru"
    sql1 = "SELECT * FROM denetleyici"

    listeleme(sql)
    sId=int(input("id sini giriniz: "))
    sqlcursor.execute("SELECT zorluk,denetleme_tarihi,denetleyici_id,denetleyici_gorus FROM soru WHERE Id=?",(sId,))
    rs=sqlcursor.fetchone()
    print(rs)
    zorluk=int(input("1-5 arasinda zorluk seviyesi: "))
    dTarih=input("Denetleme Tarihi: ")
    dGorus=input("Denetleyici Gorus: ")
    listeleme(sql1)
    denetleyici = str(input("Denetleyici adi:"))
    denetID = sqlcursor.execute("SELECT tc_no FROM denetleyici WHERE adi=?", (denetleyici,))
    denetID = denetID.fetchone()[0]

    guncelle(zorluk,dTarih,dGorus,denetID,sId)

def yazarislemleri():
    print("*"*50)
    print("Yazar Listele ->1 \nYazar Ekleme -> 2")
    print("*"*50)
    yazarsecim=int(input("islem seciniz: "))
    if yazarsecim==1:
        sql = "SELECT * FROM yazar"
        listeleme(sql)
    elif yazarsecim==2:
        yazarekleme()

def denetlemeislemleri():
    print("*"*50)
    print("Denetleyici Listele ->1 \nDenetleyici Ekleme -> 2 \nSoru Denetleme -> 3")
    print("*"*50)
    denetlemesecim=int(input("islem seciniz: "))
    if denetlemesecim==1:
        sql = "SELECT * FROM denetleyici"
        listeleme(sql)
    elif denetlemesecim==2:
        denetleyiciekleme()
    elif denetlemesecim==3:
        sorudenetleme()
    else:
        print("Yanlis secim!!!")

def soruislemleri():
    print("*" * 50)
    print("Soru Listele ->1 \nSoru Ekleme -> 2 \nKonu Ekleme -> 3 \nAlt Konu Ekleme -> 4")
    print("*" * 50)
    soruSecim=int(input("Secim yapiniz: "))
    if soruSecim==1:
        sql = "SELECT * FROM soru"
        listeleme(sql)
    elif soruSecim==2:
        soruekleme()
    elif soruSecim==3:
        konuekleme()
    elif soruSecim==4:
        altkonuekleme()
    else:
        print("Yanlis secim!!!")


while True:
    clear=lambda:os.system('cls')
    clear()
    print("*"*50)
    print("Soru islemleri -> 1 \nYazar Islemleri -> 2 \nDenetleme Islemleri -> 3 \nKurs Islemleri -> 4 \nCIKIS -> 0")
    print("*" * 50)
    secim=int(input("Seciminizi yapiniz: "))
    if secim==1:
        soruislemleri()
    elif secim==2:
        yazarislemleri()
    elif secim==3:
        denetlemeislemleri()
    elif secim==4:
        kursekleme()
    else:
        break

    sqlconnection.commit()

sqlconnection.close()