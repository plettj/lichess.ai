import pandas as pd


def calculate_win_loss_percentages(csv_file):
    data = pd.read_csv(csv_file)

    total_games = len(data)
    wins = data[data["Result"] == 1].shape[0]
    losses = data[data["Result"] == -1].shape[0]

    win_percentage = wins / total_games * 100
    loss_percentage = losses / total_games * 100

    win_versus_loss_percentage = wins / losses * 100

    return win_percentage, loss_percentage, win_versus_loss_percentage


def main():
    csv_file = "../data/output/project_2_all_games.csv"
    win_percentage, loss_percentage, win_versus_loss_percentage = (
        calculate_win_loss_percentages(csv_file)
    )

    print(f"Percentage of games won by White: {win_percentage:.2f}%")
    print(f"Percentage of games won by Black: {loss_percentage:.2f}%")
    print(
        f"Percent more games won by White than Black: {win_versus_loss_percentage:.2f}%"
    )


if __name__ == "__main__":
    main()
