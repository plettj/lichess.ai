import chess.pgn
import csv
import re

# Copyright Josiah Plett 2024

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

def count_major_minor_pieces(board):
    # Counts the total number of major and minor pieces on the board
    major_minor_pieces = 0
    for piece in board.piece_map().values():
        if piece.piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
            major_minor_pieces += 1
    return major_minor_pieces

def is_middlegame(board):
    # Checks if any of the middlegame conditions are met
    # Returns a tuple (True/False, Reason)

    # Condition 1: 10 or fewer major or minor pieces
    major_minor_pieces = count_major_minor_pieces(board)
    if major_minor_pieces <= 10:
        return True

    # Condition 2: Back rank is sparse (rows 1 and 8 have fewer than 9 pieces total)
    back_rank_pieces = 0
    for square in chess.SquareSet(chess.BB_RANK_1 | chess.BB_RANK_8):
        if board.piece_at(square) is not None:
            back_rank_pieces += 1
    if back_rank_pieces < 9:  # fewer than 9 pieces
        return True

    # Condition 3: Sufficient mixing (at least 12 pieces or pawns in the middle 4 rows)
    middle_rows_pieces = 0
    for square in chess.SquareSet(chess.BB_RANK_3 | chess.BB_RANK_4 | chess.BB_RANK_5 | chess.BB_RANK_6):
        if board.piece_at(square) is not None:
            middle_rows_pieces += 1
    if middle_rows_pieces >= 12:
        return True

    return False

def is_endgame(board):
    # Checks if the endgame condition is met
    # Condition: 6 or fewer major or minor pieces
    if count_major_minor_pieces(board) <= 6:
        return True
    return False

def do_processing(game):
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

    # Filter out all non 3|2 games, based on TimeControl
    if base_time is None or increment is None:
        return
    if base_time != 180 or increment != 0:
        return

    # Initialize move times
    white_times = []
    black_times = []
    prev_clock = {'white': base_time, 'black': base_time}
    move_number = {'white': 0, 'black': 0}

    # Initialize board and move counters for middlegame and endgame detection
    board = game.board()
    middlegame_move = -1
    endgame_move = -1
    total_move_counter = 0  # Counts half-moves (plies)

    node = game

    while node.variations:
        next_node = node.variations[0]
        move = next_node.move

        # Update the board with the move
        board.push(move)
        total_move_counter += 1  # Increment move counter

        # Check for middlegame start
        if middlegame_move == -1:
            is_midgame = is_middlegame(board)
            if is_midgame:
                middlegame_move = total_move_counter

        # Check for endgame start
        if endgame_move == -1 and is_endgame(board):
            endgame_move = total_move_counter

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

    # Data for writing to CSV
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
        'Middlegame': middlegame_move,
        'Endgame': endgame_move,
    }

    return data

def main():
    # pgn_file_path = '../data/lichess_db_chess960_rated_2024-08.pgn'
    # output_csv_path = '../data/output/parsed_output.csv'

    pgn_file_path = '../data/much_shorter_mock_data.pgn'
    output_csv_path = '../data/output/short_parsed_output_8.csv'

    pgn = open(pgn_file_path)

    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            'Result', 'White', 'Black', 'WhiteElo', 'BlackElo', 'TimeControl',
            'Termination', 'FEN', 'WhiteTimes', 'BlackTimes', 'Middlegame', 'Endgame'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        game_count = 0

        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # End of file

            data = do_processing(game)

            if data is not None:
              writer.writerow(data)
              game_count += 1

              if game_count % 100 == 0:
                  print(f'Processed {game_count} games.')

        print(f'Processed {game_count} games.')

    pgn.close()

if __name__ == '__main__':
    main()
