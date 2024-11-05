"""
SIMPLIFICATION UTILITY

Use this file to get yourself a simplified data set to work on, to organize
your thoughts better and ensure you don't accidentally mix up columns or
overfit your model to columns you didn't originally want to analyze.
"""

import csv
import os
import re
import glob

# Copyright Josiah Plett 2024

def simplify_csv(input_csv, columns_to_keep):
    # 1. Establish what the output CSV filename should be
    input_dir = os.path.dirname(input_csv)
    if input_dir == '':
        input_dir = '.'
    pattern = os.path.join(input_dir, 'project_2_simplified_*.csv')
    existing_files = glob.glob(pattern)
    existing_indices = []
    for filename in existing_files:
        match = re.search(r'project_2_simplified_(\d+)\.csv', os.path.basename(filename))
        if match:
            existing_indices.append(int(match.group(1)))
    new_index = max(existing_indices) + 1 if existing_indices else 1

    # Set output filename
    output_csv = os.path.join(input_dir, f'project_2_simplified_{new_index}.csv')

    # Filter out all columns except the ones we want to keep
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        input_fieldnames = reader.fieldnames
        columns_to_keep = [col for col in columns_to_keep if col in input_fieldnames]
        output_fieldnames = columns_to_keep + ['Row']
        writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
        writer.writeheader()

        col_num = 1
        for row in reader:
            new_row = {key: row[key] for key in columns_to_keep}

            # You can happily add any simple column modifications here :)

            new_row['Row'] = col_num
            writer.writerow(new_row)
            col_num += 1

            if col_num % 1000 == 0:
                print(f"Processed {col_num} rows...")

    print(f"Simplified CSV saved to {output_csv}")

def main():
    # Decide here if you want all games or just games that lasted until the endgame.
    input_csv = '../data/output/project_2_all_games.csv'
    # input_csv = '../data/output/project_2_endgame_games.csv'

    # Define the attributes you want to keep!
    # Preferably, put the attribute you're predicting at the start.
    columns_to_keep = ['TotalPlies', 'EloDifference', 'Middlegame', 'WhiteOpeningTime', 'BlackOpeningTime', 'WhiteTotalTime', 'BlackTotalTime', 'Termination']

    simplify_csv(input_csv, columns_to_keep)

if __name__ == '__main__':
    main()
