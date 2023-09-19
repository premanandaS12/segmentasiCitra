# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:35:24 2023

@author: Dodong
"""

import cv2
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os
import pickle as pkl
import time

import pywt
from skimage.feature import graycomatrix, graycoprops
import concurrent.futures

class ModelWarna:
    def __init__(self,RGB,proporsi):
        self.RGB=RGB
        self.prop=proporsi
        
class Tile:
    def __init__(self, namaKelurahan, wTile, hTile, x, y,img):
      self.namaKelurahan=namaKelurahan
      self.wTile=wTile
      self.hTile=hTile
      self.x=x
      self.y=y
      self.img=img
        

class Wrapper:
    def __init__(self):
        self.pathImg=''
        self.dfHSV=[]
        self.tiles=[]
        self.k=0
        self.ukuranTile=0
        self.i=0
        self.kelurahan=''
        self.temp=[]
        self.df_data_akhir=[]
        self.model=object
        
    def setAwal(self):
        self.dfHSV=[]
        self.tiles=[]
        self.i=0
        self.temp=[]
        self.df_data_akhir=[]
        
    def toDfWarna(self,arrProp,kelurahan,x,y,ukuranTile,maximum,minimum,stdev,texture):
        print('tdfa', self.tiles[self.i].namaKelurahan)
        tempDf=[]
        tempDf.append(kelurahan)
        tempDf.append(x)
        tempDf.append(y)
        tempDf.append(ukuranTile)
        for i in arrProp:
            tempDf.append(i.RGB[0])
            tempDf.append(i.RGB[1])
            tempDf.append(i.RGB[2])
            tempDf.append(i.prop)
        tempDf.append(stdev)
        for z in minimum:
            tempDf.append(z)
        for z in maximum:
            tempDf.append(z)
        for j in range(len(texture)):
            for k in range (len(texture[0])):
                for l in range(len(texture[0][0])):
                    tempDf.append(texture[j][k][l])
        self.temp=tempDf
        self.temp=self.temp[4:]
        self.dfHSV.append(tempDf)
        # print('HSV',self.dfHSV)
    
    def toDfDataAkhir(self,label,xTile,yTile,kecamatan,kota,provinsi,luas,nama_file,idKel):
        tempAkhir=[]
        tempAkhir.append(idKel)
        tempAkhir.append(self.tiles[self.i].namaKelurahan.split('_')[0])
        tempAkhir.append(256)
        tempAkhir.append(256)
        tempAkhir.append(xTile)
        tempAkhir.append(yTile)
        tempAkhir.append(self.tiles[self.i].hTile)
        tempAkhir.append(self.tiles[self.i].wTile)
        tempAkhir.append(self.tiles[self.i].x)
        tempAkhir.append(self.tiles[self.i].y)
        tempAkhir.append(kecamatan)
        tempAkhir.append(kota)
        tempAkhir.append(provinsi)
        tempAkhir.append(luas)
        tempAkhir.append(nama_file)
        tempAkhir.append(label)
        self.df_data_akhir.append(tempAkhir)
        # print('data akhir',self.df_data_akhir)
        self.temp=[]
        
    def buatGrid(self,img,ukuranTile):
        for i in range(0,256,ukuranTile):
          for j in range(0,256,ukuranTile):
            newTile = img[i : (i+ukuranTile), j : (j+ukuranTile) , :]
            print('UkuranTile',newTile.shape)
            tl=Tile(self.kelurahan, ukuranTile, ukuranTile, j//ukuranTile, i//ukuranTile, newTile)
            self.tiles.append(tl)
            
    def writeDfFiturRF(self,pathW):
        print('HSV',self.dfHSV)
        df2=pd.DataFrame(data=self.dfHSV,columns=['NamaKelurahan','x','y','UkuranTile','H1','S1','V1', 'Proporsi1','H2','S2','V2','Proporsi2','H3','S3','V3','Proporsi3','stdev','min_H',
                                                            'min_S','min_V','max_H','max_S','max_V',
                                                            'dissimilarity_0_LL','correlation_0_LL','homogeneity_0_LL','contrast_0_LL','energy_0_LL',
                                                            'dissimilarity_45_LL','correlation_45_LL','homogeneity_45_LL','contrast_45_LL','energy_45_LL',
                                                            'dissimilarity_90_LL','correlation_90_LL','homogeneity_90_LL','contrast_90_LL','energy_90_LL',
                                                            'dissimilarity_135_LL','correlation_135_LL','homogeneity_135_LL','contrast_135_LL','energy_135_LL',
                                                            'dissimilarity_180_LL','correlation_180_LL','homogeneity_180_LL','contrast_180_LL','energy_180_LL',
                                                            'dissimilarity_0_LH','correlation_0_LH','homogeneity_0_LH','contrast_0_LH','energy_0_LH',
                                                            'dissimilarity_45_LH','correlation_45_LH','homogeneity_45_LH','contrast_45_LH','energy_45_LH',
                                                            'dissimilarity_90_LH','correlation_90_LH','homogeneity_90_LH','contrast_90_LH','energy_90_LH',
                                                            'dissimilarity_135_LH','correlation_135_LH','homogeneity_135_LH','contrast_135_LH','energy_135_LH',
                                                            'dissimilarity_180_LH','correlation_180_LH','homogeneity_180_LH','contrast_180_LH','energy_180_LH',
                                                            'dissimilarity_0_HL','correlation_0_HL','homogeneity_0_HL','contrast_0_HL','energy_0_HL',
                                                            'dissimilarity_45_HL','correlation_45_HL','homogeneity_45_HL','contrast_45_HL','energy_45_HL',
                                                            'dissimilarity_90_HL','correlation_90_HL','homogeneity_90_HL','contrast_90_HL','energy_90_HL',
                                                            'dissimilarity_135_HL','correlation_135_HL','homogeneity_135_HL','contrast_135_HL','energy_135_HL',
                                                            'dissimilarity_180_HL','correlation_180_HL','homogeneity_180_HL','contrast_180_HL','energy_180_HL',
                                                            'dissimilarity_0_HH','correlation_0_HH','homogeneity_0_HH','contrast_0_HH','energy_0_HH',
                                                            'dissimilarity_45_HH','correlation_45_HH','homogeneity_45_HH','contrast_45_HH','energy_45_HH',
                                                            'dissimilarity_90_HH','correlation_90_HH','homogeneity_90_HH','contrast_90_HH','energy_90_HH',
                                                            'dissimilarity_135_HH','correlation_135_HH','homogeneity_135_HH','contrast_135_HH','energy_135_HH',
                                                            'dissimilarity_180_HH','correlation_180_HH','homogeneity_180_HH','contrast_180_HH','energy_180_HH'])
        # namaFileHSV=os.path.join(pathW, self.kelurahan)+'HSV.xlsx'
        df2.to_excel(pathW+'.xlsx')
        print(pathW)
    
    def writeDFDataAkhir(self,pathW):
        print('DFDataAkhir',self.df_data_akhir)
        df_res=pd.DataFrame(data=self.df_data_akhir,columns=['Id_Kelurahan','Kelurahan', 'Ukuran_h', 'Ukuran_w', 'x_tile','y_tile', 'ukuran_grid_h','ukuran_grid_w','x_grid','y_grid','Kecamatan','KotaKabupaten','Provinsi', 'Luas_Per_Pixel_Km_Persegi','Nama_File_Tile_Citra',
                                                            'LabelZona'])
        # namaFileRes=os.path.join(pathW, self.kelurahan)+'.csv'
        df_res.to_excel(pathW+'.xlsx')
        print(pathW)
        
    def setK(self,k):
        self.k=k
    
    def setUkuranGrid(self,ukuranGrid):
        self.ukuranTile=ukuranGrid
        
    def readImgToGrid(self):
        s1=self.pathImg.split('\\')[-1]
        s2=s1.split('.')[0]
        print('rig', s1,s2)
        # time.sleep(5)
        self.kelurahan=s2
        img=cv2.imread(self.pathImg)
        self.buatGrid(img,self.ukuranTile)
        
    
    def predictLabel(self,feature,first,kota=False):
        fitur=[]
        fitur.append(feature)
        if first==True:
            self.model=pkl.load(open('D:\\Skripsi\\DownloadGambar\\CitraNew\\Model\\rf_kab.pkl','rb'))
        elif first==True and kota==True:
            rf_model_kota=pkl.load(open('rf_kota.pkl','rb'))
        if kota==False:
            return self.model.predict(fitur)
        else:
            return rf_model_kota.predict(feature)
    
    def buatFiturPredict(self):
        process2=Process()
        futures=[]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures.append(executor.submit(process2.getMaxHSV, self.tiles[self.i]))
            futures.append(executor.submit(process2.getMinHSV, self.tiles[self.i]))
            futures.append(executor.submit(process2.getStDevHSV, self.tiles[self.i]))
            futures.append(executor.submit(process2.getdwt2d, self.tiles[self.i]))
            futures.append(executor.submit(process2.proporsiHSV, self.tiles[self.i], self.k))
            
            maximumHSV=futures[0].result()
            minimumHSV=futures[1].result()
            stdevHSV=futures[2].result()
            LL, LH, HL, HH =futures[3].result()
            propWarnaHSV=futures[4].result()
        
        tempTexture=[LL,LH,HL,HH]
        textureRes=[]
        for i in tempTexture:
            textureRes.append(process2.getGLCM(i))
        print('len texture ', len(textureRes))
        self.toDfWarna(propWarnaHSV, self.kelurahan, self.tiles[self.i].x, self.tiles[self.i].y, self.tiles[self.i].wTile, maximumHSV, minimumHSV, stdevHSV, textureRes)
        
    def checker(self, pathRes, pathRead):
        resData=os.listdir(pathRes)
        tiles=os.listdir(pathRead)
        resData_new=set([x.split('.')[0]+'.png' for x in resData])
        tiles_new=set(tiles)
        res=list(tiles_new.difference(resData_new))
        return res
    
    def run(self,pathRM,pathRT,pathWFitur,PathWRes):
        provinces=os.listdir(pathRT)
        provinces=['JawaBarat']
        for prov in provinces:
            tempPathRTProv=os.path.join(pathRT,prov)
            tempPathRMProv=os.path.join(pathRM,prov)
            tempPathWFiturProv=os.path.join(pathWFitur,prov)
            tempPathWResProv=os.path.join(PathWRes,prov)
            if not os.path.exists(tempPathWFiturProv):
                os.mkdir(tempPathWFiturProv)
            if not os.path.exists(tempPathWResProv):
                os.mkdir(tempPathWResProv)
            cities=os.listdir(tempPathRTProv)
            cities=['Bekasi']
            for city in cities:
                if not 'Kota' in city:
                    tempPathRTCity=os.path.join(tempPathRTProv,city)
                    tempPathRMCity=os.path.join(tempPathRMProv,city)
                    tempPathWFiturCity=os.path.join(tempPathWFiturProv,city)
                    tempPathWResCity=os.path.join(tempPathWResProv,city)
                    if not os.path.exists(tempPathWFiturCity):
                        os.mkdir(tempPathWFiturCity)
                    if not os.path.exists(tempPathWResCity):
                        os.mkdir(tempPathWResCity)
                    kelList=os.listdir(tempPathRTCity)
                    df_metadata=pd.read_excel(tempPathRMCity+'.xlsx')
                    kelList=['Jayabakti']
                    for kel in kelList:
                        self.setAwal()
                        tempPathRTKel=os.path.join(tempPathRTCity,kel)
                        tempPathWFiturKel=os.path.join(tempPathWFiturCity,kel)
                        tempPathWResKel=os.path.join(tempPathWResCity,kel)
                        # tilesKel=os.listdir(tempPathRTKel)
                        if not os.path.exists(tempPathWFiturKel):
                            os.mkdir(tempPathWFiturKel)
                        if not os.path.exists(tempPathWResKel):
                            os.mkdir(tempPathWResKel)
                        tilesKel=self.checker(tempPathWResKel, tempPathRTKel)
                        print(tilesKel)
                        # time.sleep(10)
                        for tileKel in tilesKel:
                            tempPathWFiturTile=os.path.join(tempPathWFiturKel,tileKel.split('.')[0])
                            tempPathWResTile=os.path.join(tempPathWResKel,tileKel.split('.')[0])
                            self.i=0
                            metaTile=df_metadata.loc[df_metadata['Nama_File_Tile_Citra'] == tileKel]
                            tempPathRTTile=os.path.join(tempPathRTKel,tileKel)
                            print(tempPathRTTile)
                            print(metaTile.iloc[0]['Nama_File_Tile_Citra'])
                            # time.sleep(5)
                            self.pathImg=tempPathRTTile
                            self.setUkuranGrid(4)
                            self.setK(5)
                            self.tiles=[]
                            self.dfHSV=[]
                            self.df_data_akhir=[]
                            self.readImgToGrid()
                            for i in range(len(self.tiles)):
                                print(metaTile.iloc[0]['Nama_File_Tile_Citra'])
                                print(kel, i)
                                if i==0:
                                    first=True
                                else:
                                    first=False
                                self.buatFiturPredict()
                                label=self.predictLabel(self.temp, first)
                                self.toDfDataAkhir(label[0], metaTile.iloc[0]['x'], metaTile.iloc[0]['y'], metaTile.iloc[0]['Kecamatan'], metaTile.iloc[0]['KotaKabupaten'], metaTile.iloc[0]['Provinsi'], metaTile.iloc[0]['Luas_Per_Pixel_Km_Persegi'], metaTile.iloc[0]['Nama_File_Tile_Citra'], metaTile.iloc[0]['Id_Kelurahan'])
                                self.i+=1
                                
                            self.writeDfFiturRF(tempPathWFiturTile)
                            self.writeDFDataAkhir(tempPathWResTile)        
                            
                            
                            
                    

class Process:
    def __init__(self):
        self.jumlahPx=0
        self.dictLabelCount={}
        self.centroid=[]
        self.label=[]
        self.proporsi=[]
        self.bgLabel=None

    # Fungsi untuk mengecek apakah terdapat bg hitam pada gambar
    def check_bg_lbl(self):
        for i in range(len(self.centroid)):
            if self.centroid [i][0]==0 and self.centroid [i][1]==0 and self.centroid [i][2]==0:
                self.bgLabel=self.label[i]
        
    # Fungsi untuk menghitung jumlah anggota pada setiap cluster
    def getAnggota(self):
        lblAnggota=np.array(self.label)
        label, counts = np.unique(lblAnggota, return_counts=True)
        label_dict=dict(zip(label,counts))
        totalJumlahPx=0
        for i in label_dict.values():
            totalJumlahPx+=i
        self.dictLabelCount=label_dict
        self.jumlahPx=totalJumlahPx
    
    # Jika terdapat bg hitam pada gambar, hitung jumlah foreground dikurangi dengan jumlah anggota bg hitam
    def px_update_fg(self):
        self.jumlahPx=self.jumlahPx-self.dictLabelCount[self.bgLabel]
    
    # Fungsi untuk menghitung jumlah persentase warna dari setiap anggota cluster
    def getProporsi(self):
        keys=self.dictLabelCount.keys()
        for i in keys:
            warna=ModelWarna(self.centroid[i],format(self.dictLabelCount[i]/self.jumlahPx*100,'.2f'))
            self.proporsi.append(warna)
            
    # Fungsi untuk sorting centroid dengan persentase diurutkan dari yang terbesar
    def sort_prop(self):
        self.dictLabelCount = dict(sorted(self.dictLabelCount.items(), key=lambda x:x[1], reverse=True)) 
            
    # Fungsi untuk buang centroid dan persentase bg hitam dari dict
    def update_dict(self):
        del self.dictLabelCount[self.bgLabel]
      
    #  Fungsi untuk mengembalikan 3 centroid warna dengan 3 persentase terbesar. Jika centroid hasil cluster
    #  kurang dari 3, lakukan copy persentase dan centroid sehingga dapat mengembalikan 3 centroid beserta dengan proporsinya.
    def tigaProporsiTerbesar(self):
        res=[]
        try:
            for i in range(3):
                res.append(self.proporsi[i])
            if len(res)>3:
                for i in range(3):
                    res[i]=res[i]
        except:
            if len(self.proporsi)<3 and len(self.proporsi)!=0:
                for i in range(len(self.proporsi)):
                    res.append(self.proporsi[i])
                if len(res)<3:
                    for i in range(3-len(res)):
                        res.append(self.proporsi[0])
                if len(res)>3:
                    for i in range(len(res)-3):
                        del res[-1]
        return res
    
    #  Fungsi untuk clustering dengan model warna HSV dan mengembalikan 3 warna dominan beserta dengan persentasenya
    def proporsiHSV(self,tile,k):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        img = img.reshape((-1, 3))
        model=KMeans(n_clusters=k,random_state=(1)).fit(img)
        centroid=model.cluster_centers_
        self.centroid = np.uint8(centroid)
        self.label=model.labels_
        
        self.getAnggota()
        self.check_bg_lbl()
        if self.bgLabel!=None:
            self.px_update_fg()
            self.update_dict()
            
        self.sort_prop()
        self.getProporsi()
        
        return self.tigaProporsiTerbesar()
    
    # Fungsi untuk melakukan transformasi dwt2d pada data grid citra
    def getdwt2d(self,tileGr):
        imgGrey=cv2.cvtColor(tileGr.img, cv2.COLOR_BGR2GRAY)
        coeffs=pywt.dwt2(imgGrey,'haar')
        LL=np.uint8(coeffs[0])
        (LH,HL,HH)=np.uint8(coeffs[-1])

        return LL, LH, HL, HH

    # Fungsi untuk menghitung GLCM
    def getGLCM(self,transform):
        dists=[1]
        angle=[0, np.pi/4, np.pi/2, 3*np.pi/4,np.pi]
        lvl=256
        sym=True
        norm=True
        res=[]
        for a in angle:
            temp=[]
            glcm = graycomatrix(transform, 
                               distances=dists, 
                               angles=[a], 
                               levels=lvl,
                               symmetric=sym, 
                               normed=norm)
            temp.append(graycoprops(glcm, 'dissimilarity')[0, 0])
            temp.append(graycoprops(glcm, 'correlation')[0, 0])
            temp.append(graycoprops(glcm, 'homogeneity')[0, 0])
            temp.append(graycoprops(glcm, 'contrast')[0, 0])
            temp.append(graycoprops(glcm, 'energy')[0, 0])
            res.append(temp)
        return res
    
    # Fungsi untuk mencari nilai minimum nilai HSV pixel dalam grid   
    def getMinHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        minimum=np.amin(img,axis=(0,1))
        return minimum
    
    # Fungsi untuk mencari nilai minimum nilai RGB pixel dalam grid  
    def getMaxHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        maximum=np.amax(img,axis=(0,1))
        return maximum
    
    # Fungsi untuk mencari nilai stdev dari grid data citra
    def getStDevHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        stdev=np.std(img)
        return stdev
    
wr=Wrapper()
wr.run('D:\\Skripsi\\DownloadGambar\\CitraNew\\Metadata','D:\\Skripsi\\DownloadGambar\\CitraNew\\Tile','D:\\Skripsi\\DownloadGambar\\CitraNew\\Warna','D:\\Skripsi\\DownloadGambar\\CitraNew\\DataAkhir')