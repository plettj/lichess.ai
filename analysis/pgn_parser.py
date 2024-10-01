import chess.pgn
import csv
import re

def parse_time_control(time_control):
    # Parse TimeControl string like '180+2'
    try:
        base, increment = time_control.split('+')
        base_time = int(base)
        increment = int(increment)
        return base_time, increment
    except ValueError:
        # Invalid TimeControl format
        return None, None

def parse_clock_time(clock_str):
    # Parse clock time string like '0:02:59' into seconds
    try:
        time_parts = clock_str.strip().split(':')
        time_parts = [int(part) for part in time_parts]
        if len(time_parts) == 3:
            hours, minutes, seconds = time_parts
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(time_parts) == 2:
            minutes, seconds = time_parts
            total_seconds = minutes * 60 + seconds
        else:
            total_seconds = int(time_parts[0])
        return total_seconds
    except ValueError:
        return None

def main():
    # pgn_file_path = '../data/lichess_db_chess960_rated_2024-08.pgn'
    # output_csv_path = '../data/output/parsed_output_1.csv'

    pgn_file_path = '../data/much_shorter_mock_data.pgn'
    output_csv_path = '../data/output/short_parsed_output_5.csv'

    pgn = open(pgn_file_path)

    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Result', 'White', 'Black', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination', 'FEN', 'WhiteTimes', 'BlackTimes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # End of file

            # Extract headers
            headers = game.headers
            result = headers.get('Result', '')
            white = headers.get('White', '')
            black = headers.get('Black', '')
            white_elo = headers.get('WhiteElo', '')
            black_elo = headers.get('BlackElo', '')
            time_control = headers.get('TimeControl', '')
            termination = headers.get('Termination', '')
            fen = headers.get('FEN', '')

            # Parse TimeControl
            base_time, increment = parse_time_control(time_control)

            # Filter games based on TimeControl
            if base_time is None or increment is None:
                continue
            if base_time < 180 or base_time > 300:
                continue
            if base_time == 300 and increment > 5:
                continue

            # Initialize move times
            white_times = []
            black_times = []
            prev_clock = {'white': base_time, 'black': base_time}
            move_number = {'white': 0, 'black': 0}

            node = game

            while node.variations:
                next_node = node.variations[0]
                move = next_node.move
                comment = next_node.comment

                clock_times = re.findall(r'\[%clk\s+([^\]]+)\]', comment)
                if clock_times:
                    clock_time_str = clock_times[0]
                    clock_time = parse_clock_time(clock_time_str)

                    player = 'white' if node.board().turn == chess.WHITE else 'black'

                    move_number[player] += 1

                    if clock_time is not None:
                        if move_number[player] == 1:
                            time_taken = prev_clock[player] - clock_time
                        else:
                            time_taken = prev_clock[player] - clock_time + increment

                        prev_clock[player] = clock_time
                        if time_taken < 0:
                            time_taken = 0
                        if player == 'white':
                            white_times.append(time_taken)
                        else:
                            black_times.append(time_taken)

                node = next_node


            # Write data to CSV
            data = {
                'White': white,
                'Black': black,
                'Result': result,
                'WhiteElo': white_elo,
                'BlackElo': black_elo,
                'TimeControl': time_control,
                'Termination': termination,
                'FEN': fen,
                'WhiteTimes': white_times,
                'BlackTimes': black_times,
            }
            writer.writerow(data)
            game_count += 1

            print(f'Processed game {game_count} with TimeControl {time_control}.')

            if game_count % 100 == 0:
                print(f'Processed {game_count} games.')

if __name__ == '__main__':
    main()
