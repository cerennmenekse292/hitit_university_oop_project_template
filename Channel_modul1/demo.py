"""
Kanal Yönetim Modülü1 – Demo Senaryosu

Bu dosya, kanal yönetim sisteminin
gerçek bir kullanım senaryosunu simüle eder.

Amaç:
- Repository + Service kullanımını göstermek
- Farklı kanal türleriyle polimorfizmi kanıtlamak
- Kanal durum geçişlerini test etmek
"""

from Channel_modul1.repository import KanalDeposu
from Channel_modul1.services import (
    KanalService,
    KanalDurumYonetici,
    KanalRaporlamaServisi
)
from Channel_modul1.implementations import (
    BireyselKanal,
    MarkaKanal,
    CocukKanal
)

def demo_calistir():
    print("=== KANAL YÖNETİM MODÜLÜ DEMO BAŞLADI ===\n")

    # Repository ve servisler
    repository = KanalDeposu()
    kanal_service = KanalService(repository)
    durum_yonetici = KanalDurumYonetici(repository)
    rapor_servisi = KanalRaporlamaServisi(repository)

    # -------------------- KANAL OLUŞTURMA --------------------
    kanal1 = BireyselKanal(
        id_c=1,
        id_sahip=101,
        baslik="Ceren'in Günlüğü",
        tur="vlog",
        durum="onay_bekliyor",
        abone_sayisi=120,
        renk_temasi="mor"
    )

    kanal2 = MarkaKanal(
        id_c=2,
        id_sahip=201,
        baslik="TechWorld Resmi",
        tur="teknoloji",
        durum="aktif",
        sirket_adi="TechWorld A.Ş.",
        reklam_butcesi=50000
    )

    kanal3 = CocukKanal(
        id_c=3,
        id_sahip=301,
        baslik="Minik Kaşifler",
        tur="egitim",
        durum="aktif",
        yas_limiti=7,
        ebeveyn_onayi=True
    )

    # Kanalları sisteme ekle
    kanal_service.kanal_olustur(kanal1)
    kanal_service.kanal_olustur(kanal2)
    kanal_service.kanal_olustur(kanal3)

    print("✔ Kanallar oluşturuldu.\n")

    # -------------------- POLİMORFİZM --------------------
    print("=== TÜM KANALLAR (Polimorfizm) ===")
    tum_kanallar = repository.tum_kanallari_getir()

    for kanal in tum_kanallar:
        kanal.bilgileri_goster()
        print("Kanal tipi:", kanal.kanal_tipi())
        print("Ek bilgiler:", kanal.ek_bilgiler())
        print("-" * 40)

    # -------------------- DURUM GEÇİŞİ --------------------
    print("\n=== DURUM GÜNCELLEME ===")
    durum_yonetici.onayla_ve_aktif_et(1)
    durum_yonetici.durumu_degistir(2, "askıya_alındı")

    for kanal in repository.tum_kanallari_getir():
        print(f"{kanal.baslik} -> {kanal.durum}")

    # -------------------- ARAMA VE FİLTRELEME --------------------
    print("\n=== 'Tech' İÇEREN KANALLAR ===")
    bulunanlar = kanal_service.kanal_basliga_gore_ara("Tech")
    for kanal in bulunanlar:
        print(kanal.baslik)

    print("\n=== AKTİF KANALLAR ===")
    aktifler = rapor_servisi.aktif_kanallari_getir()
    for kanal in aktifler:
        print(kanal.baslik)

    # -------------------- RAPORLAMA --------------------
    print("\n=== RAPORLAR ===")
    print("Toplam kanal sayısı:", rapor_servisi.toplam_kanal_sayisi())
    print("Duruma göre:", rapor_servisi.duruma_gore_sayim())
    print("Türe göre:", rapor_servisi.ture_gore_sayim())
    print("Kanal tipine göre:", rapor_servisi.tipe_gore_sayim())

    print("\n=== DEMO TAMAMLANDI ===")


if __name__ == "__main__":
    demo_calistir()
       