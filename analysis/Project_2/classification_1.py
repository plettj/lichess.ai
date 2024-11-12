"""
Input Features + Transformations
- Elo Difference: Normalize between 0 and 1
- Termination Reason: One hot encode
- Total Plies: Normalize between 0 and 1
- Opening Plies: Normalize into percentage of plies in the opening
- Middlegame Plies: Ditto for the above
- Endgame Plies: Ditto for the above
- Black + White Opening/Middlegame/Endgame times: Normalize between 0 and 1
"""

import csv
import math

# Copyright Josiah Plett 2024

class Stats:
    def __init__(self):
        self.min = math.inf
        self.max = -math.inf
    def __repr__(self):
        return f"Stats(min={self.min}, max={self.max})"

def get_column_stats(data, columns):
    stats = {column: Stats() for column in columns}
    # find mins and maxes
    for row in data:
        for column in columns:
            stats[column].min = min(stats[column].min, float(row[column]))
            stats[column].max = max(stats[column].max, float(row[column]))
    return stats

def main():
    input_csv = "../../data/output/project_2_all_games.csv"
    output_csv = "../../data/output/project_2_classification_standardized.csv"

    # Read data from CSV
    with open(input_csv, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        data = list(reader)

    # clean/reformat columns
    cleaned_data = []
    for row in data:
        # skip if white or black times has negative values
        skip = False
        for time in map(float, row["WhiteTimes"][1:-1].split(", ")):
            if time < 0:
                skip = True
                break
        if skip:
            continue
        for time in map(float, row["BlackTimes"][1:-1].split(", ")):
            if time < 0:
                skip = True
                break
        if skip:
            continue

        # Set new column to which player was higher rated
        row["BetterPlayer"] = 1 if float(row["EloDifference"]) >= 0 else 0
        # make elo diff absolute
        row["EloDifference"] = abs(float(row["EloDifference"]))
        
        # clean -1's in endgame time cols
        if row["WhiteEndgameTime"] == "-1":
            row["WhiteEndgameTime"] = 0
        if row["BlackEndgameTime"] == "-1":
            row["BlackEndgameTime"] = 0

        # convert Middlegame and Endgame columns to
        # OpeningPlies, MiddlegamePlies, EndgamePlies
        row["OpeningPlies"] = int(row["Middlegame"])
        if row["Endgame"] == "-1":
            row["MiddlegamePlies"] = int(row["TotalPlies"]) - int(row["OpeningPlies"])
            row["EndgamePlies"] = 0
        else:
            row["MiddlegamePlies"] = int(row["Endgame"]) - int(row["OpeningPlies"])
            row["EndgamePlies"] = int(row["TotalPlies"]) - int(row["Endgame"])
        row["OpeningPlies"] /= int(row["TotalPlies"])
        row["MiddlegamePlies"] /= int(row["TotalPlies"])
        row["EndgamePlies"] /= int(row["TotalPlies"])

        cleaned_data.append(row)

    columns_to_normalize = [
        "EloDifference",
        "TotalPlies",
        "OpeningPlies",
        "MiddlegamePlies",
        "EndgamePlies",
        "WhiteOpeningTime",
        "BlackOpeningTime",
        "WhiteMiddlegameTime",
        "BlackMiddlegameTime",
        "WhiteEndgameTime",
        "BlackEndgameTime"
    ]
    column_stats = get_column_stats(cleaned_data, columns_to_normalize)
    print(column_stats)

    # Processed data
    processed_data = []
    for row in cleaned_data:
        processed_row = {}

        # Pass on better player info
        processed_row["BetterPlayer"] = row["BetterPlayer"]

        # one-hot encode result
        processed_row["ResultBlackWin"] = 0
        processed_row["ResultDraw"] = 0
        processed_row["ResultWhiteWin"] = 0
        if row["Result"] == "-1":
            processed_row["ResultBlackWin"] = 1
        elif row["Result"] == "0":
            processed_row["ResultDraw"] = 1
        elif row["Result"] == "1":
            processed_row["ResultWhiteWin"] = 1
        else:
            raise Exception("Invalid Result value")

        # normalization
        for column in columns_to_normalize:
            processed_row[column] = (float(row[column]) - column_stats[column].min) / (column_stats[column].max - column_stats[column].min)

        # one-hot encode termination
        if row["Termination"] == "Normal":
            processed_row["TerminationNormal"] = 1
            processed_row["TerminationTimeForfeit"] = 0
        elif row["Termination"] == "Time forfeit":
            processed_row["TerminationNormal"] = 0
            processed_row["TerminationTimeForfeit"] = 1
        else:
            raise Exception("invalid termination type")

        processed_data.append(processed_row)

    # Write processed data to new CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=processed_data[0].keys())
        writer.writeheader()
        writer.writerows(processed_data)


if __name__ == "__main__":
    main()
