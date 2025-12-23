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
    KanalRaporlamaServisi,
    KanalIstatistikServisi,
    KanalFiltrelemeServisi,
    KanalGuvenlikServisi,
    KanalBakimServisi

)
from Channel_modul1.implementations import (
    BireyselKanal,
    MarkaKanali,
    CocukKanali
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

    kanal2 = MarkaKanali(
        id_c=2,
        id_sahip=201,
        baslik="TechWorld Resmi",
        tur="teknoloji",
        durum="aktif",
        marka_adi="TechWorld A.Ş.",
        vergi_no="1234567890"
    )

    kanal3 = CocukKanali(
        id_c=3,
        id_sahip=301,
        baslik="Minik Kaşifler",
        tur="egitim",
        durum="aktif",
        yas_limiti=7,
        veli_izni=True
    )

    # Kanalları sisteme ekle
    kanal_service.kanal_olustur(kanal1)
    kanal_service.kanal_olustur(kanal2)
    kanal_service.kanal_olustur(kanal3)

    print("✔ Kanallar oluşturuldu.\n")

    # -------------------- EKSTRA KANALLAR --------------------
    kanal4 = BireyselKanal(
        id_c=4,
        id_sahip=102,
        baslik="Gamers Daily",
        tur="vlog",
        durum="aktif",
        abone_sayisi=200,
        renk_temasi="mavi"
    )
    kanal_service.kanal_olustur(kanal4)

    kanal5 = MarkaKanali(
        id_c=5,
        id_sahip=202,
        baslik="Foodies Official",
        tur="teknoloji",
        durum="aktif",
        marka_adi="Foodies Ltd.",
        vergi_no="9876543210"
    )
    kanal_service.kanal_olustur(kanal5)

    kanal6 = CocukKanali(
        id_c=6,
        id_sahip=302,
        baslik="Küçük Bilim İnsanları",
        tur="egitim",
        durum="onay_bekliyor",
        yas_limiti=10,
        veli_izni=True
    )
    kanal_service.kanal_olustur(kanal6)

    kanal7 = BireyselKanal(
        id_c=7,
        id_sahip=103,
        baslik="Travel With Ceren",
        tur="vlog",
        durum="aktif",
        abone_sayisi=150,
        renk_temasi="yeşil"
    )
    kanal_service.kanal_olustur(kanal7)

    kanal8 = MarkaKanali(
        id_c=8,
        id_sahip=203,
        baslik="Tech Reviews",
        tur="teknoloji",
        durum="aktif",
        marka_adi="TechCorp",
        vergi_no="5555555555"
    )
    kanal_service.kanal_olustur(kanal8)

    

    print("✔ Ekstra kanallar oluşturuldu.\n")


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

    print("\n=== RAPORLAR ===")
    print("Toplam kanal sayısı:", rapor_servisi.toplam_kanal_sayisi())
    print("Duruma göre:", rapor_servisi.duruma_gore_sayim())
    print("Türe göre:", rapor_servisi.ture_gore_sayim())
    print("Kanal tipine göre:", rapor_servisi.tipe_gore_sayim())

    # -------------------- EK SERVİSLER ÇIKTI --------------------
    istatistik_servisi = KanalIstatistikServisi(repository)
    filtre_servisi = KanalFiltrelemeServisi(repository)
    guvenlik_servisi = KanalGuvenlikServisi(repository)
    bakim_servisi = KanalBakimServisi(repository)

    en_cok = istatistik_servisi.en_cok_aboneli_kanal()
    en_az = istatistik_servisi.en_az_aboneli_kanal()
    print("\n=== ABONE İSTATİSTİKLERİ ===")
    print(f"En çok aboneli kanal: {en_cok.baslik} ({en_cok.abone_sayisi} abone)")
    print(f"En az aboneli kanal: {en_az.baslik} ({en_az.abone_sayisi} abone)")

    pasifler = filtre_servisi.pasif_kanallar()
    print("\n=== PASİF KANALLAR ===")
    for k in pasifler:
        print(k.baslik)

    print("\n=== SİLİNMİŞ KANALLAR ===")
    for kanal in repository.tum_kanallari_getir():
        silinmis_mi = guvenlik_servisi.silinmis_kanal_kontrol(kanal.id_c)
        print(f"{kanal.baslik} silinmiş mi? {silinmis_mi}")

    askida_olanlar = bakim_servisi.askida_olanlari_listele()
    print("\n=== ASKIDA OLAN KANALLAR ===")
    for k in askida_olanlar:
        print(k.baslik)

    
    istatistik_servisi = KanalIstatistikServisi(repository)
    en_cok = istatistik_servisi.en_cok_aboneli_kanal()
    en_az = istatistik_servisi.en_az_aboneli_kanal()
    print("\n=== ABONE İSTATİSTİKLERİ ===")
    print(f"En çok aboneli kanal: {en_cok.baslik} ({en_cok.abone_sayisi} abone)")
    print(f"En az aboneli kanal: {en_az.baslik} ({en_az.abone_sayisi} abone)")
    print("Ortalama abone sayısı:", istatistik_servisi.ortalama_abone_sayisi())


    # DEMO TAMAMLANDI
    print("\n=== DEMO TAMAMLANDI ===")



if __name__ == "__main__":
    demo_calistir()
       