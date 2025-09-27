# Turkey University Departments & Statistics (2019-2024)

### Context (Why this Dataset?)

For anyone looking to analyze university admissions and educational trends in Turkey, the official "YÖK Atlas" portal is the most valuable resource. However, the data is presented in a raw, unstructured format, making it unsuitable for direct analysis. Longitudinal inconsistencies, missing data, and formats ill-suited for analysis pose significant challenges for anyone wanting to work with this valuable information.

This dataset was created to solve these problems. The data, scraped from YÖK Atlas and ÖSYM (official examination body) using the [YokAPI](https://github.com/izcir/YokAPI/) scraper, is presented here after a rigorous two-stage process: **Initial Cleaning** and **Normalization**.

My goal is to provide a comprehensive and reliable dataset that serves as both **a rich playground for beginners to practice their skills** and **a powerful resource for experienced analysts to conduct in-depth, real-world studies**.

### Dataset at a Glance

*   **Time Range:** 2019-2024 (6 Years) *(2025 data will be added upon release)*
*   **Total Rows:** **128,352** records in the `all_in_one_denormalized.csv` file.
*   **Unique Counts:**
    *   **32,505** unique Programs (`program_code`)
    *   **235** unique Universities
    *   **733** unique Department Names
    *   **27** unique Tags
*   **Most Common Tags:** `Burslu` (5.6k+ programs), `%50 İndirimli` (5.4k+ programs), `İngilizce` (5.2k+ programs)

### Content (What's in the Dataset?)

This dataset is offered in two formats to cater to different user needs:

#### 1. `all_in_one_denormalized.csv` (Recommended for a Quick Start)
This file is a **single, flattened (denormalized) table that joins all the information together.** Each row represents a single department's complete information and statistics for a specific year. It's ideal for beginners, for quick exploratory data analysis (EDA), or for anyone preparing data for machine learning models.
**If you're not sure where to start, use this file.**

**Example Row Structure:**
| program_code | year | university_name | city | department_name | score_type | all_tags | total_quota | final_rank_012 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 106510077 | 2024 | ABDULLAH GÜL ÜNİVERSİTESİ | KAYSERİ | Bilgisayar Mühendisliği | SAY | İngilizce | 82 | 46890 |

#### 2. `processed/` Folder (Relational / Normalized Data)
This folder contains multiple CSV files designed with a relational database schema in mind. It's suitable for advanced users who prioritize data integrity, want to perform complex SQL-like `join` operations, or plan to import the data into their own database. This structure is the "source of truth" from which the `all_in_one_denormalized.csv` file is generated.

**Core Tables:**
*   **`department_stats.csv`**: This is the **heart of the dataset**. It contains critical metrics for each program for each year, such as quota, number of enrolled students, gender distribution, and minimum admission scores and ranks.
*   **`departments_normalized.csv`**: Contains the time-invariant core information for each program (e.g., its department name, faculty, university, and score type).

> For full technical details on the data cleaning process and decisions made, please refer to the **[`CLEANING_NOTES.md` file in the project's GitHub repository](https://github.com/izcir/yok-atlas-veri-seti/blob/main/CLEANING_NOTES.md)**. <!-- UPDATE THE GITHUB LINK -->

### Usage Notes & Data Dictionary
*   **`program_code`**: Should be read as a `string` to preserve leading zeros.
*   **`final_rank_*`**: May contain nulls (`NaN`). You will need to handle these missing values in your analysis. In Pandas, you can convert these columns to a *nullable integer* type using `pd.to_numeric(df['col'], errors='coerce').astype('Int64')`.
*   **`all_tags`**: This is a comma-separated string containing multiple tags for a program. It can be converted to a list for analysis using the `split(',')` method.
*   **Faculty Names**: The `faculty_names.csv` file may contain entries with empty faculty names for some programs. This is due to missing faculty information in the source data.

### Future Vision & Planned Additions

This is a living dataset that will be continuously improved. My goal is to incorporate other valuable information from YÖK Atlas over time to create one of the most comprehensive higher education datasets for Turkey. Planned future additions include:

*   Geographic Origins of Enrolled Students (Regions and Cities)
*   High School Types and Fields of Study of Graduates
*   Average YKS Exam Net Scores of Enrolled Students
*   Preference Trends of Enrolled Students (e.g., average choice rank, most co-preferred programs)

These additions will enable much deeper socio-economic and strategic analyses.

### Inspiration (What Can You Do with This Dataset?)

This dataset is suitable for a wide range of analyses, from simple queries to complex machine learning models.

#### Starter Analyses for Beginners

*   **Exploratory Data Analysis (EDA):** What were the top 20 departments with the highest admission ranks for the "SAY" score type in 2024?
*   **Filtering and Grouping:** Compare the total quotas for `Burslu` "Bilgisayar Mühendisliği" programs at `vakif` universities in `İSTANBUL`.
*   **Simple Trends:** How have the quotas for `Tıp` faculties at `devlet` universities in `ANKARA` changed over the last 5 years?
*   **Visualization:** Create a pie chart showing the distribution of university types (`Devlet`, `Vakıf`, `KKTC`) across Turkey.
*   **Occupancy Rates:** Which associate degree programs had an occupancy rate below 80% in 2023?

#### Advanced & Real-World Analyses

*   **Competition and Popularity Analysis:** How has the admission rank (`final_rank_012`) for a specific major (e.g., "Yapay Zeka Mühendisliği") evolved over the years? Which universities are becoming more competitive in this field?
*   **Strategic Quota Planning:** What is the impact of universities' decisions to increase/decrease quotas on their occupancy rates and admission ranks? Which strategies appear more successful?
*   **Socio-Demographic Trends:** Is the ratio of female students (`female` / `total_enrolled`) in engineering fields increasing over time? How does this ratio vary by university type (`devlet`/`vakif`) or city?
*   **Private University Scholarship Strategies:** Is the gap in admission ranks between `"Burslu"` and `"Ücretli"` programs widening or narrowing over time? Which universities stand out with their scholarship programs?
*   **Identifying "Majors of the Future":** Identify majors that have been consistently introduced in recent years, have growing quotas, and maintain high occupancy rates.
*   **Predictive Modeling (Machine Learning):** Develop a regression model to predict a department's next-year admission rank (`final_rank_012`) based on its historical rank, quota, occupancy rate, and university characteristics.
*   **Clustering Analysis:** Group universities based on the diversity of their programs, score type weights, and competitiveness levels to discover profiles like "Teknoloji Odaklı Butik Üniversiteler" or "Kapsamlı Devlet Üniversiteler".