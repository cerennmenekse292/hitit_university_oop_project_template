"""
Modül 1 - Kanal Yönetimi 
Base Class Tanımı 

Bu dosya, modül 1 kapsamında yer alan tüm kanal türlerinin türediği soyut(abstract)
temel sınıfı içerir
"""
from abc import ABC, abstractmethod


class KanalC(ABC):
    def __init__(self, id_c, id_sahip, baslik, tur, durum):
        self.id_c = id_c
        self.id_sahip = id_sahip
        self.baslik = baslik
        self.tur = tur       # oyun, eğitim, vlog, müzik
        self.durum = durum   # aktif, askıya_alındı, silindi, onay_bekliyor

    def ac(self):
        self.durum = "aktif"

    def durdur(self):

        self.durum = "askıya_alındı"

    def sil(self):
        self.durum = "silindi"

    def bilgileri_goster(self):
        print(f"{self.baslik} ({self.tur}) - {self.durum}")

    # ---- ABSTRACT METOTLAR ----
    @abstractmethod
    def kanal_tipi(self):
        pass

    @abstractmethod
    def ek_bilgiler(self):
        pass