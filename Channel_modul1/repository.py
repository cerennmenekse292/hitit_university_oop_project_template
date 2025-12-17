# Kanal verilerinin tutulduğu repository katmanı

class KanalDeposu:
    """
    Kanalları bellek içinde (in-memory) saklayan basit depo sınıfı.
    """

    def __init__(self):
        self.kanallar = {}

    def kanal_ekle(self, kanal):
        """
        Yeni bir kanalı depoya ekler.
        """
        self.kanallar[kanal.id_c] = kanal

    def kanal_sil(self, kanal_id):
        """
        Kanalı tamamen silmez, durumunu 'silindi' yapar.
        """
        kanal = self.kanallar.get(kanal_id)
        if kanal:
            kanal.sil()

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