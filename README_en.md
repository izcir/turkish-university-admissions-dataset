# Turkey University Department Data & Statistics (2019-2024)

🌐 [English](README_en.md) | [Türkçe](README.md)

This repository contains university department data for the years 2019–2024, obtained from official sources like YÖK Atlas and ÖSYM using the [YokAPI](https://github.com/izcir/YokAPI/) Python-based scraper. The data has been prepared for analysis through a two-stage process: **Cleaning** and **Normalization**.

This dataset also serves as the core database for my website, [sinavizcisi.com](https://sinavizcisi.com), a platform designed to facilitate the university selection process with AI-powered analyses.

### Dataset at a Glance

*   **Covered Period:** 2019-2024 (Total of 6 years) *(2025 statistics will be added upon release)*
*   **Total Records:** 128,352 (Rows representing the core stats of each program in each year)
*   **Unique Programs:** 32,505 (`program_code`)
*   **Unique Entities:** 235 Universities, 733 Department Names, 1,131 Faculties


> **Important Note:** The data in this repository has undergone a two-stage process. First, raw data was cleaned according to the steps detailed in **[`CLEANING_NOTES.md`](https://github.com/izcir/turkish-university-admissions-dataset/blob/main/other_readme_files/cleaning_notes.md)**. The files in `data/raw/` are the output of this stage. Second, scripts in the `scripts/` folder transform this data into a normalized, relational structure under `data/processed/` and finally create the `all_in_one_denormalized.csv` file. For quick analyses, the `all_in_one_denormalized.csv` file is convenient. For more in-depth and flexible queries, the normalized structure in `data/processed/`, which prevents data redundancy, is recommended.

## 📌 Purpose and Value of the Dataset

While YÖK Atlas is the primary official source for higher education data in Turkey, it presents several challenges for data users:

*   **Inconsistencies Across Years:** Department names, program codes (IDs), and even university names can change over time, making time-series analysis and comparisons nearly impossible.
*   **Missing and Scattered Information:** There can be gaps in data for certain years, and critical metrics like quotas, scores, and ranks are often spread across different pages.

The purpose of this dataset is to solve all these problems by creating a **clean, reliable, and ready-to-use** resource for researchers, developers, and students. The key steps taken to achieve this are:

*   **Systematic Data Collection:** Regularly and systematically scraping public data from YÖK Atlas and ÖSYM using tools like `YokAPI`.
*   **Comprehensive Data Cleaning and Standardization:** Meticulously addressing identified ID conflicts, naming inconsistencies, format errors, and missing information to standardize the data.
*   **Data Enrichment:** Combining core department information with valuable yearly statistics like quotas, enrollment numbers, scores, and ranks.
*   **Relational Data Modeling (Normalization):** Structuring the data into interconnected tables to prevent data redundancy, ensure integrity, and enable efficient querying.

## 📂 Repository Structure

```bash
data/
  ├── raw/                  # Cleaned, non-normalized data
  ├── processed/            # Normalized, relational data
  └── all_in_one_denormalized.csv   # Single flattened file for analysis
scripts/
  ├── process_raw_data.py   # Script to normalize the cleaned data
  └── build_all_in_one_denormalized.py # Script to build the flattened file
CLEANING_NOTES.md           # Details of the initial data cleaning process
README.md
```

## 🔍 Data Sources and Future Vision

#### Current Status (2019-2025)
*   **2019–2024:** All statistics (scores, ranks, quotas, etc.) have been scraped from YÖK Atlas.
*   **2025:** As YÖK Atlas has not yet released the 2025 statistics, the department data for this year is sourced only from the ÖSYM guide, and thus statistical columns are empty.

#### Future Vision and Planned Additions
This is a living dataset that will be continuously improved. My goal is to create one of the most comprehensive higher education datasets for Turkey by incorporating other valuable data from YÖK Atlas. Planned future additions include:
*   Geographic Origins of Enrolled Students (Regions and Cities)
*   High School Types and Fields of Study of Graduates
*   Average YKS Exam Net Scores of Enrolled Students
*   Preference Trends of Enrolled Students (e.g., average choice rank)

## 📊 Data Model and Schema

The data in the `processed/` folder is structured into multiple files to prevent redundancy and organize the information logically. For instance, the name "Boğaziçi Üniversitesi" is stored once instead of being repeated thousands of times. The model consists of two core tables and several auxiliary tables that enrich them.

### 1. Fact Tables
These tables contain the core, measurable events or states in the dataset.

| File Name | Granularity (Each Row is...) | Description & Key Columns |
| :--- | :--- | :--- |
| **`department_stats.csv`** | The performance of one **program** in one **year**. | Contains fundamental metrics like quota, enrollment, and admission rank. This is the starting point for most analyses.<br>*(Columns: `program_code`, `year`, `total_quota`, `total_enrolled`, `final_rank_012`)* |
| **`department_avg_net_stats.csv`** | The average net score for one **lesson** in one **program** in one **year**. | Contains the academic profile of enrolled students on a per-subject basis.<br>*(Columns: `program_code`, `year`, `lesson_id`, `coefficient_type`, `average_net`)* |

### 2. Dimension and Lookup Tables
These tables contain the descriptive information that corresponds to the IDs in the fact tables.

| File Name | Purpose | Example |
| :--- | :--- | :--- |
| **`departments_normalized.csv`** | Stores time-invariant attributes of each program and acts as a bridge to other dimensions. | `101490226` → `university_id: 101`, `department_name_id: 25`, ... |
| **`universities_normalized.csv`** | Contains core information about universities (name, type, city). | `101` → "BOĞAZİÇİ ÜNİVERSİTESİ", `type_id: 1`, `city_id: 34` |
| **`lessons.csv`** | Contains information about exam subjects (name, exam type, question count). | `1` → "TYT Temel Matematik", "TYT", 40 |
| **`department_names.csv`** | Translates department IDs to names. | `25` → "Bilgisayar Mühendisliği" |
| *... (other lookup tables)* | | |

### 3. Bridge Tables
These tables manage "many-to-many" relationships. For example, a single department can have multiple tags.

| File Name | Purpose |
| :--- | :--- |
| **`department_tags.csv`** | Links `program_code` to `tag_id`, allowing one program to have multiple tags. |


---
#### Schema Relationship Summary
```
// Core Performance Data
department_stats.csv (program_code, year)

// Static info describing the performance data
└── departments_normalized.csv (program_code)
    ├── universities_normalized.csv (university_id)
    │   ├── university_cities.csv (university_city_id)
    │   └── university_types.csv (university_type_id)
    ├── department_names.csv (department_name_id)
    ├── faculty_names.csv (faculty_name_id)
    ├── score_types.csv (score_type_id)
    ├── scholarship_types.csv (scholarship_type_id)
    // A bridge table is used as a program can have multiple tags
    └── department_tags.csv (program_code -> tag_id)
        └── tags.csv (tag_id)
```
For full technical details on the data cleaning and transformation process, see: **[CLEANING_NOTES.md](https://github.com/izcir/turkish-university-admissions-dataset/blob/main/other_readme_files/cleaning_notes_en.md)**

## 🐍 Usage Examples (Python & Pandas)

This section provides practical examples of how to use both formats of the dataset.

### Example 1: Quick Analysis (with `all_in_one_denormalized.csv`)
This flattened file is ideal for quick exploratory data analysis (EDA) and filtering, as it doesn't require any join operations.

```python
import pandas as pd

# 1. Load the single, large CSV file
df = pd.read_csv('data/all_in_one_denormalized.csv')

# 2. Filter with multiple conditions: 
#    Let's find Computer Engineering departments at private universities 
#    in Istanbul for the year 2024.
conditions = (
    (df['year'] == 2024) &
    (df['city'] == 'İSTANBUL') &
    (df['university_type'] == 'vakif') &
    (df['department_name'] == 'Bilgisayar Mühendisliği')
)

result_df = df.loc[conditions]

# 3. Select and display relevant columns
print(result_df[['university_name', 'scholarship_type', 'total_quota', "total_enrolled"]])
```

### Example 2: Relational Query (with Normalized Files)
The normalized structure in the `processed/` folder is suitable for more complex and flexible queries. In this example, we will logically connect different tables using their IDs.

```python
import pandas as pd

# 1. Load the necessary tables
stats = pd.read_csv('data/processed/department_stats.csv')
depts = pd.read_csv('data/processed/departments_normalized.csv')
dept_names = pd.read_csv('data/processed/department_names.csv')
universities = pd.read_csv('data/processed/universities_normalized.csv')

# 2. Safely find the relevant IDs
#    Get the ID for Boğaziçi Üniversitesi
uni_name = "BOĞAZİÇİ ÜNİVERSİTESİ"
boun_id = universities.loc[universities['university_name'] == uni_name, 'university_id'].iloc[0]

#    Get the ID for Bilgisayar Mühendisliği
dept_name = "Bilgisayar Mühendisliği"
cmpe_id = dept_names.loc[dept_names['department_name'] == dept_name, 'department_name_id'].iloc[0]

# 3. Use these IDs to find the corresponding program code
program_conditions = (
    (depts['university_id'] == boun_id) &
    (depts['department_name_id'] == cmpe_id)
)
program_code = depts.loc[program_conditions, 'program_code'].iloc[0]

# 4. Filter the stats by program code and sort by year
boun_cmpe_stats = stats.loc[stats['program_code'] == program_code].sort_values('year')

# 5. Show the result: rank changes over the years
print(boun_cmpe_stats[['year', 'total_quota', 'final_rank_012']])
```

## 💡 Analysis Ideas with This Dataset

This dataset is a rich resource for both beginners practicing their skills and experienced analysts conducting in-depth studies.

#### Analysis Exercises and Real-World Questions
*   **Exploratory Data Analysis:** What were the top 20 departments with the highest admission ranks for the "SAY" score type in 2024?
*   **Filtering and Grouping:** Compare the total quotas for full-scholarship ("Burslu") "Bilgisayar Mühendisliği" programs at private ("vakif") universities in "İSTANBUL".
*   **Simple Trends:** How have the quotas for "Tıp" faculties at public ("devlet") universities in "ANKARA" changed over the last 5 years?
*   **Visualization:** Create a pie chart showing the distribution of university types ("Devlet", "Vakıf", "KKTC") across Turkey.
*   **Competition Analysis:** How have admission ranks (`final_rank_012`) for a specific major (e.g., "Tıp") evolved over time? Which universities are becoming more competitive?
*   **Quota and Occupancy Rate Analysis:** How successful is universities' quota planning? Which departments consistently have high/low occupancy rates (`total_enrolled` / `total_quota`)?
*   **Gender Distribution Trends:** Is the ratio of female students (`female` / `total_enrolled`) in engineering fields increasing over time? How does this ratio vary by university type ("devlet"/"vakif") or city?
*   **Scholarship Strategies:** Is the gap in admission ranks between "100% Burslu" and "Ücretli" programs at private universities widening or narrowing?
*   **Predictive Modeling:** Develop a machine learning model to predict a department's future performance based on its historical rank and quota data.
*   **Academic Profile Comparison:** Is there a significant difference in the AYT Math and Physics net averages between students of the same major at different universities (e.g., METU vs. ITU Computer Eng.)?
*   **Correlation between Admission Rank and Net Scores:** What is the correlation between a department's `final_rank_012` (admission rank) and the TYT Turkish or AYT Math net averages of its students? Which subject's net score is a better predictor of the admission rank?
*   **Longitudinal Improvement:** Are the TYT Science net averages for students in a specific major (e.g., Medicine) increasing or decreasing over the years?
*   **Major Characteristic Analysis:** What is the average TYT Math score for students enrolled in Social Science ("SÖZ") majors, versus the average TYT Social Sciences score for students in STEM ("SAY") majors?

## 🌐 Related Project: sinavizcisi.com

This dataset is not just for academic use; it is actively used in production on [sinavizcisi.com](https://sinavizcisi.com), a platform I developed to help students with their university selection process. On the site, AI-powered analyses built upon this data help students discover the most suitable departments, university opportunities, and historical trends.

## 🤝 Contributing
*   Feel free to open an `Issue` for missing data, improvement suggestions, or new feature ideas.

## 📜 License
This project is licensed under the [MIT License](LICENSE). The data is sourced from public resources (YÖK Atlas, ÖSYM) and is shared for research and educational purposes only.
