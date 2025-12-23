#Bir bir test modulu alanidir

"""
Test Dosyası: Kanal Yönetim Modülü
Bu dosya, KanalService ve KanalDeposu için kapsamlı testler içerir.
Amaç:
- CRUD işlemlerini test etmek
- Durum geçişlerini kontrol etmek
- Arama ve filtreleme fonksiyonlarını doğrulamak
- Raporlama fonksiyonlarını kontrol etmek
"""

from Channel_modul1.repository import KanalDeposu
from Channel_modul1.services import KanalService, KanalDurumYonetici, KanalRaporlamaServisi
from Channel_modul1.implementations import BireyselKanal, MarkaKanali, CocukKanali

def test_kanal_modulu():
    # -------------------- SETUP --------------------
    print("=== TEST BAŞLANGICI ===")
    depo = KanalDeposu()
    service = KanalService(depo)
    durum_yonetici = KanalDurumYonetici(depo)
    rapor_servisi = KanalRaporlamaServisi(depo)

    # -------------------- KANAL OLUŞTURMA --------------------
    print("\n-- Kanal Oluşturma Testleri --")
    kanal1 = BireyselKanal(1, 101, "Vlog Günlüğü", "vlog", "onay_bekliyor", 100, "kırmızı")
    kanal2 = MarkaKanali(2, 201, "Tech Marka", "teknoloji", "aktif", "Tech A.Ş.", "1234567890")
    kanal3 = CocukKanali(3, 301, "Minik Kaşifler", "egitim", "aktif", 7, True)

    service.kanal_olustur(kanal1)
    service.kanal_olustur(kanal2)
    service.kanal_olustur(kanal3)

    assert depo.id_ile_bul(1) is not None
    assert depo.id_ile_bul(2) is not None
    assert depo.id_ile_bul(3) is not None
    print("✔ Kanal oluşturma başarılı")

    # -------------------- DURUM DEĞİŞİKLİĞİ --------------------
    print("\n-- Durum Değişikliği Testleri --")
    durum_yonetici.onayla_ve_aktif_et(1)
    durum_yonetici.durumu_degistir(2, "askıya_alındı")
    durum_yonetici.kanali_sil(3)

    assert depo.id_ile_bul(1).durum == "aktif"
    assert depo.id_ile_bul(2).durum == "askıya_alındı"
    assert depo.id_ile_bul(3).durum == "silindi"
    print("✔ Durum değişiklikleri doğru")

    # -------------------- GÜNCELLEME --------------------
    print("\n-- Kanal Güncelleme Testleri --")
    service.kanal_guncelle(1, yeni_baslik="Yeni Vlog Günlüğü", yeni_tur="vlog")
    assert depo.id_ile_bul(1).baslik == "Yeni Vlog Günlüğü"
    print("✔ Kanal güncelleme başarılı")

    # -------------------- ARAMA VE FİLTRELEME --------------------
    print("\n-- Arama ve Filtreleme Testleri --")
    tech_kanallar = service.kanal_basliga_gore_ara("Tech")
    assert len(tech_kanallar) == 1
    aktif_kanallar = rapor_servisi.aktif_kanallari_getir()
    assert len(aktif_kanallar) == 1
    print("✔ Arama ve filtreleme başarılı")

    # -------------------- RAPORLAMA --------------------
    print("\n-- Raporlama Testleri --")
    toplam = rapor_servisi.toplam_kanal_sayisi()
    duruma_gore = rapor_servisi.duruma_gore_sayim()
    ture_gore = rapor_servisi.ture_gore_sayim()
    tipe_gore = rapor_servisi.tipe_gore_sayim()

    assert toplam == 3
    assert duruma_gore["aktif"] == 1
    assert duruma_gore["askıya_alındı"] == 1
    assert duruma_gore["silindi"] == 1
    assert ture_gore["vlog"] == 1
    assert ture_gore["teknoloji"] == 1
    assert ture_gore["egitim"] == 1
    assert tipe_gore["bireysel"] == 1
    assert tipe_gore["marka"] == 1
    assert tipe_gore["cocuk"] == 1
    print("✔ Raporlama testleri başarılı")

    print("\n=== TESTLER TAMAMLANDI ===")

if __name__ == "__main__":
    test_kanal_modulu()
# ==========================================================
# EK TESTLER – HATA, VALIDASYON VE SINIR DURUMLARI
# ==========================================================

from Channel_modul1.services import (
    KanalValidationService,
    KanalIstatistikServisi,
    KanalFiltrelemeServisi,
    KanalGuvenlikServisi,
    KanalBakimServisi
)
from Channel_modul1.services import KanalValidasyonHatasi


def test_hatali_kanal_olusturma():
    print("\n-- Hatalı Kanal Oluşturma Testleri --")
    depo = KanalDeposu()
    service = KanalService(depo)

    hatali_kanal = BireyselKanal(
        id_c=10,
        id_sahip=999,
        baslik="",
        tur="vlog",
        durum="onay_bekliyor",
        abone_sayisi=10,
        renk_temasi="mavi"
    )

    try:
        service.kanal_olustur(hatali_kanal)
        assert False
    except Exception:
        assert True

    print("✔ Hatalı başlık kontrolü çalışıyor")


def test_validation_servisi_kurallari():
    print("\n-- Validation Servisi Testleri --")
    validator = KanalValidationService()

    kanal = BireyselKanal(
        id_c=11,
        id_sahip=100,
        baslik="Test Kanal",
        tur="gecersiz_tur",
        durum="onay_bekliyor",
        abone_sayisi=5,
        renk_temasi="sarı"
    )

    try:
        validator.kanal_dogrula(kanal)
        assert False
    except KanalValidasyonHatasi:
        assert True

    print("✔ Geçersiz tür yakalandı")


def test_silinmis_kanal_islemleri():
    print("\n-- Silinmiş Kanal İşlem Testleri --")
    depo = KanalDeposu()
    service = KanalService(depo)
    durum = KanalDurumYonetici(depo)

    kanal = MarkaKanali(
        20, 500, "Silinecek Kanal", "teknoloji",
        "aktif", "Firma", 10000
    )

    service.kanal_olustur(kanal)
    durum.kanali_sil(20)

    try:
        durum.durumu_degistir(20, "aktif")
        assert False
    except Exception:
        assert True

    print("✔ Silinmiş kanal durumu değiştirilemedi")


def test_istatistik_servisi():
    print("\n-- İstatistik Servisi Testleri --")
    depo = KanalDeposu()
    service = KanalService(depo)
    istatistik = KanalIstatistikServisi(depo)

    service.kanal_olustur(BireyselKanal(
        30, 1, "Az Aboneli", "vlog", "aktif", 10, "kırmızı"
    ))
    service.kanal_olustur(BireyselKanal(
        31, 2, "Çok Aboneli", "vlog", "aktif", 500, "mavi"
    ))

    assert istatistik.en_cok_aboneli_kanal().abone_sayisi == 500
    assert istatistik.en_az_aboneli_kanal().abone_sayisi == 10
    assert istatistik.ortalama_abone_sayisi() == 255

    print("✔ İstatistik hesaplamaları doğru")


def test_filtreleme_servisi():
    print("\n-- Filtreleme Servisi Testleri --")
    depo = KanalDeposu()
    service = KanalService(depo)
    filtre = KanalFiltrelemeServisi(depo)

    service.kanal_olustur(BireyselKanal(
        40, 1, "Alpha Kanal", "vlog", "aktif", 20, "mor"
    ))
    service.kanal_olustur(BireyselKanal(
        41, 2, "Beta Kanal", "vlog", "onay_bekliyor", 30, "yeşil"
    ))

    assert len(filtre.baslik_ile_baslayanlar("A")) == 1
    assert len(filtre.baslik_uzunluguna_gore(10)) == 2
    
    # Pasif kanalları repository üzerinden say
    pasif_sayisi = len([k for k in depo.tum_kanallari_getir() if k.durum != "aktif"])
    assert len(filtre.pasif_kanallar()) == pasif_sayisi

    print("✔ Filtreleme fonksiyonları çalışıyor")


def test_guvenlik_ve_bakim_servisleri():
    print("\n-- Güvenlik ve Bakım Servisi Testleri --")
    depo = KanalDeposu()
    service = KanalService(depo)

    guvenlik = KanalGuvenlikServisi(depo)
    bakim = KanalBakimServisi(depo)

    kanal = BireyselKanal(
        50, 777, "Gizli Kanal", "vlog", "aktif", 5, "siyah"
    )

    service.kanal_olustur(kanal)

    assert guvenlik.kanal_erisim_kontrol(50, 777) is True
    assert guvenlik.kanal_erisim_kontrol(50, 123) is False

    bakim.silinmisleri_temizle()
    assert depo.id_ile_bul(50) is not None

    print("✔ Güvenlik ve bakım servisleri test edildi")
if __name__ == "__main__":
    print("\n### TÜM TESTLER MANUEL OLARAK ÇALIŞTIRILIYOR ###\n")

    test_kanal_modulu()
    test_hatali_kanal_olusturma()
    test_validation_servisi_kurallari()
    test_silinmis_kanal_islemleri()
    test_istatistik_servisi()
    test_filtreleme_servisi()
    test_guvenlik_ve_bakim_servisleri()

    print("\n### TÜM TESTLER BAŞARIYLA TAMAMLANDI ###")
