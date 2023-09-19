from django.db import models

class SegmentageImage():
    def __init__(self,h,w,luas,label,jumlah):
        self.ukuran_grid_h = h
        self.ukuran_grid_w = w
        self.luas_Per_Pixel_Km_Persegi = luas
        self.labelZona = label
        self.jumlah = jumlah

class PemanfaatanLahan():
    def __init__(self, label, pemanfaatan, luas, persentase):
        self.labelZona=label
        self.luas = luas
        self.pemanfaatanLahan=pemanfaatan
        self.persentase=persentase
        
    def tambahLuas(self,luas):
        self.luas+=luas