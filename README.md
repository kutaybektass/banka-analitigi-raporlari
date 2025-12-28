# Banka Analitiği Portföy Projesi

Bu proje, tamamen sentetik ancak gerçekçi bir veri kümesi üzerine kurulu, uçtan uca SQL odaklı bir bankacılık analitiği portföyüdür. Amaç, bankacılık düzeyinde finansal doğruluktan ziyade analitik düşünme, veri modelleme ve iş odaklı SQL sorgulama becerilerini göstermektir.

Proje, finansal analitik alanında yaygın olarak karşılaşılan alanları ele almaktadır:

* Dolandırıcılık tespiti
* Kredi risk değerlendirmesi
* Ürün kararlılık analizi
* Müşteri kaybı tespiti ve etki analizi

Bütün veriler yazılım programı aracılığıyla oluşturulmuş olup, veriler arasındaki tutarlılık olabildiğince korunmaya çalışılmıştır.

## Veri Oluşturma

* Veritabanı: MySQL

* Veri oluşturma araçları: Python (faker, random)

## Ana Tablolar

* customers — müşteri bilgileri ve sınıflandırma
* accounts — müşteri hesapları ve hesap tipleri (Çek hesabı, Vadeli hesap, Birikim hesabı, Kredi hesabı, Para piyasası heasbı)
* transactions — para transfer işlemleri
* loans — kredi portföyü detayları


# Birinci Analiz: Dolandırıcılık Tespiti
Hedef: Şüpheli transferleri tespit etmek

## Nasıl hesaplandı?
* 9000 ve 9999 arası transfer işlemlerine odaklanıldı
* 30 gün içerisinde 3 veya daha fazla işlem yapan müşteriler işaretlendi

## Kullanılan Teknikler
* COUNT() OVER (PARTITION BY ... RANGE BETWEEN INTERVAL ...)
* Zamana bağlı pencere fonksiyonları (Window functions)

### Not
Kısıtlamalara uyan hiçbir veri bulunamadığı için, sorgulama herhangi bir sonuç göstermedi.

# İkinci Analiz: Kredi Risk Değerlendirmesi
Hedef: Kredi portföy kalitesini iki sorgu içerisinde değerlendirmek

## Kredi Risk Seviyesi Sınıflandırması
Risk seviyeleri:
* Low Risk
* Medium Risk
* High Risk
olmak üzere üç sınıfa ayrılmıştır.

## Değerlendirmeye Alınan Risk Sinyalleri
* Kredi durumu (Ödenmiş, Aktif, Geciktirilmiş)
* Kalan ödeme oranı
* Kredi vade uzunluğu
* Faiz oranı

Sınıflandırma kuralları, karmaşıklıktan ziyade yorumlanabilirliğe öncelik verilerek, kasıtlı olarak kural tabanlı ve açıklanabilir şekilde oluşturulmuştur.

### Birinci Sorgu
Müşterilerin risk sinyalleri baz alınarak kredi risk sınıflandırması yapılmıştır.

<img width="1084" height="637" alt="resim" src="https://github.com/user-attachments/assets/4c8aa794-b23d-498c-91d1-1864f59c7a70" />

### İkinci Sorgu
Risk sınıflandırması gruplandırılarak, her risk grubundaki toplam kredi sayısı, toplam kredi miktarı ve toplam kalan miktar hesaplanmıştır.

<img width="393" height="75" alt="resim" src="https://github.com/user-attachments/assets/44db3351-98fe-4021-b138-103369ea249b" />

# Üçüncü Analiz: Ürün Karlılık Analizi
Hedef: Hangi bankacılık ürünlerinin yapısal olarak para kazandırdığının veya maliyet getirdiğinin anlaşılması

## Nasıl Hesaplandı?
* Faiz davranışına dayalı bir karlılık sistemi oluşturuldu
* Kredilerdeki faizler: Gelir
* Mevduat ürünleri (Birikim, Vadeli ve Para Piyasası hesapları): Gider

### Not
Buradaki amaç kar hesaplamak değil, farklı hesap türlerinin bankaya olan gelir katkısını karşılaştırmaktır.

<img width="312" height="106" alt="resim" src="https://github.com/user-attachments/assets/6489bd66-a34c-4465-9250-89e6fa4ae742" />

# Dördüncü Analiz: Müşteri Kaybı Tespiti
Hedef: Ayrılma riski olan müşterileri belirlemek

## Değerlendirmeye Alınan Sinyaller
* En az bir adet hesabı kapalı veya dondurulmuş olan müşteriler
* 30 gün içerisinde hiçbir transfer işlemi yapmamış müşteriler
* Hesaplar arasındaki toplam parası 3000'den az olan müşteriler

## Kategoriler
* Partially Churned — en az bir adet hesabı kapalı veya dondurulmuş
* High Risk — 30 gün boyunca hiç işlem yapmamış VE toplam parası 3000'den az
* Medium Risk — 30 gün boyunca hiç işlem yapmamış VEYA toplam parası 3000'den az
* Low Risk — diğer herkes

### Not
Bu analiz, çoktan ayrılmış müşterileri dahil etmeyip, ayrılma riski olan müşterileri kapsar. Partially Churned tam olarak burada devreye giriyor.

<img width="790" height="837" alt="resim" src="https://github.com/user-attachments/assets/0a04678a-796b-43ab-ad9a-ea695b18b40d" />

# Beşinci Analiz: Müşteri Kaybının Etkisi
Hedef: Müşteri kaybı kategorilerine göre riskleri ölçmek

## Yaklaşım
* Her kayıp kategorisindeki müşteri sayıları hesaplandı
* Riskte olan toplam miktar hesaplandı
* Müşteri başına ortalama miktar hesaplandı

<img width="394" height="89" alt="resim" src="https://github.com/user-attachments/assets/1d251b74-de63-425b-8ef5-93b1685ef015" />


# Kısıtlamalar
* Yapay veri üstünde çalışıldı
* Finansal mantık basitleştirildi

Bu kısıtlamalar, SQL analizine ve çıkarım yapmaya odaklanılması için kasıtlı olarak yapılmıştır. 

# Sonuç
Bu projede şunlar amaçlanmıştır:

* İş sorularını SQL'e çevirmek
* Ham verilerden analitik sinyaller tasarlamak

**Bu bir portföy sergileme projesidir, üretim amaçlı bir finansal sistem değildir.**




