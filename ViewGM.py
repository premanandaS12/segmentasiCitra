from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles import finders
import psycopg2
import re
from .models import SegmentageImage, PemanfaatanLahan

def persentase(luasPL,luasPLTotal):
    percentage=luasPL/luasPLTotal*100
    return "{:.2f}".format(percentage)

def luas(segIm):
    luasPLTotal=0
    luasPLArr=[0,0,0,0,0,0,0,0]
    res=[]
    pemanfaatan=['RTH','Pertanian','Bangunan Non Industri','Bangunan Industri','Tambak','Perairan','Transportasi']
    # del segIm[0]
    for i in segIm:
        if i.labelZona==1:
            luasPLArr[1]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==2:
            luasPLArr[2]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==3:
            luasPLArr[3]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==4:
            luasPLArr[4]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==5:
            luasPLArr[5]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==6:
            luasPLArr[6]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==7:
            luasPLArr[7]+=int(i.ukuran_grid_h)*int(i.ukuran_grid_w)*float(i.luas_Per_Pixel_Km_Persegi)*int(i.jumlah)
        elif i.labelZona==0:
            luasPLArr[0]=0
    for i in luasPLArr:
        luasPLTotal+=i
    i=1
    for i in range(1,len(luasPLArr)):
        res.append(PemanfaatanLahan(i,pemanfaatan[i-1],"{:.2f}".format(luasPLArr[i]),persentase(luasPLArr[i],luasPLTotal)))
    del luasPLArr[0]
    return res, luasPLArr

class QueryAndDb():
    def __init__(self):
        self.db_name='segmentasiCitra'
        self.username='postgres'
        self.hostname='localhost'
        self.pwd='123'
        self.port_num="5432"

    def connect(self):
        self.conn = psycopg2.connect(
                    database=self.db_name,
                    user=self.username,
                    password=self.pwd,
                    host=self.hostname,
                    port=self.port_num
                    )
        self.cur=self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def search(self,query):
        self.connect()
        self.cur.execute(query)
        rows=self.cur.fetchall()
        res=[]
        for row in rows:
            print(row[1])
            res.append(SegmentageImage(row[2], row[3], row[4], row[0], row[1]))
        self.close()
        return res



def home(request):
    if 'tingkatcari' and 'namawilayah' in request.GET:
        Kelurahan=False
        Kecamatan=False
        Kota=False
        Provinsi=False
        tingkatPencarian=request.GET["tingkatCari"]
        if tingkatPencarian=="Kelurahan":
            Kelurahan=True
        elif tingkatPencarian=="Kecamatan":
            Kecamatan=True
        elif tingkatPencarian=="KotaKabupaten":
            Kota=True
        elif tingkatPencarian=="Provinsi":
            Provinsi=True
        wilayah=request.GET["namawilayah"]
        wilayah=re.sub(', ',',',wilayah)

        if ',' in wilayah and tingkatPencarian=='Kelurahan':
            temp=wilayah.split(',')
            kelurahan=temp[0]
            kota=temp[1]
            
            select_query="SELECT labelzona, COUNT(labelzona), ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi FROM datasegmentasi INNER JOIN kelurahan ON kelurahan.id_kelurahan=datasegmentasi.id_kelurahan INNER JOIN kotakabupaten ON kotakabupaten.id_kotakabupaten=datasegmentasi.id_kotakabupaten WHERE namakelurahan='{0}' AND namakotakabupaten='{1}' GROUP BY labelzona,ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi".format(kelurahan,kota)
        elif ',' in wilayah and tingkatPencarian=='Kecamatan':
            temp=wilayah.split(',')
            kecamatan=temp[0]
            kota=temp[1]
            select_query="SELECT labelzona, COUNT(labelzona), ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi FROM datasegmentasi INNER JOIN kecamatan ON kecamatan.id_kecamatan=datasegmentasi.id_kecamatan INNER JOIN kotakabupaten ON kotakabupaten.id_kotakabupaten=datasegmentasi.id_kotakabupaten WHERE namakecamatan='{0}' AND namakotakabupaten='{1}' GROUP BY labelzona,ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi".format(kecamatan,kota)
        elif tingkatPencarian=='KotaKabupaten':
            if len(wilayah.split(','))>1:
                temp=wilayah.split(',')
                kota=temp[0]
            else:
                kota=wilayah
            select_query="SELECT labelzona, COUNT(labelzona), ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi FROM datasegmentasi INNER JOIN kotakabupaten ON kotakabupaten.id_kotakabupaten=datasegmentasi.id_kotakabupaten WHERE namakotakabupaten='{0}' GROUP BY labelzona,ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi".format(kota)
        elif tingkatPencarian=='Provinsi':
            prov=wilayah
            select_query="SELECT labelzona, COUNT(labelzona), ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi FROM datasegmentasi INNER JOIN provinsi ON provinsi.id_provinsi=datasegmentasi.id_provinsi WHERE namaprovinsi='{0}' GROUP BY labelzona,ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi".format(prov)
        
        qad=QueryAndDb()
        resquery=qad.search(select_query)
        # res.pop(0)
        resPL, arrLuas=luas(resquery)
        return render(request,'GeneralMonitoring.html', {'pencarian':True, 'kelurahan': Kelurahan, 'kecamatan':Kecamatan, 'kota':Kota, 'provinsi': Provinsi, 'wilayah':wilayah, 'TingkatCari':tingkatPencarian, 'namaWil': wilayah.split(',')[0], 'res':resPL, 'arrLuas': arrLuas})
    else:
        return render(request,'GeneralMonitoring.html', {'pencarian':False})
    # return render("<h1>Hello hehe</h1>")


    




    
