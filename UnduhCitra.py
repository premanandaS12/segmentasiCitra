# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:02:02 2023

@author: Premananda Setyo
"""

import urllib.request
from PIL import Image
import os
import math
import numpy as np
import time
import requests
import shutil
import io
import cv2
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GoogleMapsLayers:
  ROADMAP = "v"
  TERRAIN = "p"
  ALTERED_ROADMAP = "r"
  SATELLITE = "s"
  TERRAIN_ONLY = "t"
  HYBRID = "y"


class GoogleMapDownloader:
    #fungsi inisialisasi jika parameter tidak di set di inisialisasi kelas maka parameter akan mengambil nilai default
    def __init__(self, box_coord, zoom=12, layer=GoogleMapsLayers.ROADMAP):
        self._box_coord = box_coord
        self._zoom = zoom
        self._layer = layer

    #konveri koordinat desimal ke koordinat tiles
    def getXY(self):
        #membuat array kosong untuk menampung koordinat tiles
        point_coord = np.empty((1,2))
        #perulangan untuk membaca koordinat desimal di axis 0
        for i in range(0, self._box_coord.shape[0]):
            #const nilai dari lebar dan panjang gambar tiles
            tile_size = 256
            #menentukan jumlah tiles dari zoom level
            numTiles = 1 << self._zoom
            #menentukan koordinat tiles, refrensi https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#ECMAScript_.28JavaScript.2FActionScript.2C_etc..29
            #menentukan nilai x dari koordinat tiles
            point_x = (tile_size / 2 + self._box_coord[i][1] * tile_size / 360.0) * numTiles // tile_size
            #menentukan nilai y dari koordinat tiles
            sin_y = math.sin(self._box_coord[i][0] * (math.pi / 180.0))
            point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size
            #memasukan nilai x dan y kedalam array
            point = np.array([[int(point_x), int(point_y)]])
            if i == 0:
                #jika koordinat cuma berupa 1 titik maka data point_coord[0] adalah point
                point_coord[0] = point
            else:
                #jika koordinat berupa beberapa titik maka data point ditambahkan ke point_coord
                point_coord = np.append(point_coord, point, axis=0)
        #mengembalikan data point koord
        return point_coord

    def downloader1(self,url,x,y,current_tile):
        req=requests.get(url,stream=True)
        try:
          req.raw.decode_content=True
          with open(current_tile,'wb') as f:
            shutil.copyfileobj(req.raw,f) 
        except:
          print('failed')
        # im=Image.open(io.BytesIO(req.raw))
        im = Image.open(current_tile).convert('RGB')
        im_temp=np.array(im)
        im_temp=cv2.cvtColor(im_temp, cv2.COLOR_BGR2RGB)
        im_res=Image.fromarray(im_temp)
        os.unlink(current_tile)
        return im_res

    #download gambar peta
    def generateImage(self):
        print('gen img')
        #konversi koordinat desimal ke koordinat tiles
        box_coord = self.getXY()
        #mengetahui lebar dari tiles
        tile_width = int(box_coord[1][0] - box_coord[0][0]) + 1
        #mengetahui tinggi dari tiles
        tile_height = int(box_coord[2][1] - box_coord[1][1]) + 1
        #mengetahui lebar dan tinggi gambar peta yang akan di download
        width, height = 256 * tile_width, 256 * tile_height
        print('width ', width)
        print('height ' , height)
        print('twidth ', tile_width)
        print('theight ' , tile_height)
        #membuat image baru sesuai lebar dan tinggi gambar peta
        map_img = Image.new('RGB', (width, height))
        #perulangan untuk mendownload gambar peta sesuai banyak lebar tiles
        for x in range(0, tile_width):
            print('loop 1: ', x)
            #perulangan untuk mendownload gambar peta sesuai banyak tinggi tiles
            for y in range(0, tile_height):
                print('loop 2: ', y)
                #api untuk download gambar maps sesuai koordinat tiles
                
                url = f'https://mts0.googleapis.com/vt?lyrs={self._layer}&x=' + str(int(box_coord[0][0]) + x) + '&y=' + str(int(box_coord[0][1]) + y) + '&z=' + str(self._zoom)

                current_tile = str(x) + '-' + str(y)

                im=self.downloader1(url,x,y,current_tile)
                #membuat request ke api
                
                # urllib.request.urlretrieve(url, current_tile)
                print(current_tile)
                # #menggabungkan satu tiles gambar yang sudah di download ke dalam map_image
                # im = Image.open(current_tile)
                map_img.paste(im, (x * 256, y * 256))
                #menghapus gambar satu tile yang sudah di download
                # os.remove(current_tile)
                # os.unlink(current_tile)
                time.sleep(3)
                print('msk generate img')
        #mengembalikan gambar yang sudah selesai di download
        return map_img, width, height
    

path_name = "D:\\Skripsi\\DownloadGambar\\Gambar" 
img_name = path_name + "Maps_HR.png"

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
        bawah = np.min(latitude)
        #mengambil koordinat paling bawah dari hasil longitude paling kecil
        atas = np.max(latitude)
        #membuat array yang berisi 4 titik pojok
        # coord = np.array([[atas, kiri], [atas, kanan], [bawah, kiri], [bawah, kanan]])
        coord = np.array([[atas, kiri], [atas, kanan], [bawah, kiri], [bawah, kanan]])
        #mengembalikan nilai 4 titik pojok
        # print(coord)
        return coord

    #menentukan koordinat tengah dari peta tiles
    def get_img_coord(self, ujung_box):
        #mengubah parameter ujung_box menjadi numpy array
        ujung_box = np.array(ujung_box)
        #menentukan jumlah tiles dari zoom level
        numTiles = 1 << self._zoom
        #menentukan pannjang 1 derajat dari jumlah tiles karena bumi itu bundar maka dipakai rumus 360 / jumlah tiles
        oneDegres = 360 / numTiles
        #menentukan koordinat tengah tiles kiri
        kiri = ujung_box[0][1] - (ujung_box[0][1] % oneDegres)
        #menentukan koordinat tengah tiles kanan
        kanan = (ujung_box[1][1] - (ujung_box[1][1] % oneDegres)) + oneDegres
        #menentukan koordinat tengah tiles atas
        atas = -1 * (abs(ujung_box[0][0]) - (abs(ujung_box[0][0]) % oneDegres)) 
        #menentukan koordinat tengah tiles bawah
        bawah = -1 * (abs(ujung_box[2][0]) - (abs(ujung_box[2][0]) % oneDegres)) - oneDegres
        #membuat array dari nilai koordinat tengah
        coord = np.array([[atas, bawah], [kiri, kanan]])
        #mengembalikan nilai koordinat tengah
        return coord

    #konversi data koordinat desimal ke koordinat pixel
    def coord_to_pixel(self, ujung_image, data_coord):
        #mengubah parameter data_coord menjadi numpy array
        data_coord = np.array(data_coord)
        #opencv membaca gambar yang sudah di download
        # real_image = cv2.imread(img_name)
        real_image = np.array(self.image)
        #mengetahui pixel tinggi lebar dan channel dari bentuk gambar
        # h, w, c = real_image.shape
        #membuat array pixel_coord dengan tipe data int 32
        pixel_coord = np.empty((1,2), np.int32)
        #perlulangan untuk membaca data koordinat di axis 0
        for i in range(0, data_coord.shape[0]):
            #konversi titik y dari koordinat
            y = (self.height * (abs(data_coord[i][1]) - abs(ujung_image[0][0]))) / (abs(ujung_image[0][1]) - abs(ujung_image[0][0]))
            #konversi titik x dari koordinat
            x = (self.width * (abs(data_coord[i][0]) - abs(ujung_image[1][0]))) / (abs(ujung_image[1][1]) - abs(ujung_image[1][0]))
            #membuat array point untuk menampung nilai x dan y
            point = np.array([[int(x), int(y)]])
            if i == 0:
                pixel_coord[0] = point
            else:
                pixel_coord = np.append(pixel_coord, point, axis=0)
        #mengembalikan nilai koordinat yang sudah dijadikan koordinat pixel
        return pixel_coord

    #mengaplikasikan batasan pixel menurut koordinat pixel
    # FUNGSI INI YG DIBUTUHKAN UNTUK CROP IMAGE KOTAK (HASIL PENGGABUNGAN TILE-TILE)
    # BERDASAR BATAS-BATAS KELURAHAN  
    def draw_contour(self, pixel_coord):
        #opencv membaca gambar
        # real_image = cv2.imread(img_name)
        real_image = np.array(self.image)
        #membuat bounding rect (kotak) dari koordinat pixel
        rect = cv2.boundingRect(pixel_coord)
        #mengambil nilai x y w h
        x,y,w,h = rect
        #melakukan cropping gambar
        croped = real_image[y:y+h, x:x+w].copy()
        #membuat masking gambar
        pixel_coord = pixel_coord - pixel_coord.min(axis=0)
        mask = np.zeros(croped.shape[:2], np.uint8)
        #membuat kontur sesuai masking gambar
        cv2.drawContours(mask, [pixel_coord], -1, (255, 255, 255), -1, cv2.LINE_AA)
        #operasi bitwise and untuk mengeleminasi gambar di luar kontur    
        dst = cv2.bitwise_and(croped, croped, mask=mask)
        #merubah gambar yang sudah di eleminasi menjadi putih
        bg = np.ones_like(croped, np.uint8)*255
        cv2.bitwise_not(bg,bg, mask=mask)
        #menggabuungkan antara di dalam kontur dan diluar kontur yang sudah diganti warnanya
        dst2 = bg + dst
        #menyimpan gambar hasil masking sebagai assets
        # filename = 'peta_kelurahan.png'
        # plt.imshow(dst2)
        # cv2.imwrite(os.path.join(path_name , filename), dst2)
        #mengembalikan gambar hasil, gambar asli, dan masking
        return croped, mask, dst2
        # return dst2

    #membaca file json dan hanya mengembalikan data yang berupa koordinat
    def read_json(self,data_path):
        #buka file json sesuai parameter data_path
        f = open(data_path,)
        #baca data json
        data = json.load(f)
        f.close()
        #mengembalikan hanya data koordinat dari file json yang dibaca
        res=[]
        try:
            print('msk try')
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
            print('msk except try')
            res=data['geometry']['coordinates']
          except:
            print('msk except except')
            res=data['features'][0]['geometry']['coordinates'][0]
        return res

    def setImg(self,img):
      self.image=img

    #download maps sesuai koordinat
    def map_download(self, ujung_box):
        #inisialisasi kelas GoogleMapDownloader
        gmd = GoogleMapDownloader(ujung_box, self._zoom, GoogleMapsLayers.SATELLITE)
        # print("The tile coorindates are {}".format(gmd.getXY()))
        try:
            #download gambar peta
            print('mau generate img')
            img,w,h = gmd.generateImage()
            self.width=w
            self.height=h
        except IOError:
            print('Gagal')
            breakpoint
        else:
            # img.save(img_name)
            self.setImg(img)
            print("Download Maps Sukses")
            
    def writeToCSV(self,pathW,kota):
        df1=pd.DataFrame(data=np.array(self.df),columns=['Kelurahan','Kota','Provinsi','Panjang_Tile','Lebar_Tile','x','y', 'Luas_Per_Pixel(m2)','Image'])
        namaFileRGB=os.path.join(pathW, kota)+'.csv'
        df1.to_csv(namaFileRGB)
        
    def saveFull(self,img,pathW,kelurahan):
        filename='{0}.png'.format(kelurahan)
        wPath=os.path.join(pathW,filename)
        print('wPath',wPath)
        cv2.imwrite(wPath,img)
    
    def toTile(self,img_Bersih,kelurahan,kota,provinsi,pathW):
        # Fungsi untuk memotong citra kelurahan yang diunduh jadi tile berukuran 256x256
        # Karena ukurannya 256x256, beri padding terhadap gambar yang ukurannya bukan merupakan kelipatan 256 px
        print('kelurahan: ', kelurahan)
        h=img_Bersih.shape[0]
        w=img_Bersih.shape[1]
        # print(w,h)
        img_Bersih=Image.fromarray(img_Bersih)
        # print(img_Bersih)
        tiles=[]
        if h%256!=0 and w%256!=0:
            height=math.ceil(h/256)*256
            width=math.ceil(w/256)*256
            res_img = Image.new('RGB', (width, height),color=(255,255,255))
            res_img.paste(img_Bersih,(0,0))
        elif h%256!=0 or w%256!=0:
            if h%256!=0 and w%256==0:
                height=math.ceil(h/256)*256
                width=w
                res_img = Image.new('RGB', (width, height),color=(255,255,255))
                res_img.paste(img_Bersih,(0,0))
            elif h%256==0 and w%256!=0:
                width=math.ceil(w/256)*256
                height=h
                res_img = Image.new('RGB', (width, height),color=(255,255,255))
                res_img.paste(img_Bersih,(0,0))
        elif h%256==0 or w%256==0:
            res_img=img_Bersih
        # print('res img ' ,res_img)
        ukuranTile=256
        panjang_tile=res_img.size[1]/256
        lebar_tile=res_img.size[0]/256
        print('pjg tile:', panjang_tile)
        print('lebar tile:', lebar_tile)
        res_img=res_img.convert('RGB')
        res_img=np.array(res_img)
        self.saveFull(res_img, pathW, kelurahan)
        # Lakukan penyimpanan citra kelurahan utuh yang telah diberi padding sebelum dipotong ke tile-tile citra kelurahan
        for i in range(0,res_img.shape[0],ukuranTile):
          for j in range(0,res_img.shape[1],ukuranTile):
            # Lakukan pemotongan citra kelurahan ke dalam tile ukuran 256x256 px
            newTile = np.ascontiguousarray(res_img[i : (i+ukuranTile), j : (j+ukuranTile) , :])
            tl=Tile(kelurahan, kota, provinsi, panjang_tile, lebar_tile, j//ukuranTile, i//ukuranTile, newTile)
            tiles.append(tl)
        return tiles
    
    def saveTile(self,tiles,pathW):
        # SImpan tile citra kelurahan sesuai dengan nomor urut pemotongannya
        for i in range(len(tiles)):
            filename='{0}_{1}.png'.format(tiles[i].kelurahan,str(i))
            wPath=os.path.join(pathW,filename)
            cv2.imwrite(wPath,tiles[i].img)
    
            
    def run(self, kelurahan, kota, provinsi, pathWFull, pathWTile):
        # #path data json
        path_json = self._filename
        # #baca data koordinat di dalam json
        coordinates =  self.read_json(path_json)
        #menentukan koordinat pojok dari daerah dalam satuan longitude dan latitude
        ujung_coordinates = self.get_box_coord(coordinates)
        print(ujung_coordinates)
        #menentukan koordinat peta yang akan di download
        ujung_image = self.get_img_coord(ujung_coordinates)
        print(ujung_image)

        #download peta sesuai koordinat
        self.map_download(ujung_coordinates)
        # konversi data latitude dan longitude ke koordinat pixel x dan y
        pixel_coord = self.coord_to_pixel(ujung_image, coordinates)
        # mengaplikasikan batasan kelurahan menurut koordinat pixel
        only_image, boundaries_mask, img = self.draw_contour(pixel_coord)
        # Jadikan citra kelurahan yang dipotong ke dalam bentuk tile, simpan juga versi fullnya
        tiles=self.toTile(img, kelurahan, kota, provinsi,pathWFull)
        # Simpan tile data citra kelurahan dalam format .png per file
        self.saveTile(tiles, pathWTile)
        

    def checker(self, pathSemua, pathBeres):
      lstBeres=os.listdir(pathBeres)
      lstAkhir=os.listdir(pathSemua)
      temp=[]
      for i in lstBeres:
        temp.append(i.split('.')[0]+'.json')
      for i in temp:
        lstAkhir.remove(i)
      # print(temp)
      # print(lstAkhir)
      return lstAkhir

    def runBulk(self,pathR):
        # Baca path folder provinsi, list seluruh provinsi yang ada geojsonnya
        provList=os.listdir(pathR)
        # provList=['JawaTengah']
        for i in provList:
            if i=='JawaBarat':
                prov='Jawa Barat'
            elif i=='JawaTengah':
                prov='Jawa Tengah'
            elif i=='JawaTimur':
                prov='Jawa Timur'
            elif i=='KalimantanUtara':
                prov='Kalimantan Utara'
            # Buat folder per provinsi jika tidak ada. Folder full untuk menyimpan citra kelurahan yang utuh tanpa dipotong
            # Folder tile untuk menyimpan potongan citra per tile (256x256 px) yang telah dipotong dari citra kelurahan 
            tempPathProv=os.path.join(pathR,i)
            provWFull=os.path.join('D:\\Skripsi\\DownloadGambar\\CitraNew\\Full',i)
            if not os.path.exists(provWFull):
                os.mkdir(provWFull)
            provWTile=os.path.join('D:\\Skripsi\\DownloadGambar\\CitraNew\\Tile',i)
            if not os.path.exists(provWTile):
                os.mkdir(provWTile)
            cities=os.listdir(tempPathProv)
            # Buat folder per kota untuk menampung kelurahan-kelurahan di dalamnya
            for city in cities:
                cityWFull=os.path.join(provWFull,city)
                if not os.path.exists(cityWFull):
                    os.mkdir(cityWFull)
                cityWTile=os.path.join(provWTile,city)
                if not os.path.exists(cityWTile):
                    os.mkdir(cityWTile)
                tempCityR=os.path.join(tempPathProv,city)
                if 'Kota' in city:
                    self._zoom=18
                    kota=city.split('_')
                    kota=kota[0]+' '+kota[1]
                else:
                    self._zoom=16
                    kota=city
                # Lakukan check terhadap kelurahan yang telah diunduh, unduh citra kelurahan yang belum ada namun ada data jsonnya
                kelList=self.checker(tempCityR,cityWFull)
                if city=='Pemalang':
                    kelList.remove('Purwoharjo.json')
                elif city=='Rembang':
                    kelList.remove('Dresikulon.json')
                    kelList.remove('Dresiwetan.json')
                    kelList.remove('Gandrirojo.json')
                    kelList.remove('Japeledok.json')
                elif city=='Gresik':
                    kelList.remove('Abar-abir.json')
                for k in kelList:
                    kelWTile=os.path.join(cityWTile,k.split('.')[0])
                    if not os.path.exists(kelWTile):
                        os.mkdir(kelWTile)
                    tempCityR=os.path.join(tempPathProv,city)
                    self._filename=os.path.join(tempCityR, k)
                    kel=k.split('.')[0]
                    self.run(kel, kota, prov, cityWFull, kelWTile)

                    
fc=ForestCluster()
fc.runBulk('D:\\Skripsi\\Data Citra\\GeoJSON')

