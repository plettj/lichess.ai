import pandas as pd
from sklearn.linear_model import RidgeClassifier

# Copyright Josiah Plett 2024


def load_data(csv_file):
    data = pd.read_csv(csv_file)

    data = data[
        [
            "BetterPlayer",
            "ResultBlackWin",
            "ResultDraw",
            "ResultWhiteWin",
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
            "BlackEndgameTime",
            "TerminationNormal",
            "TerminationTimeForfeit"
        ]
    ]

    # Separate features and target variable
    X = data.drop(["ResultBlackWin", "ResultDraw", "ResultWhiteWin"], axis=1).to_numpy()
    y = data[["ResultBlackWin", "ResultDraw", "ResultWhiteWin"]].to_numpy().argmax(axis=1)

    return X, y


def main():
    input_csv = "../../data/output/project_2_classification_standardized.csv"

    X, y = load_data(input_csv)
    lam = 2.8117686979742253e-06

    model = RidgeClassifier(alpha=lam)
    model.fit(X, y)

    model  # <-- here it is, the trained model


if __name__ == "__main__":
    main()
