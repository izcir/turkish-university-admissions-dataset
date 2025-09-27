# Veri Temizleme ve Standardizasyon Süreci - Detaylı Notlar

Bu doküman, YÖK Atlas'tan ham olarak çekilen lisans ve önlisans bölüm verileri üzerinde yapılan temizleme, standardizasyon ve birleştirme süreçlerinin teknik detaylarını içermektedir.

## 1. Etiket (Tag) Standardizasyonu

Bölüm isimlerinin sonuna eklenen parantez içindeki bilgiler (etiketler), ham halde 100'den fazla farklı değer içeriyordu. Bu etiketler arasında il/ilçe isimleri, anlamsız kısaltmalar (`Bk. ...`) ve tekrar eden bilgiler bulunuyordu. Analiz için anlamlı olanlar aşağıdaki gibi filtrelendi ve standartlaştırıldı.

### 1.1. Lisans Programları İçin Seçilen Etiketler

```
- Almanca, Fransızca, Çince
- %50 İndirimli, %75 İndirimli, %25 İndirimli, Burslu, Ücretli
- KKTC Uyruklu, M.T.O.K.
- Lehçe, Bulgarca, Rusça, Ermenice, İspanyolca, Arapça, İtalyanca, Farsça, Korece
- Milli Savunma Bakanlığı Adına, İçişleri Bakanlığı Adına
- Erkek, Kız
- İÖ (İkinci Öğretim)
- Açıköğretim, Uzaktan Öğretim
```
*Not: `KKTC Uyruklu` ve `KKTC UYRUKLU` gibi varyasyonlar tek bir etiket altında birleştirilmiştir.*

### 1.2. Önlisans Programları İçin Seçilen Etiketler

```
- %75 İndirimli, %25 İndirimli, %50 İndirimli, Burslu, Ücretli
- İçişleri Bakanlığı Adına, Milli Savunma Bakanlığı Adına
- Uzaktan Öğretim, Açıköğretim
- Arapça, Rusça, İngilizce, İspanyolca
- İÖ (İkinci Öğretim)
- Kız, Erkek
- KKTC Uyruklu
```
*Not: `%25 İNDİRİMLİ` ve `%25 İndirimli` gibi büyük/küçük harf farklılıkları; `İÖ` ve `İö` gibi varyasyonlar standart hale getirilmiştir.*

## 2. ID ve Bölüm Adı Tutarsızlıkları Yönetimi

### 2.1. Lisans ve Önlisans ID Çakışmaları

Aşağıdaki program ID'leri, 2022'de lisans programı iken 2023-2024'te önlisans programı olarak yeniden kullanılmıştır. Veri bütünlüğünü sağlamak ve en güncel bilgiyi korumak amacıyla, bu ID'lere ait **eski (2022) lisans kayıtları silinmiş, yeni (2023-2024) önlisans kayıtları korunmuştur**.
- `202090382`, `202090389`, `202390269`, `109890188`

### 2.2. Yıllar İçinde İsmi Tamamen Değişen Bölümler

Bazı program ID'lerinin farklı yıllarda tamamen alakasız bölümlere atandığı tespit edildi. Bu durum, bölümün kapandığı ve ID'nin başka bir bölüme yeniden atandığını göstermektedir. Analizde istisna yönetimi karmaşıklığı yaratmamak için bu ID'ler **veri setinden tamamen çıkarılmıştır**:
- `203851992`: ('Havacılık Elektrik ve Elektroniği' ve 'Grafik Tasarımı')
- `107790346`: ('Antropoloji' ve 'Sosyoloji')
- `409610608`: ('Halkla İlişkiler ve Reklamcılık' ve 'Moda Tasarımı')

## 3. Eksik Verilerin Yönetimi (`onlisans_2021` Özel Durumu)

`onlisans_2021` verisinde ciddi eksiklikler mevcuttu:
- Yaklaşık 300 bölümün üniversite adı gibi genel bilgileri boştu. Bu bölümlerin bilgileri, 2020 ve 2019 verilerindeki aynı ID'li kayıtlardan dolduruldu.
- Aşağıdaki 30 program ID'sine ait kayıtlarda hem üniversite hem de bölüm adı bilgisi tamamen boştu. Bu ID'ler veri bütünlüğünü bozduğu için **önlisans programlarından çıkarılmıştır**:
  ```json
  [
      "110090130", "111091428", "202390234", "102590333", "108290342", 
      "200390165", "200390166", "202390230", "107690283", "111372222", 
      "100790529", "110090121", "202390235", "110090118", "200950636", 
      "112270826", "202390233", "112270824", "111490234", "202390236", 
      "201290312", "200950635", "112270825", "101490477", "202090343", 
      "107090280", "110090126", "102990396", "200790517", "112270829"
  ]
  ```
- Bu temizleme sürecinin bir yan etkisi olarak, ana listede bölüm adı `""` (boş string) olan bazı kayıtlar kalmıştır. Bu durum bilinen bir sorundur ve mevcut analizleri etkilememektedir.

## 4. Diğer Standardizasyonlar ve Bilinen Notlar

### 4.1. Üniversite Adı Standardizasyonu

Yıllar içinde bazı üniversitelerin isimleri değişmiştir. Veri setinde tutarlılığı sağlamak amacıyla, bir üniversiteye ait tüm kayıtlar (geçmiş yıllardaki veriler dahil) **en güncel ismiyle** standartlaştırılmıştır. Üniversitenin eski adı, `universities_normalized.csv` dosyasındaki `old_name` sütununda referans olarak tutulmaktadır.

### 4.2. Bölüm Adı Standardizasyonu

Yıllar içinde aynı bölümün isminde küçük yazım farklılıkları olduğu tespit edilmiştir (örneğin, `İngiliz Dil Bilimi` ->, `İngiliz Dilbilimi`, `Kurgu-Ses ve Görüntü Yönetimi` -> `Kurgu, Ses ve Görüntü Yönetimi`). Veri setinde tutarlılığı sağlamak amacıyla, bir bölüme ait tüm kayıtlar **en güncel yıldaki ismiyle** standart hale getirilmiştir. Bu sayede, aynı bölüm farklı yıllarda farklı isimlerle görünmemektedir.