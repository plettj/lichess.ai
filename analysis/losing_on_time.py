import pandas as pd


def calculate_time_forfeit_percentage(csv_file):
    data = pd.read_csv(csv_file)

    total_games = len(data)
    time_forfeit_games = data[data["Termination"] == "Time forfeit"].shape[0]
    time_forfeit_percentage = (time_forfeit_games / total_games) * 100

    return time_forfeit_percentage


def main():
    csv_file = "../data/output/project_2_all_games.csv"
    time_forfeit_percentage = calculate_time_forfeit_percentage(csv_file)
    print(
        f"Percentage of games lost on time (Time forfeit): {time_forfeit_percentage:.2f}%"
    )


if __name__ == "__main__":
    main()
