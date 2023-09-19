# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 13:46:59 2022

@author: Dodong
"""

# global iVal,kVal,gridVal
iVal=0
kVal=5
gridVal=4

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from sklearn.cluster import KMeans
import pandas as pd
from functools import partial
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
import matplotlib.patches as patches
 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

####### Model & Backend ####### 

import cv2
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

import pywt
from skimage.feature import graycomatrix, graycoprops

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
    def __init__(self,pathImg):
        self.pathImg=pathImg
        self.dfRGB=[]
        self.dfHSV=[]
        self.tiles=[]
        self.k=0
        self.ukuranTile=0
        self.i=0
        self.kelurahan=''
        self.temp=[]
        self.df=pd.DataFrame()
        
    def toDf(self,arrProp,labelZona,tipeModelWarna,kelurahan,x,y,ukuranTile,maximum,minimum,stdev,texture):
        tempDf=[]
        if tipeModelWarna=='RGB':
            tempDf.append(self.kelurahan)
            tempDf.append(x)
            tempDf.append(y)
            tempDf.append(ukuranTile)
            print('len tempDF smp ukuran tile',len(tempDf))
            print('len arrProp', len(arrProp))
            for i in arrProp:
                tempDf.append(i.RGB[0])
                tempDf.append(i.RGB[1])
                tempDf.append(i.RGB[2])
                tempDf.append(i.prop)

                # print(i.RGB[0])
                # print(i.RGB[1])
                # print(i.RGB[2])

            print('len tempDF smp ukuran warna',len(tempDf))
            tempDf.append(stdev)
            for z in minimum:
                tempDf.append(z)
            print('len tempDF smp min warna',len(tempDf))
            for z in maximum:
                tempDf.append(z)
            print('len tempDF smp max warna',len(tempDf))
            for j in range(len(texture)):
                for k in range (len(texture[0])):
                    for l in range(len(texture[0][0])):
                        tempDf.append(texture[j][k][l])
            tempDf.append(labelZona)
            self.dfRGB.append(tempDf)
            print(tempDf)
            
        elif tipeModelWarna=='HSV':
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
            tempDf.append(labelZona)
            self.dfHSV.append(tempDf)
        
    def buatTile(self,img,ukuranTile):
        for i in range(0,256,ukuranTile):
          for j in range(0,256,ukuranTile):
            newTile = img[i : (i+ukuranTile), j : (j+ukuranTile) , :]
            print('UkuranTile',newTile.shape)
            tl=Tile(self.kelurahan, ukuranTile, ukuranTile, j//ukuranTile, i//ukuranTile, newTile)
            self.tiles.append(tl)
            
    def writeDf(self,pathW='D:\\Skripsi\\LabelingProgram\\label'):
        df1=pd.DataFrame(data=self.dfRGB,columns=['NamaKelurahan','x','y','UkuranTile','R1','G1','B1', 'Proporsi1','R2','G2','B2','Proporsi2','R3','G3','B3','Proporsi3','stdev','min_R',
                                                            'min_G','min_B','max_R','max_G','max_B',
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
                                                            'dissimilarity_180_HH','correlation_180_HH','homogeneity_180_HH','contrast_180_HH','energy_180_HH',
                                                            'LabelZona'])
        namaFileRGB=os.path.join(pathW, self.kelurahan)+'RGB.xlsx'
        df1.to_excel(namaFileRGB)
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
                                                            'dissimilarity_180_HH','correlation_180_HH','homogeneity_180_HH','contrast_180_HH','energy_180_HH',
                                                            'LabelZona'])
        namaFileHSV=os.path.join(pathW, self.kelurahan)+'HSV.xlsx'
        df2.to_excel(namaFileHSV)
        print(namaFileRGB)
        print(namaFileHSV)
        
    def setK(self,k):
        self.k=k
    
    def setUkuranTile(self,ukuranTile):
        self.ukuranTile=ukuranTile
        
    def getProgress(self):
        progr='{0} of {1} grid'.format(self.i,len(self.tiles))
        return progr
        
    def setLabel(self,labelZona):
        process2=Process()
        maximumRGB=process2.getMaxRGB(self.tiles[self.i])
        minimumRGB=process2.getMinRGB(self.tiles[self.i])
        stdevRGB=process2.getStDevRGB(self.tiles[self.i])
        maximumHSV=process2.getMaxHSV(self.tiles[self.i])
        minimumHSV=process2.getMinHSV(self.tiles[self.i])
        stdevHSV=process2.getStDevHSV(self.tiles[self.i])
        LL,LH,HL,HH=process2.getdwt2d(self.tiles[self.i])
        
        print('LL: ',LL)
        print('LH: ',LH)
        print('HL: ',HL)
        print('HH: ',HH)
        
        tempTexture=[LL,LH,HL,HH]
        textureRes=[]
        for i in tempTexture:
            # temp=[]
            # temp.append(process2.getGLCM(i))
            textureRes.append(process2.getGLCM(i))
        # print('texture',textureRes)
        print('len texture ', len(textureRes))
        
        self.toDf(self.temp, labelZona,'RGB', self.kelurahan, self.tiles[self.i].x, self.tiles[self.i].y, self.tiles[self.i].wTile, maximumRGB, minimumRGB, stdevRGB, textureRes)
        propWarnaHSV=process2.proporsiHSV(self.tiles[self.i], self.k)
        self.toDf(propWarnaHSV, labelZona,'HSV', self.kelurahan, self.tiles[self.i].x, self.tiles[self.i].y, self.tiles[self.i].wTile, maximumHSV, minimumHSV, stdevHSV, textureRes)
        
    def getWarna(self):
        process1=Process()
        self.temp=process1.proporsiRGB(self.tiles[self.i], self.k)
        warna=[]
        persentase=[]
        for z in self.temp:
            warna.append(z.RGB)
            persentase.append(z.prop)
        return warna,persentase
        
    def readImgToTile(self):
        s1=self.pathImg.split('\\')[-1]
        s2=s1.split('.')[0]
        self.kelurahan=s2
        img=cv2.imread(self.pathImg)
        # self.ukuranTile=ukuranTile
        self.buatTile(img,self.ukuranTile)
        
    def run0(self):
        if self.i==0:
            self.readImgToTile()
            warna,persentase = self.getWarna()
        return warna,persentase
    
    def runLabel(self,label):
        if self.i<len(self.tiles):
            if label>=0:
                self.setLabel(label)
                self.i+=1
            elif label==-1:
                del self.dfRGB[-1]
                del self.dfHSV[-1]
                self.i-=1
                
    def getGambar(self):
        return self.tiles[self.i].img
    
    def drawRect(self):
        # fig, ax = plt.subplots(frameon=False)
        # fig.set_size_inches(256,256)
        
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)
        
        # ax.imshow(cv2.imread(self.pathImg), aspect='auto')
        
        # rect = patches.Rectangle((self.tiles[self.i].x, self.tiles[self.i].y), self.tiles[self.i].wTile, self.tiles[self.i].wTile, linewidth=1, edgecolor='r', facecolor='none')
        # ax.add_patch(rect)
        # ax.set_axis_off()
        
        
        fig, ax = plt.subplots(frameon=False)
        # ax.plot([0., 0., 1., 1.])
        
        # Display the image
        ax.imshow(cv2.cvtColor(cv2.imread(self.pathImg),cv2.COLOR_BGR2RGB),aspect='auto')
        
        # Create a Rectangle patch
        x=self.tiles[self.i].x*self.tiles[self.i].wTile
        y=self.tiles[self.i].y*self.tiles[self.i].wTile
        rect = patches.Rectangle((x, y), self.tiles[self.i].wTile, self.tiles[self.i].wTile, linewidth=1, edgecolor='r', facecolor='none')
        
        # Add the patch to the Axes
        ax.add_patch(rect)
        ax.set_axis_off()
        
        return fig
    

class Process:
    def __init__(self):
        self.jumlahPx=0
        self.dictLabelCount={}
        self.centroid=[]
        self.label=[]
        self.proporsi=[]
        self.bgLabel=None

    def check_bg_lbl(self):
        for i in range(len(self.centroid)):
            if self.centroid [i][0]==0 and self.centroid [i][1]==0 and self.centroid [i][2]==0:
                self.bgLabel=self.label[i]
            
    def getAnggota(self):
        lblAnggota=np.array(self.label)
        label, counts = np.unique(lblAnggota, return_counts=True)
        label_dict=dict(zip(label,counts))
        totalJumlahPx=0
        for i in label_dict.values():
            totalJumlahPx+=i
        self.dictLabelCount=label_dict
        self.jumlahPx=totalJumlahPx

        # print(self.jumlahPx)
        # print(self.dictLabelCount)
        # print(self.centroid)

    def px_update_fg(self):
        self.jumlahPx=self.jumlahPx-self.dictLabelCount[self.bgLabel]
    
    def getProporsi(self):
        keys=self.dictLabelCount.keys()
        for i in keys:
            warna=ModelWarna(self.centroid[i],format(self.dictLabelCount[i]/self.jumlahPx*100,'.2f'))
            self.proporsi.append(warna)
            
    def sort_prop(self):
        self.dictLabelCount = dict(sorted(self.dictLabelCount.items(), key=lambda x:x[1], reverse=True)) 
            
    def update_dict(self):
        del self.dictLabelCount[self.bgLabel]
        
    def tigaProporsiTerbesar(self):
        res=[]
        try:
            for i in range(3):
                res.append(self.proporsi[i])
            if len(res)>3:
                for i in range(3):
                    res[i]=res[i]
                    print('msk try if')
                # print('prop warna',self.proporsi)
        except:
            if len(self.proporsi)<3 and len(self.proporsi)!=0:
                for i in range(len(self.proporsi)):
                    res.append(self.proporsi[i])
                if len(res)<3:
                    for i in range(3-len(res)):
                        res.append(self.proporsi[0])
                    print('msk catch if')
                if len(res)>3:
                    for i in range(len(res)-3):
                        del res[-1]
                    print('prop warna',self.proporsi)
                    print('msk catch if if')
        print('pjg res di 3 prop terbesar ',len(self.proporsi))
        return res
    
    def proporsiRGB(self,tile,k):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2RGB)
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
    
    def getdwt2d(self,tileGr):
        imgGrey=cv2.cvtColor(tileGr.img, cv2.COLOR_BGR2GRAY)
        coeffs=pywt.dwt2(imgGrey,'haar')
        LL=np.uint8(coeffs[0])
        (LH,HL,HH)=np.uint8(coeffs[-1])

        return LL, LH, HL, HH

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
        # print('res_texture: ', res)
        return res
            
    def getMinRGB(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2RGB)
        minimum=np.amin(img,axis=(0,1))
        return minimum

    def getMaxRGB(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2RGB)
        maximum=np.amax(img,axis=(0,1))
        return maximum

    def getStDevRGB(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2RGB)
        stdev=np.std(img)
        return stdev

    def getMinHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        minimum=np.amin(img,axis=(0,1))
        return minimum
    
    def getMaxHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        maximum=np.amax(img,axis=(0,1))
        return maximum
    
    def getStDevHSV(self,tile):
        img=cv2.cvtColor(tile.img,cv2.COLOR_BGR2HSV)
        stdev=np.std(img)
        return stdev


####### UI ####### 

wr=object()    

def runPertama():
    imgPath=selectFile()
    
    global wr
    wr=Wrapper(imgPath)
    
    wr.setK(kVal)
    wr.setUkuranTile(gridVal)
    warna,persentase=wr.run0()
    updateTileImg(wr.getGambar())
        
    temp=[]
    for i in warna:
        tupple=(i[0],i[1],i[2])
        temp.append(tupple)
    updateWarna(temp[0], temp[1], temp[2])
    updatePropWarna(persentase[0],persentase[1],persentase[2])
    
    progrVal.set(wr.getProgress())
    showimage(wr.drawRect())
    
def runSelanjutnya(label):
    wr.runLabel(label)
    warna,persentase=wr.getWarna()
    updateTileImg(wr.getGambar())
    
    temp=[]
    for i in warna:
        tupple=(i[0],i[1],i[2])
        temp.append(tupple)
    updateWarna(temp[0], temp[1], temp[2])
    updatePropWarna(persentase[0],persentase[1],persentase[2])
    
    progrVal.set(wr.getProgress())
    showimage(wr.drawRect())
    
def exportCSV():
    wr.writeDf('D:\\Skripsi\\LabelingProgram\\label')

def selectFile():
    filetypes = (
        ('All files', '*.*'),
        ('Image files','.jpg'),
        ('Image files','.png'),
        ('Text files', '*.txt')
        
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    showinfo(
        title='Selected File',
        message=filename
    )  
    print(filename)
    return filename
        
def getK(boxK):
    global kVal
    kVal=int(boxK.get())
    print(kVal)

def getGrid(boxGrid):
    global gridVal
    gridVal=int(boxGrid.get())
    print(gridVal)

def tes(k):
    print(k)
    
def showimage(fig):
    fig.savefig("drawRect.jpg")
    utama=Image.open("drawRect.jpg")
    # os.unlink("drawRect.jpg")
    utama=utama.resize((512,512))
    utama=ImageTk.PhotoImage(utama)
    
    img_utama.configure(image=utama)
    img_utama.image=utama

def updateTileImg(img):
    imgTile=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    imgTile=imgTile.resize((50,50))
    imgTile=ImageTk.PhotoImage(imgTile)
    imgTile_lbl.configure(image=imgTile)
    imgTile_lbl.image=imgTile
    
def updateWarna(c1,c2,c3):

    canvas1=Image.new('RGB', (50,50),c1)
    canvas2=Image.new('RGB', (50,50),c2)
    canvas3=Image.new('RGB', (50,50),c3)
    
    
    warna1=ImageTk.PhotoImage(canvas1)
    warna2=ImageTk.PhotoImage(canvas2)
    warna3=ImageTk.PhotoImage(canvas3)
    
    warna1_lbl.configure(image=warna1)
    warna1_lbl.image = warna1
    
    warna2_lbl.configure(image=warna2)
    warna2_lbl.image = warna2
    
    warna3_lbl.configure(image=warna3)
    warna3_lbl.image = warna3
    
    tempLabWarna1='Warna 1: {0}'.format(str(c1))
    tempLabWarna2='Warna 2: {0}'.format(str(c2))
    tempLabWarna3='Warna 3: {0}'.format(str(c3))
    warna1RGB.set(tempLabWarna1)
    warna2RGB.set(tempLabWarna2)
    warna3RGB.set(tempLabWarna3)
    
    
    
def updatePropWarna(p1,p2,p3):
    tempProp1='Proporsi 1: {0}%'.format(str(p1))
    tempProp2='Proporsi 2: {0}%'.format(str(p2))
    tempProp3='Proporsi 3: {0}%'.format(str(p3))
    proporsiWarna1.set(tempProp1)
    proporsiWarna2.set(tempProp2)
    proporsiWarna3.set(tempProp3)
    

root=Tk()
root.title("Image Labeling")
root.maxsize(1440,900)
root.configure(background='#404040')

frBot=Frame(root,height=30,bg='#181818')
frBot.pack(side='bottom',  fill='both',  padx=10,  pady=5)


frTop=Frame(root,bg='#181818')
frTop.pack(side='top',  fill='x',  padx=10,  pady=5)
frTop.columnconfigure(0, weight=1)
frTop.columnconfigure(1, weight=1)
frTop.columnconfigure(2, weight=1)
frTop.columnconfigure(3, weight=1)
frTop.columnconfigure(4, weight=1)
frTop.columnconfigure(5, weight=1)
frTop.columnconfigure(6, weight=1)


frLeft=Frame(root,bg='#404040')
frLeft.pack(side='left',  fill='y',  padx=10,  pady=5, expand=False)


frRight=Frame(root,bg='#404040')
frRight.pack( fill='y',  padx=10,  pady=5, expand=False)


utama=Image.open('D:\\Skripsi\\LabelingProgram\\Assets\\NoImage.png')
utama=utama.resize((512,512))
utama=ImageTk.PhotoImage(utama)
img_utama=Label(frLeft,image=utama)
img_utama.pack(fill='y')



# Heading Proporsi
heading1=Label(frTop,text='Proporsi 1',bg='#181818',fg='white',font=24)
heading1.grid(column=0,row=0,columnspan=2,sticky='NW',pady=5,padx=10)

warna1=Image.open('D:\\Skripsi\\LabelingProgram\\Assets\\NoImage.png')
warna1=warna1.resize((50,50))
warna1=ImageTk.PhotoImage(warna1)
warna1_lbl=Label(frTop,image=warna1)

warna1_lbl.grid(column=0,row=1,rowspan=2,sticky='W',padx=10,pady=5)

# Heading Proporsi
heading2=Label(frTop,text='Proporsi 2',bg='#181818',fg='white',font=24)
heading2.grid(column=2,row=0,columnspan=2,sticky='NW',pady=5,padx=10)

warna2=Image.open('D:\\Skripsi\\LabelingProgram\\Assets\\NoImage.png')
warna2=warna2.resize((50,50))
warna2=ImageTk.PhotoImage(warna2)
warna2_lbl=Label(frTop,image=warna2)

warna2_lbl.grid(column=2,row=1,rowspan=2,sticky='W',padx=10,pady=5)

# Heading Proporsi
heading3=Label(frTop,text='Proporsi 3',bg='#181818',fg='white',font=24)
heading3.grid(column=4,row=0,columnspan=2,sticky='NW',pady=5,padx=10)

warna3=Image.open('D:\\Skripsi\\LabelingProgram\\Assets\\NoImage.png')
warna3=warna3.resize((50,50))
warna3=ImageTk.PhotoImage(warna3)
warna3_lbl=Label(frTop,image=warna3)
warna3_lbl.grid(column=4,row=1,rowspan=2,sticky='W',padx=10,pady=5)

# Heading Proporsi
heading4=Label(frTop,text='Tile Image',bg='#181818',fg='white',font=24)
heading4.grid(column=6,row=0,columnspan=2,sticky='NW',pady=5,padx=10)

imgTile=Image.open('D:\\Skripsi\\LabelingProgram\\Assets\\NoImage.png')
imgTile=imgTile.resize((50,50))
imgTile=ImageTk.PhotoImage(imgTile)
imgTile_lbl=Label(frTop,image=imgTile)
imgTile_lbl.grid(column=6,row=1,rowspan=2,sticky='W',padx=10,pady=5)

proporsiWarna1=StringVar()
proporsiWarna2=StringVar()
proporsiWarna3=StringVar()

proporsiWarna1.set('Proporsi 1: 0.0%')
proporsiWarna2.set('Proporsi 2: 0.0%')
proporsiWarna3.set('Proporsi 3: 0.0%')

proporsiWarna1Label=Label(frTop,textvariable=proporsiWarna1,bg='#181818',fg='white',font=18)
proporsiWarna1Label.grid(column=1,row=1,sticky='W')

proporsiWarna2Label=Label(frTop,textvariable=proporsiWarna2,bg='#181818',fg='white',font=18)
proporsiWarna2Label.grid(column=3,row=1,sticky='W')

proporsiWarna3Label=Label(frTop,textvariable=proporsiWarna3,bg='#181818',fg='white',font=18)
proporsiWarna3Label.grid(column=5,row=1,sticky='W')

warna1RGB=StringVar()
warna2RGB=StringVar()
warna3RGB=StringVar()

warna1RGB.set('Warna 1: [0 0 0]')
warna2RGB.set('Warna 2: [0 0 0]')
warna3RGB.set('Warna 3: [0 0 0]')

warna1Label=Label(frTop,textvariable=warna1RGB,font=18,bg='#181818',fg='white')
warna1Label.grid(column=1,row=2,sticky='W')
warna2Label=Label(frTop,textvariable=warna2RGB,font=18,bg='#181818',fg='white')
warna2Label.grid(column=3,row=2,sticky='W')
warna3Label=Label(frTop,textvariable=warna3RGB,font=18,bg='#181818',fg='white')
warna3Label.grid(column=5,row=2,sticky='W')


btnSF=Button(frBot,text="Export",command=partial(exportCSV))
btnSF.pack(side=tk.LEFT, padx=60,pady=5)

btnSFI=Button(frBot,text="Select File",command=partial(runPertama))
btnSFI.pack(side=tk.RIGHT, padx=60,pady=5)

btn0=Button(frRight,text="0 Background", command=partial(runSelanjutnya,0), height=1, width=40)
btn0.grid(row=0, column=0)

btn1=Button(frRight,text="1 RTH", command=partial(runSelanjutnya,1),  height=1, width=40)
btn1.grid(row=1, column=0)

btn2=Button(frRight,text="2 Pertanian", command=partial(runSelanjutnya,2), height=1, width=40)
btn2.grid(row=2, column=0)

btn3=Button(frRight,text="3 Bangunan Non-Indsutrial",command=partial(runSelanjutnya,3), height=1, width=40)
btn3.grid(row=3, column=0)

btn4=Button(frRight,text="4 Bangunan Industrial",command=partial(runSelanjutnya,4), height=1, width=40)
btn4.grid(row=4, column=0)

btn5=Button(frRight,text="5 Tambak",command=partial(runSelanjutnya,5), height=1, width=40)
btn5.grid(row=5, column=0)

btn6=Button(frRight,text="6 Perairan",command=partial(runSelanjutnya,6), height=1, width=40)
btn6.grid(row=6, column=0)

btn7=Button(frRight,text="7 Transportasi",command=partial(runSelanjutnya,7), height=1, width=40)
btn7.grid(row=7, column=0)

btn7=Button(frRight,text="Back",command=partial(runSelanjutnya,-1), height=1, width=40)
btn7.grid(row=8, column=0)


k_label=Label(frRight, text= "Enter k- Value: ", bg='#404040',fg='white',font=18)
k_label.grid(row=0, column=1, padx=5,sticky='W')

k_val=StringVar()
boxK=Entry(frRight,textvariable=k_val)
boxK.grid(row=1, column=1, padx=5,sticky='W')

btnSubK=Button(frRight,text="Submit",command=partial(getK,boxK), height=1, width=17)
btnSubK.grid(row=2, column=1,padx=5,sticky='W')

grid_lbl=Label(frRight, text= "Enter Grid Size: ",bg='#404040',fg='white',font=18)
grid_lbl.grid(row=3, column=1, padx=5,sticky='W')

grid_val=StringVar()
boxGrid=Entry(frRight,textvariable=grid_val)
boxGrid.grid(row=4, column=1, padx=5,sticky='W')

btnSubGrid=Button(frRight,text="Submit",command=partial(getGrid,boxGrid), height=1, width=17)
btnSubGrid.grid(row=5, column=1,padx=5,sticky='W')

# Heading progress
txt_progr=Label(frRight,text='Progress: ',bg='#404040',fg='white',font=18)
txt_progr.grid(row=6,column=1,sticky='W')

progrVal=StringVar()
progrVal.set('0 of 0 grid')

progr_label=Label(frRight,textvariable=progrVal,bg='#404040',fg='white',font=16)
progr_label.grid(row=7,column=1,sticky='W')

root.mainloop()
