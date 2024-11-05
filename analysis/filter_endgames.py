import csv

# Copyright Josiah Plett 2024

def process_all_games(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            try:
                row['Endgame'] = int(row['Endgame'])
                row['WhiteTotalTime'] = float(row['WhiteTotalTime'])
                row['BlackTotalTime'] = float(row['BlackTotalTime'])
                row['WhiteOpeningTime'] = float(row['WhiteOpeningTime'])
                row['BlackOpeningTime'] = float(row['BlackOpeningTime'])
            except ValueError:
                continue
            
            if row['Endgame'] == -1:
                row['WhiteMiddlegameTime'] = round(row['WhiteTotalTime'] - row['WhiteOpeningTime'], 4)
                row['BlackMiddlegameTime'] = round(row['BlackTotalTime'] - row['BlackOpeningTime'], 4)
            
            writer.writerow(row)

def filter_endgame_games(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        if fieldnames is None:
            print("No data to process.")
            return
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            try:
                if int(row['Endgame']) != -1:
                    writer.writerow(row)
            except ValueError:
                continue

def main():
    input("This file will attempt to process the data in `output/project_2_parsed_output.csv`. Press Enter to continue...")

    input_csv = '../data/output/project_2_parsed_output.csv'
    output_csv_all_games = '../data/output/project_2_all_games.csv'
    process_all_games(input_csv, output_csv_all_games)
    
    input("Processing complete. Press Enter to continue...")
    
    output_csv_endgame_games = '../data/output/project_2_endgame_games.csv'
    filter_endgame_games(output_csv_all_games, output_csv_endgame_games)

if __name__ == '__main__':
    main()
