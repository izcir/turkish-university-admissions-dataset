# Türkiye Üniversite Bölümleri & İstatistikleri (2019-2024)

### Kontekst (Neden Bu Veri Seti?)

Türkiye'deki üniversite tercihleri ve eğitim trendleri üzerine yapılacak analizler için en değerli kaynak YÖK Atlas'tır. Ancak bu veriler, ham ve yapısal olmayan bir formatta sunulduğu için doğrudan analize uygun değildir. Yıllar arası uyumsuzluklar, eksik veriler ve analiz için elverişsiz formatlar, bu değerli bilgiyi kullanmayı zorlaştırmaktadır.

Bu veri seti, bu sorunu çözmek için oluşturulmuştur. [YokAPI](https://github.com/izcir/YokAPI/) scraper'ı ile çekilen veriler, iki aşamalı bir süreçten geçirilerek sizlere sunulmaktadır: **Ön Temizleme** ve **Normalleştirme**.

Amacım, hem veri bilimine yeni başlayanlar için **alıştırma yapabilecekleri zengin bir kaynak**, hem de deneyimli analistlerin **gerçek dünya problemleri üzerine derinlemesine çalışmalar yapabileceği** kapsamlı ve güvenilir bir veri seti sunmaktır.

### Veri Seti Özeti (Dataset at a Glance)

*   **Zaman Aralığı:** 2019-2024 (6 Yıl) (2025 verileri eklenecektir)
*   **Toplam Satır:** `all_in_one_denormalized.csv` dosyasında **128.352** kayıt bulunmaktadır.
*   **Benzersiz Varlıklar:**
    *   **32.505** farklı Program (`program_code`)
    *   **235** farklı Üniversite
    *   **733** farklı Bölüm Adı
    *   **27** farklı Etiket (`tag`)
*   **En Yaygın Etiketler:** `Burslu` (5.6k+ program), `%50 İndirimli` (5.4k+ program), `İngilizce` (5.2k+ program)

### İçerik (Veri Setinin İçeriği)

Bu veri seti, farklı kullanıcı ihtiyaçlarına yönelik iki formatta sunulmaktadır:

#### 1. `all_in_one_denormalized.csv` (Hızlı Başlangıç için Önerilen)
Bu dosya, **tüm tabloların birleştirilmiş (denormalize edilmiş) halidir.** Veri setindeki her bir satır, bir bölümün belirli bir yıldaki tüm bilgilerini ve istatistiklerini içerir. Veri bilimine yeni başlayanlar, hızlı keşifsel veri analizi (EDA) yapmak isteyenler veya makine öğrenmesi modelleri için veri hazırlayanlar için idealdir.
**Eğer nereden başlayacağınızı bilmiyorsanız, bu dosyayı kullanın.**

**Örnek Satır Yapısı:**
| program_code | year | university_name | city | department_name | score_type | all_tags | total_quota | final_rank_012 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 106510077 | 2024 | ABDULLAH GÜL ÜNİVERSİTESİ | KAYSERİ | Bilgisayar Mühendisliği | SAY | İngilizce | 82 | 46890 |

#### 2. `processed/` Klasörü (İlişkisel Veri)
Bu klasör, veritabanı mantığıyla tasarlanmış, birbiriyle ilişkili ve normalize edilmiş birden çok CSV dosyası içerir. Veri bütünlüğüne önem veren, SQL benzeri `join` işlemleri yapmak isteyen veya veriyi kendi veritabanına aktarmayı planlayan ileri seviye kullanıcılar için uygundur. Bu yapı, veri setinin "source of truth" (doğruluğun kaynağı) versiyonudur ve `all_in_one_denormalized.csv` dosyası bu tablolardan oluşturulmuştur.

**Ana Tablolar (Core Tables):**
*   **`department_stats.csv`**: **Veri setinin kalbidir.** Her bir programın her yıl için kontenjan, yerleşen sayısı, cinsiyet dağılımı, en düşük giriş puanı ve en düşük giriş sıralaması gibi kritik metriklerini içerir.
*   **`departments_normalized.csv`**: Her bir programın zamanla değişmeyen temel bilgilerini (bölüm adı, fakülte, üniversite, puan türü vb.) içerir.

> Veri temizleme sürecinin tüm teknik detayları ve alınan kararlar için projenin **[GitHub reposundaki CLEANING_NOTES.md](https://github.com/izcir/yok-atlas-veri-seti/blob/main/other_readme_files/CLEANING_NOTES.md)** dosyasını inceleyebilirsiniz. <!-- GITHUB LİNKİNİ GÜNCELLE -->

### Kullanım Notları ve Veri Sözlüğü
*   **`program_code`**: Başındaki sıfırların kaybolmaması için `string` (metin) olarak okunmalıdır.
*   **`final_rank_*`**: Bazı satırlarda boş olabilir (`NaN`). Analizlerinizde bu eksik değerleri yönetmeniz gerekebilir. Pandas'ta bu kolonları `pd.to_numeric(df['col'], errors='coerce').astype('Int64')` ile *nullable integer*'a (boş bırakılabilir tamsayı) çevirebilirsiniz.
*   **`all_tags`**: Bir programın birden fazla etiketini içeren, virgülle ayrılmış bir metin alanıdır. Analiz için `split(',')` metodu ile bir listeye dönüştürülebilir.
*   **Fakülte Adları**: `faculty_names.csv` içinde bazı programlar için boş fakülte adı bulunabilir. Bu durum, ham veride fakülte bilgisinin olmamasından kaynaklanmaktadır.

### Gelecek Vizyonu ve Eklenecek Veriler

Bu veri seti, yaşayan ve sürekli gelişen bir projedir. Hedefim, YÖK Atlas'ta bulunan diğer değerli bilgileri de zamanla ekleyerek Türkiye'deki en kapsamlı ve kullanışlı yükseköğretim veri setlerinden birini oluşturmaktır. Gelecek güncellemelerde eklenmesi planlanan bazı veri başlıkları:

*   Yerleşenlerin Geldikleri Coğrafi Bölgeler ve İller
*   Yerleşenlerin Mezun Oldukları Lise Tipleri ve Alanları
*   Yerleşenlerin YKS Net Ortalamaları
*   Yerleşenlerin Tercih Eğilimleri (Ortalama kaçıncı tercihlerine yerleştikleri, en çok tercih ettikleri diğer programlar vb.)

Bu eklemelerle birlikte veri seti, çok daha derin sosyo-ekonomik ve stratejik analizlere olanak tanıyacaktır.

### Veri Setiyle Neler Yapılabilir? (Analiz Fikirleri)

Bu veri seti, basit sorgulardan karmaşık makine öğrenmesi modellerine kadar geniş bir yelpazede analizler için uygundur.

#### Yeni Başlayanlar İçin Analiz Alıştırmaları

*   **Keşifsel Veri Analizi:** 2024 yılında SAY puan türünde en yüksek sıralama ile öğrenci alan ilk 20 bölüm hangileridir?
*   **Filtreleme ve Gruplama:** İstanbul'daki vakıf üniversitelerinde bulunan "Bilgisayar Mühendisliği" bölümlerinin tam burslu kontenjan sayılarını karşılaştırın.
*   **Basit Trendler:** Ankara'daki devlet üniversitelerinde Tıp fakültesi kontenjanları son 5 yılda nasıl değişti?
*   **Görselleştirme:** Türkiye genelinde üniversite türlerinin (Devlet, Vakıf, KKTC) dağılımını bir pasta grafiği ile gösterin.
*   **Doluluk Oranları:** 2023 yılında doluluk oranı %80'in altında kalan önlisans programları hangileridir?

#### İleri Seviye ve Gerçek Dünya Analizleri

*   **Rekabet ve Popülerlik Analizi:** Belirli bir bölümün (örneğin Yapay Zeka Müh.) giriş sıralamaları (`final_rank_012`) yıllar içinde nasıl bir değişim gösterdi? Hangi üniversiteler bu alanda daha rekabetçi hale geliyor?
*   **Stratejik Kontenjan Planlaması:** Üniversitelerin kontenjan artış/azalış kararlarının doluluk oranlarına ve giriş sıralamalarına etkisi nedir? Hangi stratejiler daha başarılı görünüyor?
*   **Sosyo-Demografik Trendler:** Mühendislik gibi alanlarda kadın öğrenci oranı (`female` / `total_enrolled`) yıllar içinde artıyor mu? Bu oran üniversite tipine (devlet/vakıf) veya şehre göre farklılık gösteriyor mu?
*   **Vakıf Üniversitesi Burs Stratejileri:** `%100 Burslu` programların giriş sıralamaları ile `Ücretli` programlar arasındaki sıralama farkı (makas) zamanla nasıl değişiyor? Hangi üniversiteler burslu programlarıyla daha fazla öne çıkıyor?
*   **"Geleceğin Meslekleri" Tespiti:** Son birkaç yılda sürekli olarak yeni açılan, kontenjanları artan ve doluluk oranları yüksek olan bölümleri tespit ederek gelecekteki popüler alanları belirlemeye çalışın.
*   **Tahminleme Modelleri (Makine Öğrenmesi):** Bir bölümün geçmiş yıllardaki sıralama, kontenjan, doluluk oranı ve üniversite bilgilerini kullanarak bir sonraki yılki giriş sıralamasını (`final_rank_012`) tahmin eden bir regresyon modeli geliştirin.
*   **Kümelenme Analizi:** Üniversiteleri; sundukları bölümlerin çeşitliliği, puan türü ağırlıkları ve rekabetçilik seviyelerine göre gruplayarak (örneğin "Teknoloji Odaklı Butik Üniversiteler", "Kapsamlı Devlet Üniversiteleri") benzer profildeki kurumları keşfedin.