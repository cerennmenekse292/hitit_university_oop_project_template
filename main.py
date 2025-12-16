from app.modules.module_1.implementations import (
    Base1SubClass1, Base1SubClass2
)

from app.modules.module_2.implementations import (
    Base2SubClass1, Base2SubClass2
)

from app.modules.module_3.implementations import (
    Base3SubClass1, Base3SubClass2
)

from app.modules.module_4.implementations import (
    Base4SubClass1, Base4SubClass2
)

def run_demo():
    print("=== PROJECT MENU ===")

    # Ogrenci 1 (Modul 1)
    base_1 = [
        Base1SubClass1("parametre1"),
        Base1SubClass2("parametre2")
    ]
    for n in base_1:
        n.method1()

    # Ogrenci 2 (Modul 2)
    base_2 = [
        Base2SubClass1("parametre3"),
        Base2SubClass2("parametre4")
    ]
    for n in base_2:
        n.method2()

        
    # Ogrenci 3 (Modul 3)
    base_3 = [
        Base3SubClass1("parametre5"),
        Base3SubClass2("parametre6")
    ]
    for p in base_3:
        p.method3()

    # Ogrenci 4 (Modul 4)
    object1 = Base4SubClass1("parametre7")
    object2 = Base4SubClass2("parametre8")
    object1.method4()
    object2.method4()

if __name__ == "__main__":
    run_demo()
   

# ---Öğrenci1 modül1: Base Class---
from abc import ABC, abstractmethod
class KanalC(ABC):
    def __init__(self,id_c, id_sahip, baslik, tur, durum):
        self.id_c = id_c
        self.id_sahip = id_sahip
        self.baslik = baslik
        self.tur = tur       #oyun, eğitim, vlog, müzik vb.
        self.durum = durum   #aktif, askıya_alındı, silindi, onay_bekliyor

    def ac(self):
        self.durum = "aktif"

    def durdur(self):
        self.durum = "askıya_alındı"   

    def bilgileri_goster(self):
        print(f"{self.baslik} ({self.tur}) - {self.durum}") 
@abstractmethod
def kanal_tipi(self):
    pass

@abstractmethod
def ek_bilgiler(self):
    pass

# --- Öğrenci1: Subclasses ---
class BireyselKanal(KanalC):
    def __init__(self, id_c, id_sahip, baslik, tur, durum, abone_sayisi, renk_temasi):
        super().__init__(id_c, id_sahip, baslik, tur, durum)   
        self.abone_sayisi = abone_sayisi
        self.renk_temasi =  renk_temasi

    def bilgileri_goster(self):
        print(f"{self.baslik} ({self.tur}) - {self.durum} - Abone: {self.abone_sayisi}")

    def abone_ekle(self,miktar):
        self.abone_sayisi += miktar

    def tema_değistir(self,yeni_renk):
        self.renk_temasi = yeni_renk           

def kanal_tipi(self):
    return "bireysel"

def ek_bilgiler(self):
    return {
        "abone_sayisi": self.abone_sayisi,
        "renk temasi": self.renk_temasi
        }

# KANAL DEPOSU (repository katmanı)

class KanalDeposu:
    def __init__(self):
        self.kanallar = {}

    def kanal_ekle(self, kanal):
        self.kanallar[kanal.id_c] = kanal

    def kanal_sil(self, kanal_id):
        if kanal_id in self.kanallar:
            self.kanallar[kanal_id].sil()

    def id_ile_bul(self, kanal_id):
        return self.kanallar.get(kanal_id)

    def tum_kanallari_getir(self):
        return list(self.kannallar.valuest())

    def duruma_gore_listele(self,durum):
        #Örn: sadece "Aktif" kanallar
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.durum == durum
        ]  
    def ture_gore_listele(self,tur):
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.tur == tur
        ]
    def kanal_tipine_göre_listele(self,tip):
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.kanal_tipi() == tip
        
            ]              
