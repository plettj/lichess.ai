"""
REGRESSION - PART A - PART 1

QUESTION:

Explain what variable is predicted based on which other variables and what
you hope to accomplish by the regression. Mention your feature transformation
choices such as one-of-K coding. Since we will use regularization momentarily,
apply a feature transformation to your data matrix X such that each column
has mean 0 and standard deviation 1.

ANSWER:

We are predicting Total Plies based on other attributes that are related to
game length. They are: Elo Difference (unsigned), Middlegame, White Opening
Time,  Black Opening Time, White Total Time, Black Total Time, and Termination.

Elo Difference is unsigned because we care about the difference in skill, not
just how much better White is. Middlegame is the ply where the middlegame began.
Attributes ending in Time are the percentage of total time (180 seconds) that
was used during that period, between 0 and 1. Termination is nominal, either
"Normal" or "Time forfeit."

We hope to predict Total Moves with better accuracy than simply looking at Total
Time, which would show that the other attributes we've included, such as time
usage in the opening, have statistically significant effects on the length of
the game.

We have applied a feature transformation to the continuous attributes — all
except Termination — to set their mean to 0 and standard deviation to 1.
"""

"""
STANDARDIZATION
"""

import csv

# Copyright Josiah Plett 2024


def standardize_data(data, columns_to_standardize):
    means = {}
    stds = {}

    print("Collecting column values for standardization...")

    column_data = {col: [] for col in columns_to_standardize}
    for row in data:
        for col in columns_to_standardize:
            try:
                value = float(row[col])
            except ValueError:
                value = 0.0  # Handle missing or invalid data
            column_data[col].append(value)

    print("Computing means and standard deviations...")

    for col in columns_to_standardize:
        values = column_data[col]
        mean = sum(values) / len(values)
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        means[col] = mean
        stds[col] = std if std != 0 else 1  # Prevent division by zero

    print("Standardizing the data...")

    rows = 0
    for row in data:
        for col in columns_to_standardize:
            try:
                value = float(row[col])
                standardized_value = (value - means[col]) / stds[col]
                row[col] = standardized_value
            except ValueError:
                print(f"Invalid data in column {col}: {row[col]}")
                row[col] = 0.0  # Handle missing or invalid data
        rows += 1
        if rows % 2000 == 0:
            print(f"Standardized {rows} rows...")

    return data


def main():
    input_csv = "../../data/output/project_2_part_a_1_pre.csv"
    output_csv = "../../data/output/project_2_standardized.csv"

    columns_to_standardize = [
        "TotalPlies",
        "EloDifference",
        "Middlegame",
        "WhiteOpeningTime",
        "BlackOpeningTime",
        "WhiteTotalTime",
        "BlackTotalTime",
    ]

    # Read data from CSV
    with open(input_csv, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        data = list(reader)
        fieldnames = reader.fieldnames

    # Standardize data
    standardized_data = standardize_data(data, columns_to_standardize)

    # Write standardized data to new CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(standardized_data)


if __name__ == "__main__":
    main()
