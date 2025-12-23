"""
Kanal Yönetim Modülü – Kanal Türü Implementasyonları

Bu dosya, Kanal Yönetim Modülü kapsamında tanımlanan
soyut KanalC sınıfından türeyen somut kanal türlerini içerir.

Amaç:
- Kalıtım (inheritance) kullanımını göstermek
- Polimorfizm sayesinde kanal türüne özel davranışlar tanımlamak
- Her kanal türüne özgü ek alan ve metotları ayırmak
- Servis katmanının kanal türünden bağımsız çalışmasını sağlamak

Bu dosyada yer alan sınıflar:
- BireyselKanal
- MarkaKanali
- CocukKanali
"""

from .base import KanalC


# --- BİREYSEL KANAL ---
class BireyselKanal(KanalC):
    def __init__(
        self,
        id_c,
        id_sahip,
        baslik,
        tur,
        durum,
        abone_sayisi,
        renk_temasi,
    ):
        super().__init__(id_c, id_sahip, baslik, tur, durum)
        self.abone_sayisi = abone_sayisi
        self.renk_temasi = renk_temasi

    def kanal_tipi(self):
        return "bireysel"

    def ek_bilgiler(self):
        return {
            "abone_sayisi": self.abone_sayisi,
            "renk_temasi": self.renk_temasi,
        }

    def abone_ekle(self, miktar):
        self.abone_sayisi += miktar

    def tema_degistir(self, yeni_renk):
        self.renk_temasi = yeni_renk

    def abone_cikar(self, miktar):
        if miktar < 0:
            return
        self.abone_sayisi = max(0, self.abone_sayisi - miktar)

    def buyume_durumu(self):
        if self.abone_sayisi < 100:
            return "küçük kanal"
        elif self.abone_sayisi < 1000:
            return "orta kanal"
        else:
            return "büyük kanal"

    def tema_bilgisi(self):
        return f"Kanal teması: {self.renk_temasi}"
    


# --- MARKA KANALI ---
class MarkaKanali(KanalC):
    def __init__(self, id_c, id_sahip, baslik, tur, durum, marka_adi, vergi_no):
        super().__init__(id_c, id_sahip, baslik, tur, durum)
        self.marka_adi = marka_adi
        self.vergi_no = vergi_no


    def kanal_tipi(self):
        return "marka"

    def ek_bilgiler(self):
        return {
            "marka_adi": self.marka_adi,
            "vergi_no": self.vergi_no,
        }
    def reklam_baslat(self, butce):
        if butce <= 0:
            return "Geçersiz reklam bütçesi"
        return f"{self.marka_adi} için {butce} TL bütçeli reklam başlatıldı"

    def vergi_no_gecerli_mi(self):
        return isinstance(self.vergi_no, str) and len(self.vergi_no) >= 10

    def marka_bilgisi(self):
        return f"Marka: {self.marka_adi}, Vergi No: {self.vergi_no}"


# --- ÇOCUK KANALI ---
class CocukKanali(KanalC):
    def __init__(
        self,
        id_c,
        id_sahip,
        baslik,
        tur,
        durum,
        yas_limiti,
        veli_izni
    ):
        super().__init__(id_c, id_sahip, baslik, tur, durum)
        self.yas_limiti = yas_limiti
        self.veli_izni = veli_izni

    def kanal_tipi(self):
        return "cocuk"

    def ek_bilgiler(self):
        return {
        "yas_limiti": self.yas_limiti,
        "veli_izni": self.veli_izni
    }

    def veli_kontrolu(self, giris_yapan_id):
        return self.veli_izni == giris_yapan_id

    def icerik_izni_var_mi(self):
        return self.veli_izni is not None

    def guvenli_kanal_bilgisi(self):
        return "Bu kanal çocuklara özel güvenli içerik sunar"
