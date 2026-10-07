import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
OUTPUT_FILE = os.path.join(BASE_DIR, "data", 'all_in_one_denormalized.csv')


# These 29 codes identify a different program from 2025 onward.
# Existing CSVs retain their original schema and the latest identity.
# Preserve their 2024 identity when producing the historical merged CSV.
PROGRAM_IDENTITIES_2024 = {202990358: {'department_name_id': 607,
             'faculty_name_id': 34,
             'scholarship_type_id': 3,
             'score_type_id': 4,
             'tags': 'Burslu'},
 202990365: {'department_name_id': 607,
             'faculty_name_id': 34,
             'scholarship_type_id': 6,
             'score_type_id': 4,
             'tags': '%50 İndirimli'},
 208910258: {'department_name_id': 409,
             'faculty_name_id': 53,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209010289: {'department_name_id': 721,
             'faculty_name_id': 461,
             'scholarship_type_id': 3,
             'score_type_id': 3,
             'tags': 'Burslu,İngilizce'},
 209010296: {'department_name_id': 721,
             'faculty_name_id': 461,
             'scholarship_type_id': 9,
             'score_type_id': 3,
             'tags': '%25 İndirimli,İngilizce'},
 209210173: {'department_name_id': 409,
             'faculty_name_id': 9,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210180: {'department_name_id': 491,
             'faculty_name_id': 9,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210187: {'department_name_id': 11,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210194: {'department_name_id': 21,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210201: {'department_name_id': 23,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210208: {'department_name_id': 90,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210215: {'department_name_id': 152,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210222: {'department_name_id': 154,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210229: {'department_name_id': 228,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210236: {'department_name_id': 323,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210243: {'department_name_id': 465,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210250: {'department_name_id': 468,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210257: {'department_name_id': 515,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210264: {'department_name_id': 542,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210271: {'department_name_id': 635,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210278: {'department_name_id': 636,
             'faculty_name_id': 12,
             'scholarship_type_id': 9,
             'score_type_id': 2,
             'tags': '%25 İndirimli'},
 209210320: {'department_name_id': 305,
             'faculty_name_id': 672,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli'},
 209210327: {'department_name_id': 298,
             'faculty_name_id': 948,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli'},
 209210334: {'department_name_id': 508,
             'faculty_name_id': 163,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli,İngilizce'},
 209210341: {'department_name_id': 687,
             'faculty_name_id': 163,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli,İngilizce'},
 209210348: {'department_name_id': 687,
             'faculty_name_id': 163,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli'},
 209210355: {'department_name_id': 728,
             'faculty_name_id': 163,
             'scholarship_type_id': 9,
             'score_type_id': 4,
             'tags': '%25 İndirimli'},
 209210362: {'department_name_id': 279,
             'faculty_name_id': 157,
             'scholarship_type_id': 9,
             'score_type_id': 1,
             'tags': '%25 İndirimli'},
 209210369: {'department_name_id': 73,
             'faculty_name_id': 76,
             'scholarship_type_id': 9,
             'score_type_id': 3,
             'tags': '%25 İndirimli,İngilizce'}}


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
    # Eklenen tercih verisi
    preferences = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_preferences.csv'))
    # Eklenen placed tercih verisi
    placed_preferences = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_placed_preferences.csv'))

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
    for code, identity in PROGRAM_IDENTITIES_2024.items():
        historical = dept_year_expanded['program_code'].eq(code) & dept_year_expanded['year'].eq(2024)
        if historical.sum() != 1:
            raise ValueError(f'Expected one 2024 record for reused program code {code}')
        for field, value in identity.items():
            dept_year_expanded.loc[historical, field] = value


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
    for code, identity in PROGRAM_IDENTITIES_2024.items():
        historical = dept_year_expanded['program_code'].eq(code) & dept_year_expanded['year'].eq(2024)
        dept_year_expanded.loc[historical, 'all_tags'] = ','.join(
            sorted(set(t.strip() for t in identity['tags'].split(',') if t.strip())))


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

    # Tercih verisini ekle
    preferences['year'] = preferences['year'].astype(int)
    merged = merged.merge(preferences, on=['program_code', 'year'], how='left')

    # Placed tercih verisini ekle
    placed_preferences['year'] = placed_preferences['year'].astype(int)
    merged = merged.merge(placed_preferences, on=['program_code', 'year'], how='left')

    placed_uni_type = pd.read_csv(os.path.join(PROCESSED_DIR, 'department_placed_pref_uni_type.csv'))
    # 2019-2024 has an explicit row for every university type, including real zeros.
    # 2025 omits yurt dışı (type 4): YokAtlas published 0 for every program while 2024
    # had hundreds of positive programs, so that 0 is treated as missing, not a count.
    # Do not fill_value=0; a missing 2025 type-4 cell must stay null.
    placed_uni_type_pivot = placed_uni_type.pivot_table(
        index=['program_code', 'year'],
        columns='university_type_id',
        values='placed_pref_count',
        aggfunc='first',
    ).reset_index()
    placed_uni_type_pivot = placed_uni_type_pivot.rename(columns={
        1: 'placed_pref_uni_devlet_count',
        2: 'placed_pref_uni_vakif_count',
        3: 'placed_pref_uni_kktc_count',
        4: 'placed_pref_uni_yurt_disi_count'
    })
    merged = merged.merge(placed_uni_type_pivot, on=['program_code', 'year'], how='left')

    # Devlet / vakıf / KKTC rows exist for every program-year. fillna(0) only covers a
    # join miss and does not change 2019-2024 values. Yurt dışı is left nullable so the
    # omitted 2025 rows are not written as a fake 0.
    for col in ['placed_pref_uni_devlet_count', 'placed_pref_uni_vakif_count', 'placed_pref_uni_kktc_count']:
        if col in merged.columns:
            merged[col] = pd.to_numeric(merged[col], errors='coerce').fillna(0).round(0).astype('Int64')
    if 'placed_pref_uni_yurt_disi_count' in merged.columns:
        merged['placed_pref_uni_yurt_disi_count'] = pd.to_numeric(
            merged['placed_pref_uni_yurt_disi_count'], errors='coerce'
        ).round(0).astype('Int64')

    for rank_col in ['final_rank_012', 'final_rank_018']:
        if rank_col in merged.columns:
            merged[rank_col] = pd.to_numeric(merged[rank_col], errors='coerce').round(0).astype('Int64')

    final_cols = [
        'program_code', 'year', 'university_name', 'city', 'university_type', 'department_name',
        'faculty_name', 'score_type', 'scholarship_type', 'is_undergraduate', 'all_tags',
        'total_quota', 'total_enrolled', 'male', 'female', 'final_score_012', 'final_rank_012',
        'final_score_018', 'final_rank_018', 'initial_placement_rate', 'not_registered', 
        'additional_placement', 'avg_obp_012', 'avg_obp_018',
        # Eklenen sütunlar
        'total_preferences', 'demand_per_quota', 'avg_preference_rank', "top_1_pref_count", "top_3_pref_count", "top_9_pref_count",
        'placed_count', 'placed_pref_rank_avg', 'placed_top_1_pref_count', 'placed_top_3_pref_count', 'placed_top_10_pref_count',
        # Yeni eklenen sütunlar
        'placed_pref_uni_devlet_count', 'placed_pref_uni_vakif_count', 'placed_pref_uni_kktc_count', 'placed_pref_uni_yurt_disi_count'
    ]

    for c in final_cols:
        if c not in merged.columns:
            merged[c] = pd.NA

    final_df = (merged[final_cols]
                .sort_values(['university_name', 'department_name', 'program_code', 'year'])
                .reset_index(drop=True))

    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Written {OUTPUT_FILE} with {len(final_df):,} rows (sorted by university_name, ranks as Int64).")


if __name__ == '__main__':
    main()
