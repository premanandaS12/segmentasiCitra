# segmentasiCitra

Aplikasi percobaan ini ditujukan untuk pemetaan pemanfaatan lahan di wilayah kelurahan dan juga perhitungan luas pemanfaatan lahan di kelurahan berdasarkan tipenya.


Segmentasi Citra Pemanfaatan Lahan di Kelurahan 

Panduan program LMS
Version Python
-Python 3.10.5


Version Library
Django                 4.2.1
djangorestframework    3.13.1
numpy                  1.23.0
opencv-python          4.6.0.66
Pillow                 9.3.0
scikit-image           0.19.3
scikit-learn           1.1.1
virtualenv             20.17.1
virtualenvwrapper-win  1.2.7
psycopg2               2.9.6
PyWavelets             1.4.1

Panduan Penggunaan Software
1. Jalankan Kode donwloadGeoJSON.py (Untuk download koordinat batas wilayah kelurahan dalam file JSON, dimana file berisi latitude dan longitudenya)
2. Jalankan All.py (Untuk download gambar dan ubah file citra ke dalam tile-tile ukuran 256x256 pixel)
3. Jalankan ProgramLabelingFinal.py untuk proses melabeli data train
4. Jalankan kode buatMetaData.py untuk membuat file metadata kelurahan (dibutuhkan untuk perhitungan luas)
5. Jika sudah, selesai melabeli data citra, jalankan kode makeSegmentationData.py untuk diumpankan ke algoritma klasifikasi untuk segmentasi
6. Jalankan kode tuningRF.py, lakukan tuning parameter sampai dengan mendapatkan hasil akurasi model terbaik. Catat hyperparameter dengan hasil terbaiknmya, kemudian simpan modelnya dalam bentuk pickle.
7. Jalankan kode makeAnalisisData.py untuk segmentasi pemanfaatan lahan di wilayah kelurahan
8. Jalankan kode bikinHasilSegmentasi.py untuk menggambar hasil segmentasi pemanfaatan lahan di wilayah kelurahan. Fungsi ini dijalankan untuk mendapatkan hasil pemetaan pemanfaatan lahan di wilayah kelurahan.
9. Jika semua file yang dibutuhkan sudah siap (hasil pemetaan, luas per grid dari metadata sudah tersedia, data pemanfaatan lahan tiap grid tersedia), masukkan seluruh hasilnya ke dalam data warehouse
   untuk ditambilkan di web. Untuk memasukkannya, cukup jalankan program DBInsert.py.
10. Untuk melihat tampilan analisis di web, buka cmd dan copy kan sintaks sebagai berikut:
	--Buka directory virtual env tempat web dijalankan, cari file activate.bat nya (dalam kasus ini misalkan ada di directory D:\SkripsiUI	\segmentasiCitra\Scripts\activate.bat, sedangkan file yang dijalankan ada di dir cd D:\SkripsiUI\segmentasiCitra\project\segmentasiCitra--

	D:
	cd D:\SkripsiUI\segmentasiCitra\project\segmentasiCitra
	D:\SkripsiUI\segmentasiCitra\Scripts\activate.bat
	python manage.py runserver
	http://127.0.0.1:8000/
	
11. Jika pada http://127.0.0.1:8000/, web sudah muncul, maka dapat memasukkan query pencarian tingkat wilayah yang ingin dianalisis pemanfaatan lahannya pada halaman general monitoring.
    Sedangkan pada halaman detail monitoring, pengguna dapat melihat citra hasil pemetaan berdasarkan analisis pemanfaatan lahannya berdasarkan nama wilayah kelurahan yang dicari.
