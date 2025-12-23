"""
Kanal Yönetim Modülü1 – Repository Katmanı

Bu dosya, kanal verilerinin saklanması ve yönetilmesini sağlar.
Kanalların eklenmesi, silinmesi, güncellenmesi ve sorgulanması
işlemleri bu katmanda merkezi olarak yürütülür.
Veriye doğrudan erişim ve depolama işlemleri burada gerçekleştirilir.
"""


class KanalDeposu:
    """
    Kanalları bellek içinde (in-memory) saklayan basit depo sınıfı.
    """

    def __init__(self):
        self.kanallar = {}
        self.islem_kayitlari = []

    def kanal_ekle(self, kanal):
        """
        Yeni bir kanalı depoya ekler.
        """
        self.kanallar[kanal.id_c] = kanal

    
    def id_ile_bul(self, kanal_id):
        """
        Kanal ID'sine göre kanal döndürür.
        """
        return self.kanallar.get(kanal_id)

    def tum_kanallari_getir(self):
        """
        Depodaki tüm kanalları liste olarak döndürür.
        """
        return list(self.kanallar.values())

    def duruma_gore_listele(self, durum):
        """
        Belirli bir duruma sahip kanalları listeler.
        """
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.durum == durum
        ]

    def ture_gore_listele(self, tur):
        """
        Kanal türüne (oyun, eğitim, vlog vb.) göre filtreleme yapar.
        """
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.tur == tur
        ]

    def kanal_tipine_gore_listele(self, tip):
        """
        Kanal sınıfına göre filtreleme yapar (bireysel, marka, çocuk).
        """
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.kanal_tipi() == tip
        ]
    def kanal_var_mi(self, kanal_id):
        """
        Belirtilen ID ile kanal olup olmadığını kontrol eder.
        """
        return kanal_id in self.kanallar

    def aktif_kanallari_getir(self):
        """
        Sadece aktif durumdaki kanalları döndürür.
        """
        return [
            kanal for kanal in self.kanallar.values()
            if kanal.durum == "aktif"
        ]

    def basliga_gore_ara(self, kelime):
        """
        Kanal başlığında kelime geçen kanalları listeler.
        """
        sonuc = []

        for kanal in self.kanallar.values():
            if kelime.lower() in kanal.baslik.lower():
                sonuc.append(kanal)

        return sonuc

    def kanal_sayisi(self):
        """
        Toplam kanal sayısını döndürür.
        """
        return len(self.kanallar)

    def islem_kaydi_ekle(self, mesaj):
        """
        Repository üzerinde yapılan işlemleri kaydeder.
        """
        self.islem_kayitlari.append(mesaj)

    def islem_kayitlarini_getir(self):
        """
        Yapılan tüm işlemleri döndürür.
        """
        return self.islem_kayitlari
