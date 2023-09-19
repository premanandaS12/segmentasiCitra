# -*- coding: utf-8 -*-
"""
Created on Thu May 26 20:29:49 2023

@author: Premananda Setyo
"""

import math
from PIL import Image, ImageDraw
import pandas as pd
import os
import time

class segmentageTile:
    def __init__(self, segImg, xTile, yTile, h, w):
        self.segImg=segImg
        self.xTile=xTile
        self.yTile=yTile
        self.canvasH=h
        self.canvasW=w

# Fungsi untuk membuat gambar hasil segmentasi dari hasil pemanfaatan lahan per grid. Setiap tipe pemanfaatan lahan dari grid akan diberi warna unik dan disatukan ke dalam sebuah canvas
# sehingga membentuk citra kelurahan hasil segmentasi 
def show_segmentate_tile(df):
    w=256
    h=256
    img = Image.new("RGB", (w, h))
    segimg = ImageDraw.Draw(img)  
    for i in range(len(df)):
        if df.loc[df.index[i],'LabelZona']==0:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#FEFFFE")
        elif df.loc[df.index[i],'LabelZona']==1:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#274e13")
        elif df.loc[df.index[i],'LabelZona']==2:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#b6d7a8")
        elif df.loc[df.index[i],'LabelZona']==3:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#D97557")
        elif df.loc[df.index[i],'LabelZona']==4:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#999999")
        elif df.loc[df.index[i],'LabelZona']==5:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#46bdc6")
        elif df.loc[df.index[i],'LabelZona']==6:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#073763")
        elif df.loc[df.index[i],'LabelZona']==7:
            segimg.rectangle(((df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w'], df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']), (df.loc[df.index[i],'x_grid']*df.loc[df.index[i],'ukuran_grid_w']+df.loc[df.index[i],'ukuran_grid_w'],df.loc[df.index[i],'y_grid']*df.loc[df.index[i],'ukuran_grid_h']+df.loc[df.index[i],'ukuran_grid_h'])), fill ="#4b4b50")
    
    # img.show()
    return img

# Fungsi untuk membuat data hasil segmentasi menjadi gambar citra kelurahan hasil segmentasi 
def make_kelurahan_utuh(arrGambar,pathW):
    print(arrGambar[0].canvasW,arrGambar[0].canvasH)
    canvas=Image.new('RGB', (arrGambar[0].canvasW*256,arrGambar[0].canvasH*256),color=(255,255,255))
    for i in arrGambar:
        canvas.paste(i.segImg,(i.xTile*256,i.yTile*256))
    canvas.save(pathW+'.png')
    # canvas.show()

# Fungsi untuk menghitung waktu pembuatan citra hasil segmentasi
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  elapsed_time="{0}:{1}:{2}".format(int(hours),int(mins),sec)
  print(elapsed_time)
  return elapsed_time

# Fungsi untuk melakukan write df
def write_df(arrTime,pathWWaktu):
    df=pd.DataFrame(data=arrTime,columns=['Kelurahan','Banyak Tile','Time'])
    df.to_excel(pathWWaktu+'.xlsx')

# Fungsi untuk membuat data hasil segmentasi menjadi gambar citra kelurahan hasil segmentasi (bulk)
def show_segmentage_kelurahan(pathR,pathW,pathWWaktu):
    prov=os.listdir(pathR)
    for i in prov:
        tempPathProvR=os.path.join(pathR,i)
        tempPathProvW=os.path.join(pathW,i)
        tempPathProvWWaktu=os.path.join(pathWWaktu,i)
        cities=os.listdir(tempPathProvR)
        if not os.path.exists(tempPathProvW):
            os.mkdir(tempPathProvW)
        if not os.path.exists(tempPathProvWWaktu):
            os.mkdir(tempPathProvWWaktu)
        cities=['Bandung_Barat','Bekasi','Cianjur', 'Karawang', 'Purwakarta']
        for city in cities:
            tempPathCityR=os.path.join(tempPathProvR,city)
            tempPathCityW=os.path.join(tempPathProvW,city)
            tempPathCityWWaktu=os.path.join(tempPathProvWWaktu,city)
            kelList=os.listdir(tempPathCityR)
            arrTime=[]
            if not os.path.exists(tempPathCityW):
                os.mkdir(tempPathCityW)
            for kel in kelList:
                arrGambar=[]
                tempPathKelR=os.path.join(tempPathCityR,kel)
                tempPathKelW=os.path.join(tempPathCityW,kel)
                print(tempPathKelW)
                tiles=os.listdir(tempPathKelR)
                start=time.time()
                for tile in tiles:
                    print(tile)
                    tempPathTileR=os.path.join(tempPathKelR,tile)
                    df=pd.read_excel(tempPathTileR)
                    img=show_segmentate_tile(df)
                    print(int(df.iloc[0]['x_tile']), int(df.iloc[0]['y_tile']), int(df.iloc[0]['Ukuran_h_citra_full']), int(df.iloc[0]['Ukuran_w_citra_full']))
                    arrGambar.append(segmentageTile(img, int(df.iloc[0]['x_tile']), int(df.iloc[0]['y_tile']), int(df.iloc[0]['Ukuran_h_citra_full']), int(df.iloc[0]['Ukuran_w_citra_full'])))
                make_kelurahan_utuh(arrGambar, tempPathKelW)
                stop=time.time()
                elapsed=stop-start
                lama=time_convert(elapsed)
                timeTemp=[]
                timeTemp.append(kel)
                timeTemp.append(len(tiles))
                timeTemp.append(lama)
                arrTime.append(timeTemp)
            write_df(arrTime, tempPathCityWWaktu)
            
                
                    
# show_segmentage_kelurahan('D:\\Data Star Schema\\Segmentage Image Undersampling', 'D:\\Data Star Schema\\Segmentasi Undersampling','D:\\Data Star Schema\\Waktu Penyatuan Gambar Undersampling')
                    
# Fungsi untuk membuat data untuk dimasukkan ke tabel citra di Data Warehouse  
def makeTabelCitra(pathRF, pathRI, pathW):
    prov=os.listdir(pathRF)
    for i in prov:
        tempPathRFProv=os.path.join(pathRF,i)
        tempPathWProv=os.path.join(pathW,i)
        tempPathRIProv=os.path.join(pathRI,i)
        if not os.path.exists(tempPathWProv):
            os.mkdir(tempPathWProv)
        cities=os.listdir(tempPathRIProv)
        for city in cities:
            tempPathRFCity=os.path.join(tempPathRFProv,city)
            tempPathRICity=os.path.join(tempPathRIProv,city)
            tempPathWCity=os.path.join(tempPathWProv,city)
            df=pd.read_excel(tempPathRFCity+'.xlsx')
            kelList=os.listdir(tempPathRICity)
            lst=[]
            for kel in kelList:
                tempPathRIKel=os.path.join(tempPathRICity,kel)
                lst.append(tempPathRIKel)
            df['Path_Segmentage_Image']=lst
            df.to_excel(tempPathWCity+'.xlsx',index=(False))
            
# makeTabelCitra('D:\\Data Star Schema\\Tabel Img', 'D:\\Data Star Schema\\Img Segmentasi', 'D:\\Data Star Schema\\Tabel Citra Seg Asli')
                
                
               