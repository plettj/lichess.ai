import csv
import ast

# Copyright Josiah Plett 2024

def main():
    # input_csv_path = '../data/output/project_2_parsed_output.csv'
    # output_csv_path = '../data/output/project_2_parsed_output_extended.csv'

    input_csv_path = '../data/output/short_parsed_output_8.csv'
    output_csv_path = '../data/output/short_parsed_output_8_extended_2.csv'

    with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:

        # Use csv.DictReader and DictWriter
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames.copy()

        # Insert 'EloDifference' after 'BlackElo'
        black_elo_index = fieldnames.index('BlackElo')
        fieldnames.insert(black_elo_index + 1, 'EloDifference')

        # Insert 'TotalMoves' after 'FEN'
        fen_index = fieldnames.index('FEN')
        fieldnames.insert(fen_index + 1, 'TotalMoves')

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        row_count = 0
        for row in reader:
            # Get WhiteElo and BlackElo
            white_elo = row.get('WhiteElo', '')
            black_elo = row.get('BlackElo', '')

            try:
                elo_difference = int(white_elo) - int(black_elo)
            except ValueError:
                elo_difference = ''  # Leave empty if parsing fails

            # Get WhiteTimes and BlackTimes
            white_times_str = row.get('WhiteTimes', '')
            black_times_str = row.get('BlackTimes', '')

            try:
                # Ensure that the times are properly parsed as lists
                white_times_list = ast.literal_eval(white_times_str)
                black_times_list = ast.literal_eval(black_times_str)

                # Confirm that we have lists
                if isinstance(white_times_list, list) and isinstance(black_times_list, list):
                    total_moves = len(white_times_list) + len(black_times_list)
                else:
                    total_moves = ''
            except (ValueError, SyntaxError):
                total_moves = ''  # Leave empty if parsing fails

            # Insert EloDifference into row
            row['EloDifference'] = elo_difference

            # Insert TotalMoves into row
            row['TotalMoves'] = total_moves

            if total_moves > 8:
                writer.writerow(row)

                row_count += 1
                if row_count % 1000 == 0:
                    print(f'Processed {row_count} rows.')

    print('Processing completed.')

if __name__ == '__main__':
    main()
