# Türkiye Üniversite Bölüm Verileri & İstatistikleri (2019-2024)

🌐 [English](README_en.md) | [Türkçe](README.md)

Bu repo, [YokAPI](https://github.com/izcir/YokAPI/) adlı Python tabanlı scraper aracılığıyla YÖK Atlas ve ÖSYM kaynaklarından elde edilen 2019–2024 yılları arasındaki üniversite bölüm verilerini içerir. Veriler, iki aşamalı bir süreçle analize hazır hale getirilmiştir: **Temizleme** ve **Normalleştirme**.

Ayrıca bu veri seti, üniversite tercih sürecini kolaylaştıran ve yapay zeka destekli analizler sunan kendi sitemin ([sinavizcisi.com](https://sinavizcisi.com)) veritabanının da temelini oluşturmaktadır.

### Veri Setine Hızlı Bakış

Bu veri seti, aşağıdaki istatistiksel özetle tanımlanabilir:
*   **Kapsanan Dönem:** 2019-2024 (Toplam 6 yıl) (2025 verileri eklenecektir)
*   **Toplam Kayıt Sayısı:** 128.352 (Her bir programın her bir yıldaki durumunu gösteren satır)
*   **Benzersiz Program Sayısı:** 32.505 (`program_code`)
*   **Benzersiz Varlıklar:** 235 Üniversite, 733 Bölüm Adı, 1.131 Fakülte


> **Önemli Not:** Bu repodaki veriler iki aşamalı bir süreçten geçmiştir. İlk olarak, `YokAPI` ile çekilen ham veriler, **[`CLEANING_NOTES.md`]([CLEANING_NOTES.md](https://github.com/izcir/turkish-university-admissions-dataset/blob/main/cleaning_notes.md)** dosyasında detaylandırılan adımlarla temizlenmiştir. Bu ilk aşamada tutarsız ID'ler ayıklanmış, üniversite ve bölüm isimleri en güncel halleriyle standartlaştırılmıştır. `data/raw/` klasöründeki dosyalar bu ilk temizleme aşamasının çıktısıdır. İkinci aşamada ise `scripts/` klasöründeki betikler, bu temizlenmiş verileri alıp `data/processed/` altında normalize edilmiş, ilişkisel bir yapıya dönüştürür ve son olarak `all_in_one_denormalized.csv` dosyasını oluşturur. `all_in_one_denormalized.csv` dosyası bütün verilerin ayrıştırılmadan bırakılmış halidir. Veri tekrarını önlemek ve veriyi daha düzenli hale getirmek için `data/processed/` klasöründeki dosyalar tercih edilmelidir.

## 📌 Veri Setinin Amacı ve Değeri

YÖK Atlas, Türkiye'deki yükseköğretim sistemi üzerine yapılacak analizler için en temel ve resmi veri kaynağıdır. Ancak, bu veriler ham halde sunulduğu için doğrudan analiz ve uygulama geliştirmeye elverişli değildir. Veri kullanıcılarının karşılaştığı temel sorunlar şunlardır:

*   **Yıllar Arası Tutarsızlıklar:** Bölüm isimleri, program kodları (ID'ler) ve hatta üniversite adları yıllar içinde değişebilir, bu da zaman serisi analizlerini ve karşılaştırmaları neredeyse imkansız hale getirir.
*   **Eksik ve Dağınık Bilgiler:** Farklı yıllara ait verilerde boşluklar olabilir ve kontenjan, puan, sıralama gibi önemli metrikler farklı sayfalarda dağınık halde bulunur.

Bu veri setinin amacı, yukarıda belirtilen tüm bu sorunları çözerek araştırmacılar, geliştiriciler ve öğrenciler için **temiz, güvenilir ve kullanıma hazır** bir kaynak oluşturmaktır. Bu hedefe ulaşmak için izlenen temel adımlar şunlardır:

*   **Sistematik Veri Toplama:** YÖK Atlas ve ÖSYM'den alınan halka açık verilerin, `YokAPI` gibi araçlarla düzenli ve sistematik bir şekilde toplanması.
*   **Kapsamlı Veri Temizleme ve Standardizasyon:** Tespit edilen ID çakışmaları, bölüm ve üniversite adı farklılıkları, format hataları ve eksik bilgilerin titizlikle giderilmesi ve verinin standart bir yapıya kavuşturulması.
*   **Veri Zenginleştirme:** Temel bölüm bilgilerinin, yıllık kontenjan, yerleşen sayısı, puan ve sıralama gibi değerli istatistiklerle birleştirilerek zenginleştirilmesi.
*   **İlişkisel Veri Modellemesi (Normalleştirme):** Veri tekrarını önlemek, bütünlüğü sağlamak ve verimli sorgulara olanak tanımak amacıyla tüm verinin birbiriyle ilişkili tablolara ayrılarak normalize edilmesi.

## 📂 Repository Yapısı

```bash
data/
  ├── raw/                  # Temizlenmiş, normalize edilmemiş veriler
  ├── processed/            # Normalize edilmiş, ilişkisel veriler
  └── all_in_one_denormalized.csv   # Analiz için birleştirilmiş tek dosya
scripts/
  ├── process_raw_data.py   # Temizlenmiş verileri normalize eden betik
  └── build_all_in_one_denormalized.py # Normalize verileri birleştiren betik
cleaning_notes.md           # İlk aşama veri temizleme sürecinin detayları
README.md
```

## 🔍 Veri Kaynakları ve Gelecek Vizyonu

#### Mevcut Durum (2019-2025)
*   **2019–2024 yılları:** Tüm istatistikler (puan, sıralama, kontenjan vb.) YÖK Atlas üzerinden çekilmiştir.
*   **2025 yılı:** YÖK Atlas henüz 2025 verilerini yayınlamadığı için, bu yıla ait bölümler yalnızca ÖSYM kılavuzundan alınmıştır ve istatistik verileri boştur.

#### Gelecek Vizyonu ve Eklenecek Veriler
Bu veri seti, yaşayan ve sürekli gelişen bir projedir. Hedefim, Türkiye'deki en kapsamlı yükseköğretim veri setlerinden birini oluşturmaktır. Gelecek güncellemelerde YÖK Atlas'tan aşağıdaki verilerin de eklenmesi planlanmaktadır:
*   Yerleşenlerin Geldikleri Coğrafi Bölgeler ve İller
*   Yerleşenlerin Mezun Oldukları Lise Tipleri ve Alanları
*   Yerleşenlerin YKS Net Ortalamaları
*   Yerleşenlerin Tercih Eğilimleri (Ortalama kaçıncı tercihlerine yerleştikleri vb.)


## 📊 Veri Modeli ve Dosyaların İçeriği

`processed/` klasöründeki veriler, bilgi tekrarını önlemek ve veriyi daha düzenli hale getirmek için birden fazla dosyaya ayrılmıştır. Bu yapı sayesinde, örneğin "Boğaziçi Üniversitesi" ismi binlerce kez tekrarlanmak yerine tek bir yerde tutulur. Model, iki ana tablo ve onları zenginleştiren yardımcı tablolardan oluşur.

### 1. Ana Tablolar (Verinin Kalbi)

Analizlerinizin büyük ihtimalle başlayacağı iki temel tablo bunlardır:

*   **`department_stats.csv` (Yıllık Performans Verileri)**
    *   **Her satırı ne anlama geliyor?** Bir bölümün, belirli bir yıldaki performansını (kontenjan, yerleşen, sıralama vb.) gösterir.
    *   **Önemli Sütunlar:** `program_code`, `year`, `total_quota`, `total_enrolled`, `final_rank_012`, `initial_placement_rate`, `not_registered`, `additional_placement`, `avg_obp_012`, `avg_obp_018`.

*   **`departments_normalized.csv` (Bölümlerin Sabit Bilgileri)**
    *   **Her satırı ne anlama geliyor?** Bir bölümün zamanla değişmeyen temel özelliklerini (hangi üniversiteye ve fakülteye ait olduğu, puan türü vb.) içerir.
    *   **Amacı:** Diğer tüm açıklayıcı tablolara bir köprü görevi görür.
    *   **Önemli Sütunlar:** `program_code`, `university_id`, `department_name_id`, `faculty_name_id`, `score_type_id`.

### 2. Açıklayıcı "Lookup" Tabloları

Bu tablolar, ana tablolardaki kimlik numaralarını (`..._id`) herkesin anlayabileceği metinlere çevirir.

*   `department_names.csv`: Bölüm ID'lerini isimlere çevirir (Örn: `1` → `"Bilgisayar Mühendisliği"`).
*   `faculty_names.csv`: Fakülte ID'lerini isimlere çevirir (Örn: `5` → `"Mühendislik Fakültesi"`).
*   `universities_normalized.csv`: Üniversite ID'lerini üniversite bilgilerine çevirir.
*   `university_cities.csv`: Şehir ID'lerini şehir isimlerine çevirir (Örn: `34` → `"İSTANBUL"`).
*   `university_types.csv`: Üniversite türü ID'lerini tür isimlerine çevirir (Örn: `1` → `"devlet"`).
*   `score_types.csv`: Puan türü ID'lerini isimlerine çevirir (Örn: `2` → `"SAY"`).
*   `scholarship_types.csv`: Burs türü ID'lerini isimlerine çevirir (Örn: `3` → `"%50 İndirimli"`).
*   `tags.csv`: Etiket ID'lerini isimlerine çevirir (Örn: `24` → `"İngilizce"`).

### 3. İlişki Kuran Köprü Tabloları

Bazı bilgileri basitçe bağlamak mümkün değildir. Örneğin, bir bölümün birden fazla etiketi olabilir. Bu köprü tabloları, bu tür karmaşık ilişkileri yönetir.

*   **`department_tags.csv`**
    *   **Amacı:** Bir bölümün birden fazla etikete sahip olabilmesini sağlar. Bu dosya sayesinde bir bölüm hem `"İngilizce"` hem de `"Burslu"` olarak işaretlenebilir.
    *   **Yapısı:** Her satırı, bir `program_code` ile bir `tag_id`'yi birbirine bağlar.

---
#### Tabloların Birbiriyle İlişkisi (Özet)
```
// Merkezdeki Performans Verileri
department_stats.csv (program_code, year)

// Performans verilerini açıklayan sabit bilgiler
└── departments_normalized.csv (program_code)
    ├── universities_normalized.csv (university_id)
    │   ├── university_cities.csv (university_city_id)
    │   └── university_types.csv (university_type_id)
    ├── department_names.csv (department_name_id)
    ├── faculty_names.csv (faculty_name_id)
    ├── score_types.csv (score_type_id)
    ├── scholarship_types.csv (scholarship_type_id)
    // Bir bölümün birden fazla etiketi olabileceği için köprü tablo kullanılır
    └── department_tags.csv (program_code -> tag_id)
        └── tags.csv (tag_id)
```
Tüm veri temizleme ve dönüşüm süreçlerinin teknik detayları için: **[CLEANING_NOTES.md](CLEANING_NOTES.md)**

## 🐍 Kullanım Örnekleri (Python & Pandas)

Bu bölümde, veri setinin iki farklı formatının nasıl kullanılacağına dair pratik örnekler bulunmaktadır.

### Örnek 1: Hızlı Analiz (`all_in_one_denormalized.csv` ile)
Bu birleştirilmiş dosya, `join` işlemi gerektirmediği için hızlı keşifsel veri analizi (EDA) ve filtreleme işlemleri için idealdir.

```python
import pandas as pd

# 1. Tek ve büyük CSV dosyasını yükle
df = pd.read_csv('data/all_in_one_denormalized.csv')

# 2. Çoklu koşullarla filtreleme: 
#    2024 yılında, İstanbul'daki vakıf üniversitelerinin 
#    Bilgisayar Mühendisliği bölümlerini bulalım.
conditions = (
    (df['year'] == 2024) &
    (df['city'] == 'İSTANBUL') &
    (df['university_type'] == 'vakif') &
    (df['department_name'] == 'Bilgisayar Mühendisliği')
)

result_df = df.loc[conditions]

# 3. İlgili sütunları seç ve göster
print(result_df[['university_name', 'scholarship_type', 'total_quota', "total_enrolled"]])
```

### Örnek 2: İlişkisel Sorgu (Normalize Dosyalarla)
`processed/` klasöründeki normalize edilmiş yapı, daha karmaşık ve esnek sorgular için uygundur. Bu örnekte, ID'leri kullanarak farklı tabloları mantıksal olarak birbirine bağlayacağız.

```python
import pandas as pd

# 1. Gerekli tabloları yükle
stats = pd.read_csv('data/processed/department_stats.csv')
depts = pd.read_csv('data/processed/departments_normalized.csv')
dept_names = pd.read_csv('data/processed/department_names.csv')
universities = pd.read_csv('data/processed/universities_normalized.csv')

# 2. İlgili ID'leri güvenli bir şekilde bul
#    Boğaziçi Üniversitesi'nin ID'sini al
uni_name = "BOĞAZİÇİ ÜNİVERSİTESİ"
boun_id = universities.loc[universities['university_name'] == uni_name, 'university_id'].iloc[0]

#    Bilgisayar Mühendisliği bölümünün ID'sini al
dept_name = "Bilgisayar Mühendisliği"
cmpe_id = dept_names.loc[dept_names['department_name'] == dept_name, 'department_name_id'].iloc[0]

# 3. Bu ID'leri kullanarak ilgili program kodunu bul
program_conditions = (
    (depts['university_id'] == boun_id) &
    (depts['department_name_id'] == cmpe_id)
)
program_code = depts.loc[program_conditions, 'program_code'].iloc[0]

# 4. Program koduna göre istatistikleri filtrele ve yıllara göre sırala
boun_cmpe_stats = stats.loc[stats['program_code'] == program_code].sort_values('year')

# 5. Sonucu göster: Yıllara göre sıralama değişimi
print(boun_cmpe_stats[['year', 'total_quota', 'final_rank_012']])
```

## 💡 Veri Setiyle Yapılabilecek Analizler

Bu veri seti, hem veri bilimine yeni başlayanlar için alıştırma yapabilecekleri hem de deneyimli analistlerin derinlemesine çalışmalar yürütebileceği zengin bir kaynaktır.

#### Yeni Başlayanlar İçin Analiz Alıştırmaları
*   **Keşifsel Veri Analizi:** 2024 yılında SAY puan türünde en yüksek sıralama ile öğrenci alan ilk 20 bölüm hangileridir?
*   **Filtreleme ve Gruplama:** İstanbul'daki vakıf üniversitelerinde bulunan "Bilgisayar Mühendisliği" bölümlerinin tam burslu kontenjan sayılarını karşılaştırın.
*   **Basit Trendler:** Ankara'daki devlet üniversitelerinde Tıp fakültesi kontenjanları son 5 yılda nasıl değişti?
*   **Görselleştirme:** Türkiye genelinde üniversite türlerinin (Devlet, Vakıf, KKTC) dağılımını bir pasta grafiği ile gösterin.

#### İleri Seviye ve Gerçek Dünya Analizleri
*   **Rekabet Analizi:** Belirli bir bölümün (örneğin Tıp) giriş sıralamaları (`final_rank_012`) yıllar içinde nasıl bir değişim gösterdi? Hangi üniversiteler daha rekabetçi hale geliyor?
*   **Kontenjan ve Doluluk Oranı Analizi:** Üniversitelerin kontenjan planlaması ne kadar başarılı? Hangi bölümlerin doluluk oranları (`total_enrolled` / `total_quota`) sürekli yüksek/düşük seyrediyor?
*   **Cinsiyet Dağılımı Trendleri:** Mühendislik gibi alanlarda kadın öğrenci oranı (`female` / `total_enrolled`) yıllar içinde artıyor mu? Bu oran üniversite tipine (devlet/vakıf) veya şehre göre farklılık gösteriyor mu?
*   **Burs Stratejileri:** Vakıf üniversitelerinde `%100 Burslu` programların giriş sıralamaları ile `Ücretli` programlar arasındaki makas açılıyor mu, daralıyor mu?
*   **Tahminleme Modelleri:** Bir bölümün geçmiş yıllardaki sıralama ve doluluk oranlarına bakarak bir sonraki yılki performansını tahmin eden bir makine öğrenmesi modeli geliştirin.

## 🌐 İlgili Proje: sinavizcisi.com

Bu veri seti yalnızca akademik kullanım için değil, aynı zamanda öğrencilerin tercih süreçlerini kolaylaştırmak amacıyla geliştirdiğim [sinavizcisi.com](https://sinavizcisi.com) platformunda da aktif olarak kullanılmaktadır. Sitede, veriler üzerine geliştirdiğim yapay zekâ tabanlı analizler sayesinde öğrenciler kendilerine en uygun bölümleri ve üniversiteleri keşfedebilmektedir.

## 🤝 Katkıda Bulunma
*   Eksik veriler, iyileştirme önerileri ve yeni alanlar için `Issue` açabilirsiniz.

## 📜 Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır. Veriler kamuya açık kaynaklardan (YÖK Atlas, ÖSYM) alınmış olup yalnızca araştırma ve eğitim amaçlı paylaşılmaktadır.
