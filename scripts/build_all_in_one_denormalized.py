import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
OUTPUT_FILE = os.path.join(BASE_DIR, "data", 'all_in_one_denormalized.csv')


def main():
    # Core processed tables
    dept_norm = pd.read_csv(os.path.join(PROCESSED_DIR, 'departments_normalized.csv'))
    dept_names = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_names.csv'))
    faculty_names = pd.read_csv(os.path.join(PROCESSED_DIR, 'faculty_names.csv'))
    universities = pd.read_csv(os.path.join(PROCESSED_DIR, 'universities_normalized.csv'))
    uni_types = pd.read_csv(os.path.join(PROCESSED_DIR, 'university_types.csv'))
    uni_cities = pd.read_csv(os.path.join(PROCESSED_DIR, 'university_cities.csv'))
    score_types = pd.read_csv(os.path.join(PROCESSED_DIR, 'score_types.csv'))
    scholarship_types = pd.read_csv(os.path.join(PROCESSED_DIR, 'scholarship_types.csv'))
    dept_years = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_years.csv'))
    years = pd.read_csv(os.path.join(PROCESSED_DIR, 'years.csv'))
    dept_tags = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_tags.csv'))
    tags = pd.read_csv(os.path.join(PROCESSED_DIR, 'tags.csv'))
    stats = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_stats.csv'))
    # Raw stats (already partially cleaned but not normalized)
    #stats = pd.read_csv(os.path.join(RAW_DIR, 'department_stats_raw.csv'))

    # Build tags aggregated per program_code
    tags_full = dept_tags.merge(tags, on='tag_id', how='left')
    tags_agg = (tags_full
                .dropna(subset=['tag'])
                .groupby('program_code')['tag']
                .apply(lambda s: ','.join(sorted(set(t for t in s if isinstance(t, str) and t.strip()))))
                .reset_index()
                .rename(columns={'tag': 'all_tags'}))

    # Expand departments by years
    dept_year_expanded = dept_norm.merge(dept_years, on='program_code', how='left')
    dept_year_expanded = dept_year_expanded.merge(years, on='year_id', how='left')

    # Join names
    dept_year_expanded = dept_year_expanded.merge(dept_names, on='department_name_id', how='left')
    dept_year_expanded = dept_year_expanded.merge(faculty_names, on='faculty_name_id', how='left')

    # University joins
    universities_full = (universities
                         .merge(uni_types, on='university_type_id', how='left')
                         .merge(uni_cities, on='university_city_id', how='left'))
    dept_year_expanded = dept_year_expanded.merge(universities_full, on='university_id', how='left')

    # Score & scholarship
    dept_year_expanded = dept_year_expanded.merge(score_types, on='score_type_id', how='left')
    dept_year_expanded = dept_year_expanded.merge(scholarship_types, on='scholarship_type_id', how='left')

    # Tags aggregated
    dept_year_expanded = dept_year_expanded.merge(tags_agg, on='program_code', how='left')

    # Merge stats (left join to keep structure even if stats missing)
    if 'year' in stats.columns:
        try:
            dept_year_expanded['year_int'] = dept_year_expanded['year'].astype(int)
            stats['year_int'] = stats['year'].astype(int)
            merged = dept_year_expanded.merge(stats.drop(columns=['year']), on=['program_code', 'year_int'], how='left')
            merged['year'] = merged['year_int']
            merged.drop(columns=['year_int'], inplace=True)
        except Exception:
            dept_year_expanded['year_str'] = dept_year_expanded['year'].astype(str)
            stats['year_str'] = stats['year'].astype(str)
            merged = dept_year_expanded.merge(stats.drop(columns=['year']), on=['program_code', 'year_str'], how='left')
            merged['year'] = merged['year_str']
            merged.drop(columns=['year_str'], inplace=True)
    else:
        merged = dept_year_expanded.copy()

    # RANK kolonlarini kesin olarak Int64 (nullable) formatina zorla
    for rank_col in ['final_rank_012', 'final_rank_018']:
        if rank_col in merged.columns:
            merged[rank_col] = pd.to_numeric(merged[rank_col], errors='coerce').round(0).astype('Int64')

    final_cols = [
        'program_code', 'year', 'university_name', 'city', 'university_type', 'department_name',
        'faculty_name', 'score_type', 'scholarship_type', 'is_undergraduate', 'all_tags',
        'total_quota', 'total_enrolled', 'male', 'female', 'final_score_012', 'final_rank_012',
        'final_score_018', 'final_rank_018'
    ]

    for c in final_cols:
        if c not in merged.columns:
            merged[c] = pd.NA

    # Sort by university_name primarily (then department_name, program_code, year for determinism)
    final_df = (merged[final_cols]
                .sort_values(['university_name', 'department_name', 'program_code', 'year'])
                .reset_index(drop=True))

    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Written {OUTPUT_FILE} with {len(final_df):,} rows (sorted by university_name, ranks as Int64).")


if __name__ == '__main__':
    main()
