### **Turkish University Admissions & Stats (2019-2024)**
A comprehensive dataset of department quotas, placements, scores, and rankings from Turkey's Higher Education Council (YÖK). Ideal for analyzing educational trends and building predictive models.

For a complete overview of the data collection, cleaning, and standardization methodology, please refer to the official [GitHub repository](https://github.com/izcir/turkish-university-admissions-dataset).

> **(TR) Bu veri seti, Türkiye'deki üniversitelerin 2019-2024 arası kontenjan, yerleşen sayısı, taban puan ve sıralama gibi detaylı istatistiklerini içerir. Ana dosya olan `01_university_admissions_turkey_2019_2024.csv`, tüm bu verilerin analiz için birleştirilmiş pratik halidir. Veriyi daha iyi anlamak ve analizlere başlamak için Türkçe hazırlanan başlangıç notebook'larına göz atabilirsiniz.**

### **Starter Notebooks**
We have prepared two notebooks to help you get started:
* **[EDA] Exploring Turkish University Admissions:** A starter guide for basic exploratory data analysis, visualizations, and trend discovery.
* **Data Quality & Inconsistencies Analysis:** A crucial analysis of the dataset's known issues and limitations. **It is highly recommended to review this notebook before conducting in-depth analysis.**

### **Files**
* **`01_university_admissions_turkey_2019_2024.csv`**: The main, analysis-ready file. **Recommended for most users.**
* **Individual CSV Files (`universities_normalized.csv`, `department_stats.csv`, etc.)**: A collection of all the individual relational tables used to build the main file. These are ideal for advanced users or for running the starter notebooks.
* **Detailed Preference Files (`department_preference_ranks.csv` & `department_placed_preference_ranks.csv`):** For advanced preference analysis, these files provide row-level detail on the exact preference ranks of all students and of those who were placed. This granular data is **not** aggregated in the main `..._2024.csv` file and is **not** used in the starter notebooks.

### **Source & Methodology**
The data is sourced from Turkey's Higher Education Council (YÖK) Atlas and ÖSYM. The data was collected programmatically via the [YokAPI Python package](https://github.com/izcir/YokAPI). Key decisions regarding data standardization are documented in the [`cleaning_notes.md`](https://github.com/izcir/turkish-university-admissions-dataset/blob/main/other_readme_files/cleaning_notes.md) file within the GitHub repository.

---

### **Data Dictionary / Veri Sözlüğü for `01_university_admissions_turkey_2019_2024.csv`**

| Column Name / Sütun Adı | Description / Açıklama |
|---|---|
| `program_code` | Unique identifier for each department program. / *Her bir bölüm programı için benzersiz kod.* |
| `year` | The year the data pertains to. / *Verinin ait olduğu yıl.* |
| `university_name` | Name of the university. / *Üniversitenin adı.* |
| `city` | The city where the university campus is located. / *Üniversite kampüsünün bulunduğu şehir.* |
| `university_type` | Type of the university (State, Foundation, etc.). / *Üniversitenin türü (Devlet, Vakıf, vb.).* |
| `department_name` | Name of the department/program. / *Bölümün/programın adı.* |
| `faculty_name` | Name of the faculty. / *Fakültenin adı.* |
| `score_type` | The exam score type required for admission (SAY, EA, SÖZ, DİL). / *Bölüme girmek için gereken puan türü.* |
| `scholarship_type` | Scholarship status (Full-Paid, Full Scholarship, etc.). / *Bursluluk durumu (Ücretli, Tam Burslu, vb.).* |
| `is_undergraduate`| Boolean flag; `True` for undergraduate (4+ years), `False` for associate (2 years). / *Programın lisans (True) mı yoksa ön lisans (False) mı olduğunu belirten bayrak.* |
| `all_tags` | A collection of tags for the program (e.g., English, Evening Education). / *Bölümle ilişkili etiketler (örn: İngilizce, İkinci Öğretim).* |
| `total_quota` | The total number of students the department planned to accept. / *Bölümün almayı planladığı toplam öğrenci sayısı.* |
| `total_enrolled` | The total number of students who enrolled. / *Bölüme yerleşen toplam öğrenci sayısı.* |
| `male` | Number of enrolled male students. / *Yerleşen erkek öğrenci sayısı.* |
| `female` | Number of enrolled female students. / *Yerleşen kadın öğrenci sayısı.* |
| `final_score_012` | The minimum score of the last student placed (0.12 coefficient). / *Yerleşen son öğrencinin 0.12 katsayılı taban puanı.* |
| `final_rank_012` | The rank of the last student placed (0.12 coefficient). / *Yerleşen son öğrencinin 0.12 katsayılı taban sıralaması.* |
| `final_score_018` | Historical minimum score of the last student placed (0.18 coefficient). / *Yerleşen son öğrencinin 0.18 katsayılı taban puanı (eski sistem).* |
| `final_rank_018` | Historical rank of the last student placed (0.18 coefficient). / *Yerleşen son öğrencinin 0.18 katsayılı taban sıralaması (eski sistem).* |
| `initial_placement_rate` | The percentage of the quota filled after the initial placement. / *İlk yerleştirme sonunda kontenjanın doluluk oranı.* |
| `not_registered` | Number of placed students who did not register. / *Yerleştiği halde kayıt yaptırmayan öğrenci sayısı.* |
| `additional_placement` | Number of students placed via additional placements. / *Ek yerleştirmelerle yerleşen öğrenci sayısı.* |
| `avg_obp_012` | Average High School GPA (OBP) of enrolled students (0.12 coefficient). / *Yerleşen öğrencilerin Ortalama Ortaöğretim Başarı Puanı (0.12 katsayılı).* |
| `avg_obp_018` | Historical Average OBP of enrolled students (0.18 coefficient). / *Yerleşen öğrencilerin Ortalama OBP'si (0.18 katsayılı, eski sistem).* |
| `total_preferences`| Total number of times the program was listed in students' preference lists. / *Programın toplam tercih edilme sayısı.* |
| `demand_per_quota`| A calculated metric: `total_preferences` / `total_quota`. / *Hesaplanmış metrik: Toplam tercih sayısı / Toplam kontenjan.* |
| `avg_preference_rank`| The average rank of this program in all preference lists it appeared in. / *Bu bölümü tercih eden tüm öğrencilerin ortalama tercih sırası.* |
| `top_1_pref_count`| Number of students who listed this program as their 1st choice. / *Bu bölümü 1. sırada tercih eden öğrenci sayısı.* |
| `top_3_pref_count`| Number of students who listed this program in their top 3 choices. / *Bu bölümü ilk 3 sırada tercih eden öğrenci sayısı.* |
| `top_9_pref_count`| Number of students who listed this program in their top 9 choices. / *Bu bölümü ilk 9 sırada tercih eden öğrenci sayısı.* |
| `placed_count` | Total number of students placed in the program. / *Programa yerleşen toplam öğrenci sayısı.* |
| `placed_pref_rank_avg`| Average preference rank among students who were placed in this program. / *Bu programa yerleşen öğrencilerin ortalama tercih sırası.* |
| `placed_top_1_pref_count`| Number of placed students who listed this program as their 1st choice. / *Bu programa yerleşen ve 1. sırada tercih eden öğrenci sayısı.* |
| `placed_top_3_pref_count`| Number of placed students who listed this program in their top 3 choices. / *Bu programa yerleşen ve ilk 3'te tercih eden öğrenci sayısı.* |
| `placed_top_10_pref_count`| Number of placed students who listed this program in their top 10 choices. / *Bu programa yerleşen ve ilk 10'da tercih eden öğrenci sayısı.* |
| `placed_pref_uni_devlet_count`| Among placed students, the total number of State university preferences in their lists. / *Yerleşen öğrencilerin tercih listelerindeki Devlet üniversitesi sayısı.* |
| `placed_pref_uni_vakif_count`| Among placed students, the total number of Foundation university preferences in their lists. / *Yerleşen öğrencilerin tercih listelerindeki Vakıf üniversitesi sayısı.* |
| `placed_pref_uni_kktc_count`| Among placed students, the total number of TRNC university preferences in their lists. / *Yerleşen öğrencilerin tercih listelerindeki KKTC üniversitesi sayısı.* |
| `placed_pref_uni_yurt_disi_count`| Among placed students, the total number of International university preferences in their lists. / *Yerleşen öğrencilerin tercih listelerindeki Yurtdışı üniversitesi sayısı.* |