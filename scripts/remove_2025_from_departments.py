import csv
import re

input_path = 'data/raw/departments_raw.csv'
output_path = 'data/raw/departments_raw_no2025.csv'

def has_only_2025(years):
    years = years.strip('"')
    year_list = [y.strip() for y in years.split(',') if y.strip()]
    return len(year_list) == 1 and year_list[0] == '2025'

def remove_2025(years):
    years = years.strip('"')
    year_list = [y.strip() for y in years.split(',') if y.strip() and y.strip() != '2025']
    return ','.join(year_list)

with open(input_path, encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    header = next(reader)
    writer.writerow(header)
    for row in reader:
        years = row[6]
        if has_only_2025(years):
            continue
        row[6] = remove_2025(years)
        writer.writerow(row)
