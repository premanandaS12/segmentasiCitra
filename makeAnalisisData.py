# -*- coding: utf-8 -*-
"""
Created on Sun May 14 20:47:36 2023

@author: Dodong
"""
import pandas as pd
import os
import pickle as pkl
import time

# Class model untuk menyimpan  
class MetaData:
    def __init__(self,ukuran_h_citra,ukuran_w_citra,x_tile,y_tile,id_kecamatan,id_kota_kabupaten,id_provinsi,luas_per_pixel_km_persegi,id_kelurahan):
        self.ukuran_h_citra=ukuran_h_citra
        self.ukuran_w_citra=ukuran_w_citra
        self.x_tile=x_tile
        self.y_tile=y_tile
        self.id_kecamatan=id_kecamatan
        self.id_kota_kabupaten=id_kota_kabupaten
        self.id_provinsi=id_provinsi
        self.luas_per_pixel_km_persegi=luas_per_pixel_km_persegi
        self.id_kelurahan=id_kelurahan


class SegmentageData:
    def __init__(self):
        self.model_kab=None
        self.model_kota=None

    # Fungsi untuk cari id_provinsi 
    def searchProv(self, pathRTP, prov):
        df=pd.read_excel(pathRTP)
        prov=df.loc[df['Provinsi'] == prov]
        
        return prov.iloc[0]['Id_Provinsi']
    
    # Fungsi untuk cari id kota/kabupaten
    def searchKotaKabupaten(self, pathRTK, kotaKab):
        df=pd.read_excel(pathRTK)
        if '_' in kotaKab:
            temp=kotaKab.split('_')
            kotaKab=temp[0]+' '+temp[1]
        else:
            kotaKab=kotaKab
        kota=df.loc[df['KotaKabupaten'] == kotaKab]
        return kota.iloc[0]['Id_KotaKabupaten']
    
    # Fungsi untuk cari id kecamatan
    def searchKecamatan(self, pathRTKec, kecamatan):
        df=pd.read_excel(pathRTKec)
        kec=df.loc[df['Kecamatan'] == kecamatan]
        return kec.iloc[0]['Id_Kecamatan']
    
    # Fungsi untuk cari id kelurahan
    def searchKelurahan(self, pathRTKel, kelurahan):
        df=pd.read_excel(pathRTKel)
        kel=df.loc[df['Kelurahan'] == kelurahan]
        return kel.iloc[0]['Id_Kelurahan']

    # Fungsi untuk menyatukan metadata 
    def searchMetaData(self, pathRM, pathRTP, pathRTK, pathRTKec, pathRTKel, tileKel):
        print(pathRM)
        tileKel=tileKel.split('.')[0]+'.png'
        df=pd.read_excel(pathRM)
        metaTile=df.loc[df['Nama_File_Tile_Citra'] == tileKel]
        print(metaTile)
        print('prov ',metaTile.iloc[0]['Provinsi'])
        provinsi=self.searchProv(pathRTP, metaTile.iloc[0]['Provinsi'])
        kotaKab=self.searchKotaKabupaten(pathRTK, metaTile.iloc[0]['KotaKabupaten'])
        kec=self.searchKecamatan(pathRTKec, metaTile.iloc[0]['Kecamatan'])
        kel=self.searchKelurahan(pathRTKel, metaTile.iloc[0]['Kelurahan'])
        return MetaData(metaTile.iloc[0]['Ukuran_h'], metaTile.iloc[0]['Ukuran_w'], metaTile.iloc[0]['x'], metaTile.iloc[0]['y'], kec, kotaKab, provinsi, metaTile.iloc[0]['Luas_Per_Pixel_Km_Persegi'], kel)
    
   
    # Fungsi untuk melakukan koreksi nilai - HSV di DF
    def correction(self, df):
        df.loc[df.H1<0,'H1'] += 256
        df.loc[df.S1<0,'S1'] += 256
        df.loc[df.V1<0,'V1'] += 256
        df.loc[df.H2<0,'H2'] += 256
        df.loc[df.S2<0,'S2'] += 256
        df.loc[df.V2<0,'V2'] += 256
        df.loc[df.H3<0,'H3'] += 256
        df.loc[df.S3<0,'S3'] += 256
        df.loc[df.V3<0,'V3'] += 256
        return df
    
    # Fungsi untuk menyesuaikan data ke format df
    def to_df(self, label, metadata, x, y, ukuranGrid):
        arr_df=[]
        for i in range(len(label)):
            temp=[]
            temp.append(metadata.id_kelurahan)
            temp.append(metadata.ukuran_h_citra)
            temp.append(metadata.ukuran_w_citra)
            temp.append(metadata.x_tile)
            temp.append(metadata.y_tile)
            temp.append(256)
            temp.append(256)
            temp.append(ukuranGrid[i])
            temp.append(ukuranGrid[i])
            temp.append(x[i])
            temp.append(y[i])
            temp.append(metadata.id_kecamatan)
            temp.append(metadata.id_kota_kabupaten)
            temp.append(metadata.id_provinsi)
            temp.append(metadata.luas_per_pixel_km_persegi)
            temp.append(label[i])
            arr_df.append(temp)
        column=['Id_Kelurahan', 'Ukuran_h_citra_full', 'Ukuran_w_citra_full', 'x_tile','y_tile', 'Ukuran_h_citra_tile', 'Ukuran_w_citra_tile', 'ukuran_grid_h','ukuran_grid_w','x_grid','y_grid','Id_Kecamatan','Id_KotaKabupaten','Id_Provinsi', 'Luas_Per_Pixel_Km_Persegi', 'LabelZona']
        df=pd.DataFrame(data=arr_df,columns=column)
        return df

    # Fungsi untuk write df ke dalam file .xlsx 
    def writeDf(self, df, pathW):
        df.to_excel(pathW+'.xlsx',index=(False))
    
    # Fungsi untuk baca fitur 
    def readFeature(self, pathR):
        df=pd.read_excel(pathR)
        feature=df.iloc[:,5:]
        x=df.iloc[:,2]
        y=df.iloc[:,3]
        ukuranGrid=df.iloc[:,4]
        return feature,x,y,ukuranGrid

    # Fungsi untuk predict DF menggunakan model RF 
    def predict(self, df_fitur, kota):
        if kota==False:
            return self.model_kab.predict(df_fitur)
        else:
            return self.model_kota.predict(df_fitur)

    # Fungsi untuk membuat data file image gambar citra kelurahan asli dengan ide kelurahan, kecamatan, provinsi, kota/kab
    def to_df_image(self, pathImage, metadata):
        temp=[]
        temp.append(metadata.id_kelurahan)
        temp.append(metadata.id_kecamatan)
        temp.append(metadata.id_kota_kabupaten)
        temp.append(metadata.id_provinsi)
        temp.append(pathImage)
        return temp

    # Fungsi untuk membuat df image ke file .xlsx
    def write_df_img(self,pathWImg,arr_df):
        column=['Id_Kelurahan','Id_Kecamatan','Id_KotaKabupaten','Id_Provinsi', 'Path_Image']
        df=pd.DataFrame(data=arr_df,columns=column)
        df.to_excel(pathWImg+'.xlsx', index=False)
    
    # Fungsi untuk membuat df waktu ke file .xlsx
    def write_df_waktu(self,pathWAnalisisWaktu,arr_df):
        column=['Kelurahan','Kota','Waktu_Analisis']
        df=pd.DataFrame(data=arr_df,columns=column)
        df.to_excel(pathWAnalisisWaktu+'.xlsx',index=False)
    
    # Fungsi untuk load model klasifikasi dari file pkl
    def load(self, first, kota):
        if first==True:
            self.model_kab=pkl.load(open('D:\\Skripsi\\DownloadGambar\\CitraNew\\Model\\Iter 2\\Undersampling\\rf_kab_undersampling.pkl','rb'))
            self.model_kota=pkl.load(open('D:\\Skripsi\\DownloadGambar\\CitraNew\\Model\\Iter 2\\Undersampling\\rf_kota_undersampling.pkl','rb'))
    
    # FUngsi untuk menyesuaikan format data waktu yang dibutuhkan dari proses analisis ke dalam array untuk dijadikan file xlsx 
    def to_df_waktu_analisis(self,waktu,kelurahan,kota):
        temp=[]
        temp.append(kelurahan)
        temp.append(kota)
        temp.append(waktu)
        return temp
    
    # Fungsi untuk membulatkan waktu ke format jam, menit, detik
    def time_convert(self,sec):
      mins = sec // 60
      sec = sec % 60
      hours = mins // 60
      mins = mins % 60
      elapsed_time="{0}:{1}:{2}".format(int(hours),int(mins),sec)
      print(elapsed_time)
      return elapsed_time
        
    def main(self, pathRF, pathRM, pathRTP, pathRTK, pathRTKel, pathRTKec, pathW, pathRCitra, pathWImg, pathWWaktu):
        prov=os.listdir(pathRF)
        kota=False
        first=True
        for i in prov:
            tempPathProvM=os.path.join(pathRM,i)
            tempPathProvF=os.path.join(pathRF,i)
            tempPathProvCitra=os.path.join(pathRCitra,i)
            tempPathProvW=os.path.join(pathW,i)
            tempPathWImgProv=os.path.join(pathWImg,i)
            tempPathWWaktuProv=os.path.join(pathWWaktu,i)
            if not os.path.exists(tempPathProvW):
                os.mkdir(tempPathProvW)
            if not os.path.exists(tempPathWImgProv):
                os.mkdir(tempPathWImgProv)
            if not os.path.exists(tempPathWWaktuProv):
                os.mkdir(tempPathWWaktuProv)
            cities=os.listdir(tempPathProvF)
            arr_df_img=[]
            arr_waktu=[]
            for city in cities:
                if 'Kota' in city:
                    kota=True
                else:
                    kota=False
                print(city)
                tempPathCityM=os.path.join(tempPathProvM,city)+'.xlsx'
                tempPathCityF=os.path.join(tempPathProvF,city)
                tempPathCityCitra=os.path.join(tempPathProvCitra,city)
                tempPathCityW=os.path.join(tempPathProvW,city)
                tempPathWImgCity=os.path.join(tempPathWImgProv,city)
                tempPathWWaktuCity=os.path.join(tempPathWWaktuProv,city)
                if not os.path.exists(tempPathCityW):
                    os.mkdir(tempPathCityW)
                kelList=os.listdir(tempPathCityF)
                for kel in kelList:
                    print(kel)
                    tempPathKelF=os.path.join(tempPathCityF,kel)
                    tempPathKelCitra=os.path.join(tempPathCityCitra,kel)+'.png'
                    tempPathKelW=os.path.join(tempPathCityW,kel)
                    if not os.path.exists(tempPathKelW):
                        os.mkdir(tempPathKelW)
                    tiles=os.listdir(tempPathKelF)
                    start=time.time()
                    for tile in tiles:
                        tempPathTileF=os.path.join(tempPathKelF,tile)
                        tempPathTileW=os.path.join(tempPathKelW,tile)
                        try:
                            metadata=self.searchMetaData(tempPathCityM, pathRTP, pathRTK, pathRTKec, pathRTKel, tile)
                            feature,x,y,ukuranGrid=self.readFeature(tempPathTileF)
                            df=self.correction(feature)
                            self.load(first, kota)
                            first=False
                            labelZona=self.predict(df, kota)
                            df_seg_image=self.to_df(labelZona, metadata, x, y, ukuranGrid)
                            self.writeDf(df_seg_image, tempPathTileW)
                        except:
                            break
                    stop=time.time()
                    elapsed_time=stop-start
                    lama=self.time_convert(elapsed_time)
                    arr_df_img.append(self.to_df_image(tempPathKelCitra, metadata))
                    arr_waktu.append(self.to_df_waktu_analisis(lama,kel,city))
                self.write_df_img(tempPathWImgCity, arr_df_img)
                self.write_df_waktu(tempPathWWaktuCity, arr_waktu)
                arr_df_img=[]
                arr_waktu=[]

sd=SegmentageData()                     
sd.main('D:\\Skripsi\\DownloadGambar\\CitraNew\\Warna', 'D:\\Skripsi\\DownloadGambar\\CitraNew\\Metadata', 'D:\\Data Star Schema\\Tabel Provinsi\\Provinsi.xlsx','D:\\Data Star Schema\\Tabel Kota\\KotaKab.xlsx', 'D:\\Data Star Schema\\Tabel Kelurahan\\Kelurahan_Unique.xlsx', 'D:\\Data Star Schema\\Tabel Kecamatan\\Kecamatan.xlsx', 'D:\\Data Star Schema\\Segmentage Image Undersampling', 'D:\\Skripsi\\DownloadGambar\\CitraNew\\Full', 'D:\\Data Star Schema\\Tabel Img Undersampling','D:\\Data Star Schema\\Waktu Undersampling') 