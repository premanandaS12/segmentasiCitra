# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:02:02 2023

@author: Premananda Setyo
"""

import os
import numpy as np
import json
import numpy as np
import pandas as pd
import cv2


class Kelurahan:
  def __init__(self, idKel, namaKel, namaKec, namaKotaKab, namaProv):
    self.idKel=idKel
    self.namaKel=namaKel
    self.namaKec=namaKec
    self.namaKotaKab=namaKotaKab
    self.namaProv=namaProv
    

class ClusterUtility:
    def __init__(self,zoom,img,ujung_kel):
        self._zoom = zoom
        self._img = img
        self._ujung_kel = ujung_kel

    #fungsi untuk mengubah koordinat desimal ke degree minutes second
    def ddToDms(self,dd):
        is_positive = dd >= 0
        dd = abs(dd)
        minutes,seconds = divmod(dd*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        return (degrees,minutes,seconds)

    #fungsi untuk mengubah degree minutes second ke kilometer
    # INI TIDAK DIBUTUHKAN
    def ddToKm(self, d, m, s):
        deg = 111.32
        minutes = 1.85
        seconds= 0.0309
        km_degress = deg * d
        km_minutes = minutes * m
        km_second = seconds * s
        km_total = km_degress + km_minutes + km_second
        return km_total

    #fungsi untuk mengubah degree minutes second ke meter
    # INI TIDAK DIBUTUHKAN
    def kmToM(self, km, squared = False):
        m_total = 0
        if squared:
            m_total = km * 1000000
        else:
            m_total = km * 1000
        return m_total

    
    def getLuasPerPx(self):
        
        # [[bawah, kiri], [bawah, kanan], [atas, kiri], [atas, kanan]]
        
        #membuat array dari koordinat ujung peta
        ujung_kel = np.array(self._ujung_kel)
        #koordinat atas peta
        atas = ujung_kel[2][0]
        #koordinat bawah peta
        bawah = ujung_kel[0][0]
        #koordinat kiri peta
        kiri = ujung_kel[0][1]
        #koordinat kanan peta
        kanan = ujung_kel[1][1]
        #mengetahui jumlah tiles dalam peta pada zoom level
        numTiles = 1 << self._zoom
        #mengetahui 1 derajat dalam 1 tiles di dalam peta
        oneDegres = 360 / numTiles
        #mengetahui tinggi peta dalam koordinat
        tinggi = abs(bawah) - abs(atas)
        #mengetahui lebar peta dalam koordinat
        lebar = abs(kanan) - abs(kiri)
        #konversi tinggi peta ke degree minutes second
        degrees_tinggi, minutes_tinggi, seconds_tinggi = self.ddToDms(tinggi)
        #konversi lebar peta ke degree minutes second
        degrees_lebar, minutes_lebar, seconds_lebar = self.ddToDms(lebar)
        #konversi tinggi peta km
        km_tinggi = self.ddToKm(degrees_tinggi, minutes_tinggi, seconds_tinggi)
        #konversi lebar peta ke km
        km_lebar = self.ddToKm(degrees_lebar, minutes_lebar, seconds_lebar)
        #mengetahui tinggi satu pixel dalam satuan km
        satu_px_tinggi =  km_tinggi / self._img.shape[0]
        #mengetahui lebar satu pixel dalam satuan km
        satu_px_lebar = km_lebar  / self._img.shape[1]  
        #mengetahui luas satu pixel peta dalam satuan km persegi
        km_luas_satu_px = satu_px_tinggi * satu_px_lebar
        print('luas 1 px clu: ', km_luas_satu_px)
        return km_luas_satu_px
    



class Tile:
    def __init__(self, kelurahan, kota, provinsi, pTile, lTile, x, y,img):
      self.kelurahan=kelurahan
      self.kota=kota
      self.provinsi=provinsi
      self.pTile=pTile
      self.lTile=lTile
      self.x=x
      self.y=y
      self.img=img


class ForestCluster:
    def __init__(self, filename="", zoom = 18, k_proses = 7, grid_size = 3, grid_percentage = 60):
        self._filename = filename
        self._zoom = zoom
        self._k_proses = k_proses
        self._grid_size = grid_size
        self.df=[]
        self.image=[]
        self.width=0
        self.height=0

    #membaca data koordinat dan menentukan titik pojok dari koordinat
    def get_box_coord(self, data_coord):
        new_data_coord = []
        for data in data_coord:
            new_data_coord.append([data[0],data[1]])
        #mengubah parameter data_coord menjadi numpy array
        data_coord = np.array(new_data_coord)
        #membuat numpy array kosong untuk menampung longitude
        longitude = np.array([]) # garis bujur timur ke barat atau kanan ke kiri
        #membuat numpy array kosong untuk menampung latitude
        latitude = np.array([]) #garis lintang utara ke selatan atau atas ke bawah
        #pelulangan untuk membaca data 2 dimensi
        for i in range(0, data_coord.shape[1]):
            for j in range(0, data_coord.shape[0]):
                if i == 0:
                    #jika data di axis 0 maka ditambahkan ke array longitude
                    longitude = np.append(longitude, data_coord[j][i])
                elif i == 1:
                    #jika data di axis 1 maka ditambahkan ke array latitude
                    latitude = np.append(latitude, data_coord[j][i])
        #mengambil koordinat paling kanan dari hasil longitude paling besar
        kanan = np.max(longitude)
        #mengambil koordinat paling kiri dari hasil longitude paling kecil
        kiri = np.min(longitude)
        #mengambil koordinat paling atas dari hasil longitude paling besar
        atas = np.min(latitude)
        #mengambil koordinat paling bawah dari hasil longitude paling kecil
        bawah = np.max(latitude)
        #membuat array yang berisi 4 titik pojok
        # coord = np.array([[atas, kiri], [atas, kanan], [bawah, kiri], [bawah, kanan]])
        coord = np.array([[bawah, kiri], [bawah, kanan], [atas, kiri], [atas, kanan]])
        #mengembalikan nilai 4 titik pojok
        # print(coord)
        return coord


    #membaca file json dan hanya mengembalikan data yang berupa koordinat
    def read_json(self,data_path):
        #buka file json sesuai parameter data_path
        f = open(data_path,)
        #baca data json
        data = json.load(f)
        f.close()
        # print(data)
        #mengembalikan hanya data koordinat dari file json yang dibaca
        res=[]
        try:
            # print('msk try')
            # idKel=data['features'][0]['attributes']['OBJECTID']
            # WADMKD=data['features'][0]['attributes']['WADMKD']
            WADMKC=data['features'][0]['attributes']['WADMKC']
            # WADMKK=data['features'][0]['attributes']['WADMKK']
            # WADMPR=data['features'][0]['attributes']['WADMPR']
            temp=data['features'][0]['geometry']['rings']
            if len(temp)==1:
              print(len(temp))
              res=temp[0]
            elif len(temp)>1:
              print(len(temp))
              for i in temp:
                for j in i:
                  res.append(j)
        except:
          try:
            # print('msk except try')
            res=data['geometry']['coordinates']
            # idKel=data['properties']['OBJECTID']
            # WADMKD=data['properties']['WADMKD']
            WADMKC=data['properties']['WADMKC']
            # WADMKK=data['properties']['WADMKK']
            # WADMPR=data['properties']['WADMPR']
          except:
            # print('msk except except')
            res=data['features'][0]['geometry']['rings'][0]
            # idKel=data['features'][0]['attributes']['OBJECTID']
            # WADMKD=data['features'][0]['attributes']['WADMKD']
            try:
                WADMKC=data['features'][0]['attributes']['WADMKC']
            except:
                WADMKC='Unknown'
            # WADMKK=data['features'][0]['attributes']['WADMKK']
            # WADMPR=data['features'][0]['attributes']['WADMPR']
        # print(idKel,WADMKD,WADMKC,WADMKK,WADMPR)
        # self.kel=Kelurahan(idKel,WADMKD,WADMKC,WADMKK,WADMPR)
        # kel=Kelurahan(idKel,WADMKD,WADMKC,WADMKK,WADMPR)
        return res,WADMKC

    def ResizeWithAspectRatio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)

    def get_pxKm(self, img, ujung):
        clu = ClusterUtility(self._zoom,img, ujung)
        km_luas_satu_px=clu.getLuasPerPx()
        return km_luas_satu_px

    def setImg(self,img):
      self.image=img
            
    def writeToCSV(self,pathW):
        df1=pd.DataFrame(data=np.array(self.df),columns=['Id_Kelurahan','Kelurahan', 'Ukuran_h', 'Ukuran_w', 'x','y', 'Kecamatan','KotaKabupaten','Provinsi', 'Luas_Per_Pixel_Km_Persegi','Nama_File_Tile_Citra'])
        df1.to_excel(pathW+'.xlsx')
        
    
    def toDf(self, idKel, namaKel, ukuran_h, ukuran_w,  x, y, kec, namaKotaKab, namaProv, km_luas_satu_px, i):
            col=[]
            col.append(idKel)
            col.append(namaKel)
            col.append(ukuran_h)
            col.append(ukuran_w)
            col.append(x)
            col.append(y)
            col.append(kec)
            col.append(namaKotaKab)
            col.append(namaProv)
            col.append(km_luas_satu_px)
            col.append(i)
            self.df.append(col)
            
    def run(self, pathRFull, pathRTile, idKel, prov, city, kel):
        if prov=='JawaBarat':
            prov='Jawa Barat'
        elif prov=='JawaTengah':
            prov='Jawa Tengah'
        elif prov=='JawaTimur':
            prov='Jawa Timur'
        
        if 'Kota' in city:
            city=city.split('_')[0]+' '+city.split('_')[1]
        
        print('msk run')
        path_json = self._filename
        coordinates, kec =  self.read_json(path_json)
        ujung_coordinates = self.get_box_coord(coordinates)
        print(ujung_coordinates)
        print(pathRFull)
        img=cv2.imread(pathRFull)
        h,w,c =img.shape
        km_luas_satu_px = self.get_pxKm(img, ujung_coordinates)
        tiles=os.listdir(pathRTile)
        # print(tiles)
        for i in tiles:
            y,x=divmod(int(i.split('.')[0].split('_')[1]),w//256)
            print(idKel, kel, h//256, w//256, x, y, kec, city, prov, km_luas_satu_px, i)
            # time.sleep(3)
            self.toDf(idKel, kel, h//256, w//256, x, y, kec, city, prov,  km_luas_satu_px, i)
                
        
    def checker(self, pathSemua, pathBeres):
      
      lstBeres=os.listdir(pathBeres)
      lstAkhir=os.listdir(pathSemua)
      temp=[]
      for i in lstBeres:
        temp.append(i.split('.')[0])
      for i in temp:
        lstAkhir.remove(i)
      print(temp)
      print(lstAkhir)
      return lstAkhir

    def runBulk(self,pathRF,pathRT,pathWM,json,gagalMD):
        count=0
        provList=os.listdir(pathRF)
        for i in provList:
            tempPathProvF=os.path.join(pathRF,i)
            tempPathProvT=os.path.join(pathRT,i)
            tempPathProvM=os.path.join(pathWM,i)
            tempPathProvJ=os.path.join(json,i)
            tempPathProvG=os.path.join(gagalMD,i)
            cities=os.listdir(tempPathProvF)
            cities=self.checker(tempPathProvJ, tempPathProvM)
            for city in cities:
                df_failed=[]
                tempPathCityF=os.path.join(tempPathProvF,city)
                tempPathCityT=os.path.join(tempPathProvT,city)
                tempPathCityM=os.path.join(tempPathProvM,city)
                tempPathCityJ=os.path.join(tempPathProvJ,city)
                tempPathCityG=os.path.join(tempPathProvG,city)
                if 'Kota' in city:
                    self._zoom=18
                    kota=city.split('_')
                    kota=kota[0]+' '+kota[1]
                else:
                    self._zoom=16
                    kota=city
                kelList=os.listdir(tempPathCityF)
                kelJSON=os.listdir(tempPathCityJ)
                kel2=os.listdir(tempPathCityF)
                if city=='Pemalang':
                    kelJSON.remove('Purwoharjo.json')
                elif city=='Rembang':
                    kelJSON.remove('Dresikulon.json')
                    kelJSON.remove('Dresiwetan.json')
                    kelJSON.remove('Gandrirojo.json')
                    kelJSON.remove('Japeledok.json')
                elif city=='Gresik':
                    kelJSON.remove('Abar-abir.json')
                elif city=='Sumenep':
                    kelJSON.remove('Palo lo an.json')
                
                for k in range(len(kelList)):
                    self._filename=os.path.join(tempPathCityJ, kelJSON[k])
                    pathRFull=os.path.join(tempPathCityF, kel2[k])
                    pathRTile=os.path.join(tempPathCityT, kelList[k].split('.')[0])
                    if kelJSON[k].split('.')[0] in kelList[k].split('.')[0]:
                        try:
                            print('msk try')
                            if len(kel2[k].split('.'))==2:
                                self.run(pathRFull,pathRTile,count,i,city,kel2[k].split('.')[0])
                            else:
                                self.run(pathRFull,pathRTile,count,i,city,kel2[k].split('.')[0]+' '+kel2[k].split('.')[1])
                        except:
                            print('msk except')
                            df_failed.append(kelList[k])
                    count+=1
                if len(df_failed)!=0:
                    df_failed=pd.DataFrame(data=df_failed)
                    df_failed.to_csv(tempPathCityG+'.csv')
                
                self.writeToCSV(tempPathCityM)
                self.df=[]
                    
fc=ForestCluster()
fc.runBulk('D:\\Skripsi\\DownloadGambar\\CitraNew\\Full','D:\\Skripsi\\DownloadGambar\\CitraNew\\Tile','D:\\Skripsi\\DownloadGambar\\CitraNew\\Metadata','D:\\Skripsi\\Data Citra\\GeoJSON','D:\\Skripsi\\DownloadGambar\\CitraNew\\GagalMetaData')

