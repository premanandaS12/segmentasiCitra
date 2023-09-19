from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles import finders
import psycopg2
import re
from .models import *
from PIL import Image
from django.templatetags.static import static
import io
import os

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

def makeImgToStatic(img):
    kel_asli=Image.open(io.BytesIO(img[0].imgAsli))
    kel_seg=Image.open(io.BytesIO(img[0].imgSeg))
    baseImg=os.path.join('static', 'images')
    kel_asli.save(os.path.join(baseImg,'kelAsli.png'))
    kel_seg.save(os.path.join(baseImg,'kelSeg.png'))

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

    def searchLuas(self,query):
        self.connect()
        self.cur.execute(query)
        rows=self.cur.fetchall()
        res=[]
        for row in rows:
            print(row[1])
            res.append(SegmentageImage(row[2], row[3], row[4], row[0], row[1]))
        self.close()
        return res
    
    def searchImg(self,query):
        self.connect()
        self.cur.execute(query)
        rows=self.cur.fetchall()
        res=[]
        for row in rows:
            print(row[1])
            res.append(ImageTampilan(row[0],row[1]))
        self.close()
        return res

def detailMonitor(request):
    if 'kelCari' in request.GET:
        namakel=request.GET["kelCari"]
        namakel=re.sub(' , ',',',namakel)

        if ',' in namakel:
            temp=namakel.split(',')
            kelurahan=temp[0]
            kota=temp[1]
            
            select_query_luas="SELECT labelzona, COUNT(labelzona), ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi FROM datasegmentasi INNER JOIN kelurahan ON kelurahan.id_kelurahan=datasegmentasi.id_kelurahan INNER JOIN kotakabupaten ON kotakabupaten.id_kotakabupaten=datasegmentasi.id_kotakabupaten WHERE namakelurahan='{0}' AND namakotakabupaten='{1}' GROUP BY labelzona,ukuran_grid_h, ukuran_grid_w, luas_per_pixel_km_persegi".format(kelurahan,kota)
            select_query_gambar="SELECT citrakelurahan, citrakelurahansegmentasi FROM dataCitra INNER JOIN kelurahan ON kelurahan.id_kelurahan=dataCitra.id_kelurahan INNER JOIN kotakabupaten ON kotakabupaten.id_kotakabupaten=dataCitra.id_kotakabupaten WHERE namakelurahan='{0}' AND namakotakabupaten='{1}'".format(kelurahan,kota)
        
        qad=QueryAndDb()
        resQueryLuas=qad.searchLuas(select_query_luas)
        resQueryImg=qad.searchImg(select_query_gambar)
        resPL, arrLuas=luas(resQueryLuas)
        makeImgToStatic(resQueryImg)
        return render(request,'DetailMonitoring.html', {'pencarian':True, 'namaWil': namakel.split(',')[0], 'res':resPL, 'arrLuas': arrLuas})
    else:
        return render(request,'DetailMonitoring.html', {'pencarian':False})
