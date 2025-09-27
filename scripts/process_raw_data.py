import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def build_dimension(df: pd.DataFrame, column: str, id_col: str, value_col: str, out_filename: str) -> pd.DataFrame:
    """Generic dimension builder (dropna + unique + id assignment + save)."""
    values = df[column].dropna().drop_duplicates().reset_index(drop=True)
    dim = pd.DataFrame({
        id_col: range(1, len(values) + 1),
        value_col: values
    })
    dim.to_csv(os.path.join(PROCESSED_DIR, out_filename), index=False)
    return dim

def explode_multi(df: pd.DataFrame, code_col: str, multi_col: str, sep: str = ',') -> pd.DataFrame:
    tmp = df[[code_col, multi_col]].dropna().copy()
    tmp[multi_col] = tmp[multi_col].apply(lambda x: [v.strip() for v in str(x).split(sep)])
    return tmp.explode(multi_col)

def collect_unique_tokens(series: pd.Series, sep: str = ',') -> list:
    bag = set()
    for item in series.dropna():
        for token in str(item).split(sep):
            token = token.strip()
            if token:
                bag.add(token)
    return sorted(bag)

# --------------------------------------------------
# Main Processing
# --------------------------------------------------

def main():
    ensure_dir(PROCESSED_DIR)

    # Read raw data
    universities = pd.read_csv(os.path.join(RAW_DIR, "universities_raw.csv"))
    departments = pd.read_csv(os.path.join(RAW_DIR, "departments_raw_no2025.csv"))

    # --------------------------------------------------
    # Department & Faculty Name Dimensions
    # --------------------------------------------------
    department_names = departments['department_name'].drop_duplicates().reset_index(drop=True)
    faculty_names = departments['faculty_name'].drop_duplicates().reset_index(drop=True)

    department_names_df = pd.DataFrame({
        'department_name_id': range(1, len(department_names) + 1),
        'department_name': department_names
    })
    faculty_names_df = pd.DataFrame({
        'faculty_name_id': range(1, len(faculty_names) + 1),
        'faculty_name': faculty_names
    })

    department_names_df.to_csv(os.path.join(PROCESSED_DIR, "department_names.csv"), index=False)
    faculty_names_df.to_csv(os.path.join(PROCESSED_DIR, "faculty_names.csv"), index=False)

    departments_merged = departments.merge(department_names_df, on="department_name", how="left")
    departments_merged = departments_merged.merge(faculty_names_df, on="faculty_name", how="left")

    # --------------------------------------------------
    # Score & Scholarship Types
    # --------------------------------------------------
    score_types_df = build_dimension(
        departments_merged, 'score_type', 'score_type_id', 'score_type', 'score_types.csv'
    )
    scholarship_types_df = build_dimension(
        departments_merged, 'scholarship_type', 'scholarship_type_id', 'scholarship_type', 'scholarship_types.csv'
    )

    departments_merged = departments_merged.merge(score_types_df, on="score_type", how="left")
    departments_merged = departments_merged.merge(scholarship_types_df, on="scholarship_type", how="left")

    # --------------------------------------------------
    # Departments Normalized
    # --------------------------------------------------
    departments_final = departments_merged[[
        "program_code",
        "department_name_id",
        "faculty_name_id",
        "university_id",
        "score_type_id",
        "scholarship_type_id",
        "is_undergraduate",
        "years",
        "tags",
    ]]
    departments_final.to_csv(os.path.join(PROCESSED_DIR, "departments_normalized.csv"), index=False)

    # --------------------------------------------------
    # Years Dimension + Bridge Table
    # --------------------------------------------------
    unique_years = collect_unique_tokens(departments_merged['years'])
    years_df = pd.DataFrame({
        'year_id': range(1, len(unique_years) + 1),
        'year': unique_years
    })
    years_df.to_csv(os.path.join(PROCESSED_DIR, "years.csv"), index=False)

    departments_exploded_years = explode_multi(departments_merged, 'program_code', 'years')
    departments_exploded_years = departments_exploded_years.merge(years_df, left_on='years', right_on='year', how='left')
    department_years_df = departments_exploded_years[['program_code', 'year_id']].reset_index(drop=True)
    department_years_df.to_csv(os.path.join(PROCESSED_DIR, "department_years.csv"), index=False)

    # --------------------------------------------------
    # Tags Dimension + Bridge Table
    # --------------------------------------------------
    unique_tags = collect_unique_tokens(departments_merged['tags'])
    tags_df = pd.DataFrame({
        'tag_id': range(1, len(unique_tags) + 1),
        'tag': unique_tags
    })
    tags_df.to_csv(os.path.join(PROCESSED_DIR, "tags.csv"), index=False)

    departments_exploded_tags = explode_multi(departments_merged, 'program_code', 'tags')
    departments_exploded_tags = departments_exploded_tags.merge(tags_df, left_on='tags', right_on='tag', how='left')
    department_tags_df = departments_exploded_tags[['program_code', 'tag_id']].reset_index(drop=True)
    department_tags_df.to_csv(os.path.join(PROCESSED_DIR, "department_tags.csv"), index=False)

    # --------------------------------------------------
    # University Type & City Dimensions
    # --------------------------------------------------
    university_types_df = build_dimension(
        universities, 'university_type', 'university_type_id', 'university_type', 'university_types.csv'
    )
    university_cities_raw = universities['city'].drop_duplicates().reset_index(drop=True)
    university_cities_df = pd.DataFrame({
        'university_city_id': range(1, len(university_cities_raw) + 1),
        'city': university_cities_raw
    })
    university_cities_df.to_csv(os.path.join(PROCESSED_DIR, "university_cities.csv"), index=False)

    universities_merged = universities.merge(university_types_df, on="university_type", how="left")
    universities_merged = universities_merged.merge(university_cities_df, on="city", how="left")

    universities_final = universities_merged[[
        "university_id",
        "university_name",
        "old_name",
        "university_type_id",
        "university_city_id"
    ]]
    universities_final.to_csv(os.path.join(PROCESSED_DIR, "universities_normalized.csv"), index=False)


if __name__ == "__main__":  # Script entry point
    main()

