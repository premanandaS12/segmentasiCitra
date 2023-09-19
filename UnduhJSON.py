import requests
import json
import os
import time

def downloadByKelurahan(kelurahan,kota,provinsi,wPath='D:\\Skripsi\\Data Citra\\GeoJSON'):
    # Fungsi ini untuk download data batas wilayah kelurahan dalam format latitude dan longitude
    param={"f":"json","returnGeometry": "true" , "geometryType": "esriGeometryPolygon", "spatialRel": "esriSpatialRelIntersects", "outFields": "OBJECTID, NAMOBJ, WADMKC, WADMKD, WADMKK, WADMPR, LUASWH", "orderByFields": "OBJECTID ASC"}
    param['where']=str("WADMKD='"+kelurahan+"' AND WADMKK='"+kota+"' AND WADMPR='"+provinsi+"'")
    # print(param)
    response = requests.get("https://geoservices.big.go.id/rbi/rest/services/BATASWILAYAH/Administrasi_AR_KelDesa_10K/FeatureServer/0/query", 
                  params=param,timeout=300)
    res=response.json()
    # simpan response dari query ke dalam file
   
    with open(wPath, 'w') as f:
        json.dump(res, f, ensure_ascii=False)

rPath='D:\\Skripsi\\Data Citra\\Kelurahan'
wPath='D:\\Skripsi\\Data Citra\\GeoJSON'
prov=os.listdir(rPath)

for i in prov:
    # Baca folder dari tempat simpan file json per kelurahan
    if i=='JawaBarat':
        provinsi='Jawa Barat'
    elif i=='JawaTengah':
        provinsi='Jawa Tengah'
    elif i=='JawaTimur':
        provinsi='Jawa Timur'
    elif i=='KalimantanUtara':
        provinsi='Kalimantan Utara'
    print("Provinsi ",provinsi)
    rProv=os.path.join(rPath, i)
    wProv=os.path.join(wPath, i)
    # Liast semua kota yang ada di dalam folder provinsi 
    cities=os.listdir(rProv)
    for city in cities:
        print("Kota ",city)
        rCityPath=os.path.join(rProv, city)
        tempPath=os.path.join(wProv, city.split('.')[0])
        kota=city.split('.')[0]
        if '_' in kota:
            kota=kota.split('_')
            tempKota=kota[0]+' '+kota[1]
        else:
            tempKota=kota
        # Kalau tidak ada foldernya, buat foldernya
        if not os.path.exists(tempPath):
            os.mkdir(tempPath)
        with open(rCityPath) as file:
            kelurahan=file.read().splitlines()
        kelurahan=['Kabongan Kidul','Kabongan Lor','Kedungtulup','Karaskepoh','Lodankulon','Lodanwetan','Sambongpayak','Sumberejo']
        # Handle nama kelurahan yang aneh seperti Pa'loloan, nama kelurahan dengan garis miring
        for k in kelurahan:
            if len(k.split('.'))>2:
                Kel=k.split(".")
                tempKel=Kel[0]+"''"+Kel[1]
                tempKP=Kel[0]+" "+Kel[1]
            elif "'" in k:
                Kel=k.split("'")
                tempKel=Kel[0]+"''"+Kel[1]
                tempKP=Kel[0]+" "+Kel[1]
            elif "/" in k:
                Kel=k.split("/")
                tempKel=Kel[0]+"/"+Kel[1]
                tempKP=Kel[0]+" "+Kel[1]
            else:
                tempKP=k
                tempKel=k
            resPath=os.path.join(tempPath,tempKP)+'.json'
            print('Kelurahan ', tempKP)
            # Donwload data batas kelurahannya dan simpan dalam format json
            downloadByKelurahan(tempKel, tempKota, provinsi,resPath)
            # time.sleep(3)