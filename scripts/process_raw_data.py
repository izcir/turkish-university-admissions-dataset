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

    # --------------------------------------------------
    # Lessons Dimension + Net Stats Fact Table
    # --------------------------------------------------

    lessons_data = [
        {'lesson_name': 'AYT Biyoloji', 'exam_type': 'AYT', 'max_questions': 13},
        {'lesson_name': 'AYT Coğrafya-1', 'exam_type': 'AYT', 'max_questions': 6},
        {'lesson_name': 'AYT Coğrafya-2', 'exam_type': 'AYT', 'max_questions': 11},
        {'lesson_name': 'AYT Din Kültürü ve Ahlak Bilgisi', 'exam_type': 'AYT', 'max_questions': 6},
        {'lesson_name': 'AYT Felsefe Grubu', 'exam_type': 'AYT', 'max_questions': 12},
        {'lesson_name': 'AYT Fizik', 'exam_type': 'AYT', 'max_questions': 14},
        {'lesson_name': 'AYT Kimya', 'exam_type': 'AYT', 'max_questions': 13},
        {'lesson_name': 'AYT Matematik', 'exam_type': 'AYT', 'max_questions': 40},
        {'lesson_name': 'AYT Tarih-1', 'exam_type': 'AYT', 'max_questions': 10},
        {'lesson_name': 'AYT Tarih-2', 'exam_type': 'AYT', 'max_questions': 11},
        {'lesson_name': 'AYT Türk Dili ve Edebiyatı', 'exam_type': 'AYT', 'max_questions': 24},
        {'lesson_name': 'TYT Fen Bilimleri', 'exam_type': 'TYT', 'max_questions': 20},
        {'lesson_name': 'TYT Temel Matematik', 'exam_type': 'TYT', 'max_questions': 40},
        {'lesson_name': 'TYT Sosyal Bilimler', 'exam_type': 'TYT', 'max_questions': 20},
        {'lesson_name': 'TYT Türkçe', 'exam_type': 'TYT', 'max_questions': 40},
        {'lesson_name': 'YDT Yabancı Dil', 'exam_type': 'YDT', 'max_questions': 80}
    ]
    
    lesson_column_map = {
        'AYT Biyoloji': 'ayt_bio',
        'AYT Coğrafya-1': 'ayt_cog1',
        'AYT Coğrafya-2': 'ayt_cog2',
        'AYT Din Kültürü ve Ahlak Bilgisi': 'ayt_dk',
        'AYT Felsefe Grubu': 'ayt_fel',
        'AYT Fizik': 'ayt_fiz',
        'AYT Kimya': 'ayt_kim',
        'AYT Matematik': 'ayt_mat',
        'AYT Tarih-1': 'ayt_tar1',
        'AYT Tarih-2': 'ayt_tar2',
        'AYT Türk Dili ve Edebiyatı': 'ayt_tr',
        'TYT Fen Bilimleri': 'tyt_fen',
        'TYT Temel Matematik': 'tyt_mat',
        'TYT Sosyal Bilimler': 'tyt_sos',
        'TYT Türkçe': 'tyt_tr',
        'YDT Yabancı Dil': 'ydt_dil'
    }

    lessons_df = pd.DataFrame(lessons_data)
    lessons_df['lesson_id'] = range(1, len(lessons_df) + 1)

    lessons_df = lessons_df[['lesson_id', 'lesson_name', 'exam_type', 'max_questions']]
    lessons_df.to_csv(os.path.join(PROCESSED_DIR, "lessons.csv"), index=False)

    nets_012_df = pd.read_csv(os.path.join(RAW_DIR, "department_avg_nets_012.csv"))
    nets_018_df = pd.read_csv(os.path.join(RAW_DIR, "department_avg_nets_018.csv"))

    nets_012_df['coefficient_type'] = '0.12'
    nets_018_df['coefficient_type'] = '0.18'

    all_nets_df = pd.concat([nets_012_df, nets_018_df], ignore_index=True)

    id_vars = ['program_code', 'year', 'coefficient_type']
    value_vars = list(lesson_column_map.values())

    long_format_nets = pd.melt(
        all_nets_df,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='lesson_column',
        value_name='average_net'
    )

    long_format_nets.dropna(subset=['average_net'], inplace=True)
    
    column_to_lesson_df = pd.DataFrame(list(lesson_column_map.items()), columns=['lesson_name', 'lesson_column'])
    column_to_lesson_df = pd.merge(column_to_lesson_df, lessons_df[['lesson_id', 'lesson_name']], on='lesson_name')

    final_net_stats = pd.merge(
        long_format_nets,
        column_to_lesson_df[['lesson_column', 'lesson_id']],
        on='lesson_column'
    )
    
    department_net_stats_df = final_net_stats[[
        'program_code',
        'year',
        'lesson_id',
        'coefficient_type',
        'average_net'
    ]].reset_index(drop=True)

    department_net_stats_df.to_csv(os.path.join(PROCESSED_DIR, "department_avg_net_stats.csv"), index=False)

    # --------------------------------------------------
    # Department Preferences Fact Table + Preference Ranks Bridge Table
    # --------------------------------------------------

    preferences_df = pd.read_csv(os.path.join(RAW_DIR, "department_preference_raw.csv"))

    preferences_df['program_code'] = preferences_df['program_code'].astype(str)

    department_preferences_df = preferences_df[[
        'program_code',
        'year',
        'total_preferences',
        'demand_per_quota',
        'avg_preference_rank',
        'top_1_pref_count',
        'top_3_pref_count',
        'top_9_pref_count'
    ]].copy()
    department_preferences_df.to_csv(os.path.join(PROCESSED_DIR, "department_preferences.csv"), index=False)

    rank_columns = [f'rank_{i}_count' for i in range(1, 10)] + ['rank_10_plus_count']
    rank_levels = [str(i) for i in range(1, 10)] + ['10+']

    preferences_ranks_long = pd.melt(
        preferences_df,
        id_vars=['program_code', 'year'],
        value_vars=rank_columns,
        var_name='rank_column',
        value_name='count'
    )

    rank_mapping = {col: level for col, level in zip(rank_columns, rank_levels)}
    preferences_ranks_long['rank_level'] = preferences_ranks_long['rank_column'].map(rank_mapping)

    department_preference_ranks_df = preferences_ranks_long[[
        'program_code',
        'year',
        'rank_level',
        'count'
    ]].dropna(subset=['count']).reset_index(drop=True)

    department_preference_ranks_df.to_csv(os.path.join(PROCESSED_DIR, "department_preference_ranks.csv"), index=False)

    # --------------------------------------------------
    # Department Placed Preferences Fact Table + Placed Preference Ranks Bridge Table
    # --------------------------------------------------

    placed_df = pd.read_csv(os.path.join(RAW_DIR, "department_placed_preference_raw.csv"))

    placed_df['program_code'] = placed_df['program_code'].astype(str)

    department_placed_preferences_df = placed_df[[
        'program_code',
        'year',
        'placed_count',
        'placed_pref_rank_avg',
        'placed_top_1_pref_count',
        'placed_top_3_pref_count',
        'placed_top_10_pref_count'
    ]].copy()
    department_placed_preferences_df.to_csv(os.path.join(PROCESSED_DIR, "department_placed_preferences.csv"), index=False)

    rank_columns = [f'placed_rank_{i}_count' for i in range(1, 25)]
    rank_levels = [str(i) for i in range(1, 25)]

    placed_ranks_long = pd.melt(
        placed_df,
        id_vars=['program_code', 'year'],
        value_vars=rank_columns,
        var_name='rank_column',
        value_name='count'
    )

    rank_mapping = {col: level for col, level in zip(rank_columns, rank_levels)}
    placed_ranks_long['rank_level'] = placed_ranks_long['rank_column'].map(rank_mapping)

    department_placed_preference_ranks_df = placed_ranks_long[[
        'program_code',
        'year',
        'rank_level',
        'count'
    ]].dropna(subset=['count']).reset_index(drop=True)

    department_placed_preference_ranks_df.to_csv(os.path.join(PROCESSED_DIR, "department_placed_preference_ranks.csv"), index=False)


if __name__ == "__main__":  
    main()

