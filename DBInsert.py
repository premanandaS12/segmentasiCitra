# -*- coding: utf-8 -*-
"""
Created on Thu May 18 20:18:49 2023

@author: Premananda Setyo
"""

import psycopg2
import pandas as pd
import os
import cv2
import io
import numpy as np
from PIL import Image
import concurrent.futures

query="SELECT kelurahan, labelzona, COUNT(LabelZona), ukuran_grid_h, ukuran_grid_w, Luas_Per_Pixel_Km_Persegi FROM dataSegmentasi WHERE kelurahan='Baranangsiang' AND kotakabupaten='Bandung Barat' GROUP BY LabelZona, ukuran_grid_h, ukuran_grid_w, Luas_Per_Pixel_Km_Persegi, kelurahan"


class QueryAndDb():
    def __init__(self):
        self.db_name='segmentasiCitra'
        self.username='postgres'
        self.hostname='localhost'
        self.pwd='123'
        self.port_num="5432"
        self.conn=None
        self.cur=None

    # Connect ke db
    def connect(self):
        self.conn = psycopg2.connect(
                    database=self.db_name,
                    user=self.username,
                    password=self.pwd,
                    host=self.hostname,
                    port=self.port_num
                    )
        self.cur=self.conn.cursor()

    # Close koneksi ke db
    def close(self):
        self.conn.commit()
        if self.cur!=None and self.conn!=None:
            self.cur.close()
            self.conn.close()
    
    # Fungsi untuk commit data ke db
    def commit(self):
        self.conn.commit()

    # Buat table dimensi provinsi
    def makeTableProv(self):
        self.connect()
        print(self.conn,self.cur)
        create_table_prov='''CREATE TABLE IF NOT EXISTS provinsi (
                            id_provinsi INTEGER PRIMARY KEY,
                            namaProvinsi varchar (256))'''
        self.cur.execute(create_table_prov)
        self.close()

    # Buat table dimensi kota/kab
    def makeTableKota(self):
        self.connect()
        create_table_kota='''CREATE TABLE IF NOT EXISTS kotaKabupaten (
                            id_kotaKabupaten INTEGER PRIMARY KEY,
                            namaKotaKabupaten varchar (256))'''
        self.cur.execute(create_table_kota)
        self.close()

    # Buat table dimensi kecamatan
    def makeTableKecamatan(self):
        self.connect()
        create_table_kecamatan='''CREATE TABLE IF NOT EXISTS kecamatan (
                            id_kecamatan INTEGER PRIMARY KEY,
                            namaKecamatan varchar (256))'''
        self.cur.execute(create_table_kecamatan)
        self.close()

    # Buat table dimensi kelurahan
    def makeTableKelurahan(self):
        self.connect()
        create_table_kelurahan='''CREATE TABLE IF NOT EXISTS kelurahan (
                            id_kelurahan INTEGER PRIMARY KEY,
                            namaKelurahan varchar (256))'''
        self.cur.execute(create_table_kelurahan)
        self.close()

    # Buat fact table segmentasi
    def makeTableSegmentasi(self):
        self.connect()
        create_table_segmentasi='''CREATE TABLE IF NOT EXISTS dataSegmentasi (
                    id SERIAL PRIMARY KEY,
                    id_kelurahan int REFERENCES kelurahan(id_kelurahan),
                    ukuran_h_citra_full int,
                    ukuran_w_citra_full int,
                    x_tile int,
                    y_tile int,
                    ukuran_h_citra_tile int,
                    ukuran_w_citra_tile int,
                    ukuran_grid_h int,
                    ukuran_grid_w int,
                    x_grid int,
                    y_grid int,
                    id_kecamatan int REFERENCES kecamatan(id_kecamatan),
                    id_kotaKabupaten int REFERENCES kotaKabupaten(id_kotaKabupaten),
                    id_provinsi int REFERENCES provinsi(id_provinsi),
                    luas_per_pixel_km_persegi float,
                    labelZona int)'''
        self.cur.execute(create_table_segmentasi)
        self.close()
    
    # Buat fact table image
    def makeTableImg(self):
        self.connect()
        create_table_img='''CREATE TABLE IF NOT EXISTS dataCitra (
                    id SERIAL PRIMARY KEY,
                    id_kelurahan int REFERENCES kelurahan(id_kelurahan),
                    id_kecamatan int REFERENCES kecamatan(id_kecamatan),
                    id_kotaKabupaten int REFERENCES kotaKabupaten(id_kotaKabupaten),
                    id_Provinsi int REFERENCES provinsi(id_provinsi),
                    citraKelurahan bytea,
                    citraKelurahanSegmentasi bytea)'''
        self.cur.execute(create_table_img)
        self.close()
    
    # Buat insert data kelurahan
    def insertKelurahan(self,record):
        # self.connect()
        insert_kelurahan="""INSERT INTO kelurahan (id_kelurahan, namaKelurahan) VALUES (%s, %s)"""
        self.cur.execute(insert_kelurahan,record)
        # self.close()

    # Buat insert data kecamatan
    def insertKecamatan(self,record):
        # self.connect()
        insert_kecamatan="""INSERT INTO kecamatan (id_kecamatan, namaKecamatan) VALUES (%s, %s)"""
        self.cur.execute(insert_kecamatan, record)
        # self.close()
    
    # Buat insert data kota/kabupaten
    def insertKotaKabupaten(self,record):
        # self.connect()
        insert_kota="""INSERT INTO kotaKabupaten (id_kotaKabupaten, namaKotaKabupaten) VALUES (%s, %s)"""
        self.cur.execute(insert_kota, record)
        # self.close()

    # Buat insert data provinsi
    def insertProvinsi(self,record):
        # self.connect()
        insert_provinsi="""INSERT INTO provinsi (id_provinsi, namaProvinsi) VALUES (%s, %s)"""
        self.cur.execute(insert_provinsi, record)
        # self.close()

    # Buat insert data segmentasi
    def insertSegmentageData(self, record):
        # self.connect()
        print(record)
        insert_seg_data="""INSERT INTO dataSegmentasi (id_kelurahan, ukuran_h_citra_full, ukuran_w_citra_full, x_tile, y_tile, ukuran_h_citra_tile, ukuran_w_citra_tile, ukuran_grid_h, ukuran_grid_w, x_grid, y_grid, id_kecamatan, id_kotaKabupaten, id_provinsi, luas_per_pixel_km_persegi, labelZona) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cur.execute(insert_seg_data, record)
        self.commit()
        # self.close()

    # Buat insert image ke table datacitra
    def insertImage(self, record):
        # self.connect()
        print(record)
        insert_provinsi="""INSERT INTO dataCitra (id_kelurahan, id_kecamatan, id_kotaKabupaten, id_Provinsi, citraKelurahan, citraKelurahanSegmentasi) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cur.execute(insert_provinsi, record)
        self.commit()
        # self.close()

    def dropTableSegmentasi(self):
        dropTable="""DROP TABLE dataSegmentasi"""
        self.cur.execute(dropTable)

    def search(self,query):
        self.connect()
        self.cur.execute(query)
        rows=self.cur.fetchall()
        res=[]
        for row in rows:
            print(row[0], row[1], row[2], row[3], row[4], row[5])
            # res.append(SegmentageImage(row[1], row[2], row[3], row[0], row[1]))
        self.close()
        return res
    
    def checkTable(self):
        self.connect()
        # if self.cur!=None and self.conn!=None:
        #     print('msk check table')
        print(self.cur)
        self.cur.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        for table in self.cur.fetchall():
            print(table)
        self.close()

def insertKelurahan(pathR):
    print('Kelurahan')
    df=pd.read_excel(pathR)
    qad=QueryAndDb()
    qad.connect()
    for idx, row in df.iterrows():
        record=(row['Id_Kelurahan'],row['Kelurahan'])
        qad.insertKelurahan(record)
        print(row['Kelurahan'])
    qad.close()

def insertKecamatan(pathR):
    print('Kecamatan')
    df=pd.read_excel(pathR)
    qad=QueryAndDb()
    qad.connect()
    for idx, row in df.iterrows():
        record=(row['Id_Kecamatan'],row['Kecamatan'])
        qad.insertKecamatan(record)
        print(row['Kecamatan'])
    qad.close()

def insertKota(pathR):
    print('Kota')
    df=pd.read_excel(pathR)
    qad=QueryAndDb()
    qad.connect()
    for idx, row in df.iterrows():
        record=(row['Id_KotaKabupaten'],row['KotaKabupaten'])
        qad.insertKotaKabupaten(record)
        print(row['KotaKabupaten'])
    qad.close()

def insertProvinsi(pathR):
    print('Provinsi')
    df=pd.read_excel(pathR)
    qad=QueryAndDb()
    qad.connect()
    for idx, row in df.iterrows():
        record=(row['Id_Provinsi'],row['Provinsi'])
        qad.insertProvinsi(record)
        print(row['Provinsi'])
    qad.close()

def insertSegmentageData(pathR, cities):
    status=[]
    count=0
    print('segmentage data')
    qad=QueryAndDb()
    qad.connect()
    prov=os.listdir(pathR)
    for i in prov:
        tempPathProv=os.path.join(pathR,i)
        # cities=os.listdir(tempPathProv)
        cities=[cities]
        for city in cities:
            tempPathCity=os.path.join(tempPathProv,city)
            kelList=os.listdir(tempPathCity)
            for kel in kelList:
                tempPathKel=os.path.join(tempPathCity,kel)
                tiles=os.listdir(tempPathKel)
                for tile in tiles:
                    tempPathFile=os.path.join(tempPathKel,tile)
                    try:
                        df=pd.read_excel(tempPathFile)
                        futures=[]
                        for idx, row in df.iterrows():
                            temp=[]
                            record=(row['Id_Kelurahan'],row['Ukuran_h_citra_full'],row['Ukuran_w_citra_full'],row['x_tile'],row['y_tile'],row['Ukuran_h_citra_tile'],row['Ukuran_w_citra_tile'],row['ukuran_grid_h'],row['ukuran_grid_w'],row['x_grid'],row['y_grid'],row['Id_Kecamatan'],row['Id_KotaKabupaten'],row['Id_Provinsi'],row['Luas_Per_Pixel_Km_Persegi'],row['LabelZona'])
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                futures.append(executor.submit(qad.insertSegmentageData, record))
                            # qad.commit()
                            count+=1
                            print(count, row['Id_Kelurahan'], 'insert seg img')
                            temp.append(idx)
                            temp.append(tempPathFile)
                            temp.append(kel)
                            temp.append(city)
                            temp.append(prov)
                            status.append(temp)
                    except:
                        break
    qad.close()
    df=pd.DataFrame(data=status, column=['rowNumber', 'path', 'kel', 'kota', 'provinsi'])
    df.to_csv('D:\\Data Star Schema\\Log\\Status_{0}.csv'.format(city))

def img_to_byte_array(img):
  imgByteArr = io.BytesIO()
  img.save(imgByteArr, format=img.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def insertCitra(pathR):
    count=0
    print('insert citra')
    qad=QueryAndDb()
    qad.connect()
    prov=os.listdir(pathR)
    for i in prov:
        tempPathProv=os.path.join(pathR,i)
        cities=os.listdir(tempPathProv)
        for city in cities:
            tempPathFile=os.path.join(tempPathProv,city)
            try:
                df=pd.read_excel(tempPathFile)
                futures=[]
                for idx, row in df.iterrows():
                    imgAsliKel = img_to_byte_array(Image.open(row['Path_Image']))
                    imgSegKel = img_to_byte_array(Image.open(row['Path_Segmentage_Image']))
                    record=(row['Id_Kelurahan'],row['Id_Kecamatan'],row['Id_KotaKabupaten'],row['Id_Provinsi'], imgAsliKel, imgSegKel)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                            futures.append(executor.submit(qad.insertImage, record))
                    # qad.commit()
                    count+=1
                    print(count, row['Id_Kelurahan'], 'insert citra')
            except:
                break
    qad.close()

qad=QueryAndDb()
# qad.search(query)
# qad.makeTableProv()
# qad.makeTableKota()
# qad.makeTableKecamatan()
# qad.makeTableKelurahan()
# qad.makeTableSegmentasi()
# qad.makeTableImg()
qad.checkTable()

def main1():
    futures=[]
    qad=QueryAndDb()
    with concurrent.futures.ThreadPoolExecutor() as executor:
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Bandung_Barat'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Bekasi'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Cianjur'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Karawang'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Kota_Bandung'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Kota_Banjar'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Kota_Depok'))
            futures.append(executor.submit(insertSegmentageData, 'D:\\Data Star Schema\\Segmentage Image', 'Purwakarta'))
            # futures.append(executor.submit(insertCitra, 'D:\\Data Star Schema\\Tabel Citra Seg Asli'))
main1()
def main2():
    futures=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures.append(executor.submit(insertCitra, 'D:\\Data Star Schema\\Tabel Citra Seg Asli'))
# main2()



