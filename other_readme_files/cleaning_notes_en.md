# Data Cleaning and Standardization Process - Detailed Notes

This document provides technical details on the cleaning, standardization, and consolidation processes applied to the raw undergraduate and associate degree department data scraped from YÖK Atlas.

## 1. Tag Standardization

The parenthetical information appended to department names (referred to as "tags") initially contained over 100 different unique values. These included city/district names, meaningless abbreviations (e.g., `Bk. ...`), and redundant information. Only the tags deemed meaningful for analysis were filtered and standardized as follows.

### 1.1. Selected Tags for Undergraduate Programs (Lisans)

```
- German, French, Chinese
- 50% Scholarship, 75% Scholarship, 25% Scholarship, Full Scholarship, Paid
- TRNC National, M.T.O.K. (Special Quota for Vocational High Schools)
- Polish, Bulgarian, Russian, Armenian, Spanish, Arabic, Italian, Persian, Korean
- On behalf of the Ministry of National Defence, On behalf of the Ministry of Interior
- Female Only, Male Only
- Evening Education (İÖ)
- Open Education, Distance Learning
```
*Note: Variations such as `KKTC Uyruklu` and `KKTC UYRUKLU` (TRNC National) were merged into a single standardized tag.*

### 1.2. Selected Tags for Associate Degree Programs (Önlisans)

```
- 75% Scholarship, 25% Scholarship, 50% Scholarship, Full Scholarship, Paid
- On behalf of the Ministry of Interior, On behalf of the Ministry of National Defence
- Distance Learning, Open Education
- Arabic, Russian, English, Spanish
- Evening Education (İÖ)
- Female Only, Male Only
- TRNC National
```
*Note: Case differences like `%25 İNDİRİMLİ` and `%25 İndirimli`, and variations like `İÖ` and `İö` (Evening Education), were standardized.*

## 2. Management of ID and Department Name Inconsistencies

### 2.1. Undergraduate and Associate Degree ID Conflicts

The following program IDs were used for undergraduate programs in 2022 but were reassigned to associate degree programs in 2023-2024. To ensure data integrity and retain the most current information, the **older (2022) undergraduate records for these IDs were deleted, while the newer (2023-2024) associate degree records were kept**.
- `202090382`, `202090389`, `202390269`, `109890188`

### 2.2. Departments with Completely Different Names Across Years

It was found that some program IDs were assigned to entirely unrelated departments in different years. This indicates that a department was closed and its ID was later repurposed. To avoid creating complex exceptions in the analysis, these IDs were **completely removed from the dataset**:
- `203851992`: (Assigned to both 'Aviation Electrical and Electronics' and 'Graphic Design')
- `107790346`: (Assigned to both 'Anthropology' and 'Sociology')
- `409610608`: (Assigned to both 'Public Relations and Advertising' and 'Fashion Design')

## 3. Handling Missing Data (A Special Case for `onlisans_2021`)

The `onlisans_2021` (Associate Degree 2021) data contained significant gaps:
- General information, such as the university name, was missing for approximately 300 departments. This information was backfilled using data from the 2020 and 2019 records for the same program IDs.
- For the following 30 program IDs, both the university and department name fields were completely empty. As these records compromised data integrity, they were **removed from the associate degree dataset**:
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
- As a side effect of this cleaning process, some records with a department name of `""` (empty string) remain in the main list. This is a known issue and does not affect current analyses.

## 4. Other Standardizations and Known Notes

### 4.1. University Name Standardization

Over the years, some universities have changed their names. To ensure consistency across the dataset, all records belonging to a university (including data from previous years) have been standardized to use its **most current name**. The former name of the university is preserved for reference in the `old_name` column of the `universities_normalized.csv` file.

### 4.2. Department Name Standardization

Minor spelling and formatting differences were identified in the names of the same department across different years (e.g., `İngiliz Dil Bilimi` vs. `İngiliz Dilbilimi`, `Kurgu-Ses ve Görüntü Yönetimi` vs. `Kurgu, Ses ve Görüntü Yönetimi`). To ensure consistency, all records for a given department have been standardized to use the name from the **most recent year**. This prevents the same department from appearing with different names in different years.