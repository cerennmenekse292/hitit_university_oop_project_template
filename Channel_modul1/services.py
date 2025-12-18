"""
Kanal Yönetim Modülü – Servis Katmanı

Bu dosya, kanal nesneleri üzerinde yapılan iş kurallarını içerir.
Veri erişimi repository katmanı üzerinden sağlanır.
Kanal oluşturma, güncelleme, durum değiştirme ve listeleme
işlemleri bu katmanda merkezi olarak yönetilir.
"""
from Channel_modul1.repository import KanalRepository
from Channel_modul1.base import KanalC

class KanalService:
    """
    KanalService, kanal yönetim modülündeki ana iş kurallarını içerir.
    Kanal oluşturma, güncelleme, arama ve listeleme işlemlerini yürütür.
    """

    def __init__(self, repository: KanalRepository):
        self.repository = repository

    # -------------------- OLUŞTURMA --------------------
    def kanal_olustur(self, kanal: KanalC):
        if not isinstance(kanal, KanalC):
            raise TypeError("Geçersiz kanal nesnesi")

        mevcut = self.repository.id_ile_bul(kanal.id_c)
        if mevcut:
            raise ValueError("Bu ID ile kanal zaten mevcut")

        if kanal.durum not in ["onay_bekliyor", "aktif"]:
            raise ValueError("Kanal başlangıç durumu geçersiz")

        self.repository.kanal_ekle(kanal)
        return kanal

    # -------------------- GÜNCELLEME --------------------
    def kanal_guncelle(self, kanal_id, yeni_baslik=None, yeni_tur=None):
        kanal = self.repository.id_ile_bul(kanal_id)

        if not kanal:
            raise ValueError("Kanal bulunamadı")

        if yeni_baslik:
            kanal.baslik = yeni_baslik

        if yeni_tur:
            kanal.tur = yeni_tur

        return kanal

    # -------------------- SİLME --------------------
    def kanal_sil(self, kanal_id):
        kanal = self.repository.id_ile_bul(kanal_id)

        if not kanal:
            raise ValueError("Kanal bulunamadı")

        kanal.durum = "silindi"
        return kanal

    # -------------------- ARAMA --------------------
    def kanal_id_ile_bul(self, kanal_id):
        return self.repository.id_ile_bul(kanal_id)

    def kanal_basliga_gore_ara(self, anahtar_kelime):
        sonuc = []

        for kanal in self.repository.tum_kanallari_getir():
            if anahtar_kelime.lower() in kanal.baslik.lower():
                sonuc.append(kanal)

        return sonuc

    # -------------------- LİSTELEME --------------------
    def tum_kanallari_getir(self):
        return self.repository.tum_kanallari_getir()

    def duruma_gore_listele(self, durum):
        return self.repository.duruma_gore_listele(durum)

    def ture_gore_listele(self, tur):
        return self.repository.ture_gore_listele(tur)


class KanalDurumYonetici:
    """
    KanalDurumYonetici, kanal durum geçişlerinin
    kontrollü ve kurallı şekilde yapılmasını sağlar.
    """

    GECERLI_DURUMLAR = [
        "onay_bekliyor",
        "aktif",
        "askıya_alındı",
        "silindi"
    ]

    def __init__(self, repository: KanalRepository):
        self.repository = repository

    def durum_gecerli_mi(self, durum):
        return durum in self.GECERLI_DURUMLAR

    def durumu_degistir(self, kanal_id, yeni_durum):
        kanal = self.repository.id_ile_bul(kanal_id)

        if not kanal:
            raise ValueError("Kanal bulunamadı")

        if not self.durum_gecerli_mi(yeni_durum):
            raise ValueError("Geçersiz kanal durumu")

        if kanal.durum == "silindi":
            raise ValueError("Silinmiş kanalın durumu değiştirilemez")

        kanal.durum = yeni_durum
        return kanal

    def kanali_sil(self, kanal_id):
        kanal = self.repository.id_ile_bul(kanal_id)

        if not kanal:
            raise ValueError("Kanal bulunamadı")

        kanal.durum = "silindi"
        return kanal

    def onayla_ve_aktif_et(self, kanal_id):
        kanal = self.repository.id_ile_bul(kanal_id)

        if not kanal:
            raise ValueError("Kanal bulunamadı")

        if kanal.durum != "onay_bekliyor":
            raise ValueError("Kanal onay beklemiyor")

        kanal.durum = "aktif"
        return kanal
    
class KanalRaporlamaServisi:
    """
    KanalRaporlamaServisi, kanallar üzerinden
    basit istatistiksel raporlar üretir.
    """

    def __init__(self, repository: KanalRepository):
        self.repository = repository

    def toplam_kanal_sayisi(self):
        return len(self.repository.tum_kanallari_getir())

    def duruma_gore_sayim(self):
        sonuc = {}

        for kanal in self.repository.tum_kanallari_getir():
            sonuc.setdefault(kanal.durum, 0)
            sonuc[kanal.durum] += 1

        return sonuc

    def ture_gore_sayim(self):
        sonuc = {}

        for kanal in self.repository.tum_kanallari_getir():
            sonuc.setdefault(kanal.tur, 0)
            sonuc[kanal.tur] += 1

        return sonuc

    def tipe_gore_sayim(self):
        sonuc = {}

        for kanal in self.repository.tum_kanallari_getir():
            tip = kanal.kanal_tipi()
            sonuc.setdefault(tip, 0)
            sonuc[tip] += 1

        return sonuc

    def aktif_kanallari_getir(self):
        return [
            kanal for kanal in self.repository.tum_kanallari_getir()
            if kanal.durum == "aktif"
        ]
