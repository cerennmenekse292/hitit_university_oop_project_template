"""
Kanal Yönetim Modülü1 – Servis Katmanı

Bu dosya, kanal nesneleri üzerinde yapılan iş kurallarını içerir.
Veri erişimi repository katmanı üzerinden sağlanır.
Kanal oluşturma, güncelleme, durum değiştirme ve listeleme
işlemleri bu katmanda merkezi olarak yönetilir.
"""
from Channel_modul1.repository import KanalDeposu
from Channel_modul1.base import KanalC

# -------------------- CUSTOM EXCEPTIONS --------------------

class KanalHatasi(Exception):
    """Tüm kanal hataları için temel sınıf."""
    pass


class KanalBulunamadiHatasi(KanalHatasi):
    """Kanal bulunamadığında fırlatılır."""
    pass


class KanalValidasyonHatasi(KanalHatasi):
    """Kanal kurallara uymadığında fırlatılır."""
    pass

# -------------------- VALIDATION SERVICE --------------------

class KanalValidationService:
    """
    Kanal nesneleri için iş kurallarını ve doğrulamaları yapar.
    Repository ile doğrudan iletişim kurmaz.
    """

    GECERLI_TURLER = ["oyun", "egitim", "vlog", "muzik", "teknoloji"]

    def kanal_dogrula(self, kanal: KanalC):
        if not kanal.baslik or kanal.baslik.strip() == "":
            raise KanalValidasyonHatasi("Kanal başlığı boş olamaz")

        if kanal.tur not in self.GECERLI_TURLER:
            raise KanalValidasyonHatasi("Geçersiz kanal türü")

        if kanal.durum not in ["onay_bekliyor", "aktif"]:
            raise KanalValidasyonHatasi("Başlangıç durumu geçersiz")

        self._kanal_tipine_ozel_kurallar(kanal)

    def _kanal_tipine_ozel_kurallar(self, kanal: KanalC):
        tip = kanal.kanal_tipi()

        if tip == "bireysel":
            if kanal.abone_sayisi < 0:
                raise KanalValidasyonHatasi("Abone sayısı negatif olamaz")

        elif tip == "marka":
            if not kanal.marka_adi:
                raise KanalValidasyonHatasi("Marka kanalı şirket adı içermeli")

        elif tip == "cocuk":
            if kanal.veli_izni is None:
                raise KanalValidasyonHatasi("Çocuk kanalı için veli bilgisi zorunlu")


class KanalService:
    """
    KanalService, kanal yönetim modülündeki ana iş kurallarını içerir.
    Kanal oluşturma, güncelleme, arama ve listeleme işlemlerini yürütür.
    """

    def __init__(self, repository: KanalDeposu):
        self.repository = repository
        self.validation_service = KanalValidationService()

    # -------------------- OLUŞTURMA --------------------
    def kanal_olustur(self, kanal: KanalC):
        self.validation_service.kanal_dogrula(kanal)

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

    def __init__(self, repository: KanalDeposu):
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

    def __init__(self, repository: KanalDeposu):
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
class KanalIstatistikServisi:
    def __init__(self, repository):
        self.repository = repository

    def en_cok_aboneli_kanal(self):
        kanallar = self.repository.tum_kanallari_getir()
        if not kanallar:
            return None

        max_kanal = kanallar[0]
        for kanal in kanallar:
            if hasattr(kanal, "abone_sayisi"):
                if kanal.abone_sayisi > getattr(max_kanal, "abone_sayisi", 0):
                    max_kanal = kanal
        return max_kanal

    def en_az_aboneli_kanal(self):
        kanallar = self.repository.tum_kanallari_getir()
        sonuc = None
        for kanal in kanallar:
            if hasattr(kanal, "abone_sayisi"):
                if sonuc is None or kanal.abone_sayisi < sonuc.abone_sayisi:
                    sonuc = kanal
        return sonuc

    def ortalama_abone_sayisi(self):
        toplam = 0
        sayac = 0
        for kanal in self.repository.tum_kanallari_getir():
            if hasattr(kanal, "abone_sayisi"):
                toplam += kanal.abone_sayisi
                sayac += 1
        return toplam / sayac if sayac > 0 else 0

    def abone_araligina_gore_listele(self, min_abone, max_abone):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if hasattr(kanal, "abone_sayisi"):
                if min_abone <= kanal.abone_sayisi <= max_abone:
                    sonuc.append(kanal)
        return sonuc


class KanalGecmisServisi:
    def __init__(self, repository):
        self.repository = repository

    def kanal_olusturma_kaydi(self, kanal):
        mesaj = f"Kanal oluşturuldu: {kanal.baslik}"
        self.repository.islem_kaydi_ekle(mesaj)

    def kanal_silme_kaydi(self, kanal):
        mesaj = f"Kanal silindi: {kanal.baslik}"
        self.repository.islem_kaydi_ekle(mesaj)

    def kanal_durum_degisim_kaydi(self, kanal, eski, yeni):
        mesaj = f"{kanal.baslik} durumu {eski} -> {yeni}"
        self.repository.islem_kaydi_ekle(mesaj)

    def tum_kayitlari_getir(self):
        return self.repository.islem_kayitlarini_getir()


class KanalFiltrelemeServisi:
    def __init__(self, repository):
        self.repository = repository

    def baslik_ile_baslayanlar(self, harf):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if kanal.baslik.lower().startswith(harf.lower()):
                sonuc.append(kanal)
        return sonuc

    def baslik_uzunluguna_gore(self, min_uzunluk):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if len(kanal.baslik) >= min_uzunluk:
                sonuc.append(kanal)
        return sonuc

    def pasif_kanallar(self):
        return [
            kanal for kanal in self.repository.tum_kanallari_getir()
            if kanal.durum != "aktif"
        ]


class KanalGuvenlikServisi:
    def __init__(self, repository):
        self.repository = repository

    def silinmis_kanal_kontrol(self, kanal_id):
        kanal = self.repository.id_ile_bul(kanal_id)
        if not kanal:
            return False
        return kanal.durum == "silindi"

    def kanal_erisim_kontrol(self, kanal_id, kullanici_id):
        kanal = self.repository.id_ile_bul(kanal_id)
        if not kanal:
            return False
        return kanal.id_sahip == kullanici_id


class KanalBakimServisi:
    def __init__(self, repository):
        self.repository = repository

    def silinmisleri_temizle(self):
        silinecekler = []
        for kanal_id, kanal in self.repository.kanallar.items():
            if kanal.durum == "silindi":
                silinecekler.append(kanal_id)

        for kanal_id in silinecekler:
            del self.repository.kanallar[kanal_id]

    def askida_olanlari_listele(self):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if kanal.durum == "askıya_alındı":
                sonuc.append(kanal)
        return sonuc

    def sistem_durumu_raporu(self):
        rapor = {
            "toplam": 0,
            "aktif": 0,
            "pasif": 0,
            "silinmis": 0
        }

        for kanal in self.repository.tum_kanallari_getir():
            rapor["toplam"] += 1
            if kanal.durum == "aktif":
                rapor["aktif"] += 1
            elif kanal.durum == "silindi":
                rapor["silinmis"] += 1
            else:
                rapor["pasif"] += 1

        return rapor
    



# ==========================================================
# EK SERVİS – KANAL ANALİZ VE DENETİM SERVİSİ
# ==========================================================

class KanalAnalizServisi:
    """
    KanalAnalizServisi, kanallar üzerinde
    ileri seviye analiz ve denetim işlemleri yapar.

    Amaç:
    - Aktif / pasif oranlarını hesaplamak
    - Sorunlu kanalları tespit etmek
    - Sistem sağlığı hakkında özet bilgi vermek
    """

    def __init__(self, repository):
        self.repository = repository

    def aktif_kanal_orani(self):
        kanallar = self.repository.tum_kanallari_getir()
        if not kanallar:
            return 0

        aktif = 0
        for kanal in kanallar:
            if kanal.durum == "aktif":
                aktif += 1

        return aktif / len(kanallar)

    def pasif_kanal_orani(self):
        kanallar = self.repository.tum_kanallari_getir()
        if not kanallar:
            return 0

        pasif = 0
        for kanal in kanallar:
            if kanal.durum != "aktif":
                pasif += 1

        return pasif / len(kanallar)

    def onay_bekleyen_kanallar(self):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if kanal.durum == "onay_bekliyor":
                sonuc.append(kanal)
        return sonuc

    def askida_olan_kanallar(self):
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if kanal.durum == "askıya_alındı":
                sonuc.append(kanal)
        return sonuc

    def sorunlu_kanallar(self):
        """
        Sorunlu kanal:
        - Başlığı çok kısa olan
        - Pasif durumda olan
        """
        sonuc = []
        for kanal in self.repository.tum_kanallari_getir():
            if len(kanal.baslik) < 5 or kanal.durum != "aktif":
                sonuc.append(kanal)
        return sonuc

    def kanal_saglik_raporu(self):
        rapor = {
            "toplam": 0,
            "aktif": 0,
            "pasif": 0,
            "onay_bekleyen": 0,
            "askida": 0
        }

        for kanal in self.repository.tum_kanallari_getir():
            rapor["toplam"] += 1

            if kanal.durum == "aktif":
                rapor["aktif"] += 1
            elif kanal.durum == "onay_bekliyor":
                rapor["onay_bekleyen"] += 1
                rapor["pasif"] += 1
            elif kanal.durum == "askıya_alındı":
                rapor["askida"] += 1
                rapor["pasif"] += 1
            elif kanal.durum == "silindi":
                rapor["pasif"] += 1

        return rapor

    def ozet_yazdir(self):
        rapor = self.kanal_saglik_raporu()
        print("=== KANAL SİSTEM SAĞLIK RAPORU ===")
        for anahtar, deger in rapor.items():
            print(f"{anahtar}: {deger}")
