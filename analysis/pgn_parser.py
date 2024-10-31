import chess.pgn
import csv
import re
import ast

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

    # Parse Result
    result = 0 if result == '1/2-1/2' else 1 if result == '1-0' else -1

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

    # Initialize time usage columns
    white_opening_time = black_opening_time = white_middlegame_time = black_middlegame_time = -1
    white_endgame_time = black_endgame_time = white_total_time = black_total_time = -1

    # Track time used in each phase
    time_used = {'white_opening': 0, 'black_opening': 0, 'white_middlegame': 0, 'black_middlegame': 0, 'white_endgame': 0, 'black_endgame': 0}

    node = game

    while node.variations:
        next_node = node.variations[0]
        move = next_node.move

        # Update the board with the move
        board.push(move)
        total_move_counter += 1  # Increment move counter

        comment = next_node.comment
        clock_times = re.findall(r'\[%clk\s+([^\]]+)\]', comment)

        if clock_times:
            clock_time_str = clock_times[0]
            clock_time = parse_clock_time(clock_time_str)

            player = 'white' if node.board().turn == chess.WHITE else 'black'
            move_number[player] += 1

            if clock_time is not None:
                time_taken = prev_clock[player] - clock_time
                prev_clock[player] = clock_time

                # Accumulate time based on the game phase
                if player == 'white':
                    white_times.append(time_taken)
                else:
                    black_times.append(time_taken)
                
                if middlegame_move == -1:
                    time_used[f'{player}_opening'] += time_taken
                elif endgame_move == -1:
                    time_used[f'{player}_middlegame'] += time_taken
                else:
                    time_used[f'{player}_endgame'] += time_taken
        else:
            # No clock time found, skip this whole game
            return

        # Check for middlegame start
        if middlegame_move == -1 and is_middlegame(board):
            middlegame_move = total_move_counter
            white_opening_time = time_used['white_opening'] / base_time
            black_opening_time = time_used['black_opening'] / base_time

        # Check for endgame start
        if endgame_move == -1 and is_endgame(board):
            endgame_move = total_move_counter
            white_middlegame_time = time_used['white_middlegame'] / base_time
            black_middlegame_time = time_used['black_middlegame'] / base_time

        node = next_node
    
    # If the middlegame was never reached, set it to the ply where the game ended
    if middlegame_move == -1:
        middlegame_move = total_move_counter
        white_opening_time = time_used['white_opening'] / base_time
        black_opening_time = time_used['black_opening'] / base_time

    # Calculate total moves
    total_moves = len(white_times) + len(black_times)

    if total_moves <= 8:
        return  # Filter out games with fewer than 9 moves

    # Finalize endgame time and total clock time usage
    white_endgame_time = time_used['white_endgame'] / base_time if endgame_move > -1 else -1
    black_endgame_time = time_used['black_endgame'] / base_time if endgame_move > -1 else -1
    white_total_time = (base_time - prev_clock['white']) / base_time if termination != "Time forfeit" or result != -1 else 1
    black_total_time = (base_time - prev_clock['black']) / base_time if termination != "Time forfeit" or result != 1 else 1

    # Calculate elo difference
    try:
        elo_difference = int(white_elo) - int(black_elo)
    except ValueError:
        elo_difference = ''

    significant_digits = 4

    # Data for writing to CSV
    data = {
        'White': white,
        'Black': black,
        'Result': result,
        'WhiteElo': white_elo,
        'BlackElo': black_elo,
        'EloDifference': elo_difference,
        'TimeControl': time_control,
        'Termination': termination,
        'FEN': fen,
        'WhiteTimes': white_times,
        'BlackTimes': black_times,
        'TotalMoves': total_moves,
        'Middlegame': middlegame_move,
        'Endgame': endgame_move,
        'WhiteOpeningTime': round(white_opening_time, significant_digits),
        'BlackOpeningTime': round(black_opening_time, significant_digits),
        'WhiteMiddlegameTime': round(white_middlegame_time, significant_digits) if endgame_move > -1 else -1,
        'BlackMiddlegameTime': round(black_middlegame_time, significant_digits) if endgame_move > -1 else -1,
        'WhiteEndgameTime': round(white_endgame_time, significant_digits) if endgame_move > -1 else -1,
        'BlackEndgameTime': round(black_endgame_time, significant_digits) if endgame_move > -1 else -1,
        'WhiteTotalTime': round(white_total_time, significant_digits),
        'BlackTotalTime': round(black_total_time, significant_digits),
    }

    return data

def main():
    # pgn_file_path = '../data/lichess_db_chess960_rated_2024-08.pgn'
    # output_csv_path = '../data/output/project_2_parsed_output.csv'

    pgn_file_path = '../data/much_shorter_mock_data.pgn'
    output_csv_path = '../data/output/short_parsed_output_13_extended.csv'

    pgn = open(pgn_file_path)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Result', 'White', 'Black', 'WhiteElo', 'BlackElo', 'EloDifference', 'TimeControl',
            'Termination', 'FEN', 'WhiteTimes', 'BlackTimes', 'TotalMoves', 'Middlegame', 'Endgame',
            'WhiteOpeningTime', 'BlackOpeningTime', 'WhiteMiddlegameTime', 'BlackMiddlegameTime',
            'WhiteEndgameTime', 'BlackEndgameTime', 'WhiteTotalTime', 'BlackTotalTime'
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

                if game_count % 1000 == 0:
                    print(f'Processed {game_count} games.')

        print(f'Processed {game_count} games in total.')

    pgn.close()

if __name__ == '__main__':
    main()
