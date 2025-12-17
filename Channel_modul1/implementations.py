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


# --- MARKA KANALI ---
class MarkaKanali(KanalC):
    def __init__(
        self,
        id_c,
        id_sahip,
        baslik,
        tur,
        durum,
        marka_adi,
        vergi_no,
    ):
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


# --- ÇOCUK KANALI ---
class CocukKanali(KanalC):
    def __init__(
        self,
        id_c,
        id_sahip,
        baslik,
        tur,
        durum,
        veli_id,
    ):
        super().__init__(id_c, id_sahip, baslik, tur, durum)
        self.veli_id = veli_id

    def kanal_tipi(self):
        return "cocuk"

    def ek_bilgiler(self):
        return {
            "veli_id": self.veli_id
        }