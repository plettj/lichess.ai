import numpy as np
import pandas as pd

# Copyright Josiah Plett 2024

def load_data(csv_file):
    data = pd.read_csv(csv_file)

    # Selecting only relevant columns: 'BetterPlayer' for prediction, 'Result' columns for outcome
    data = data[["BetterPlayer", "ResultBlackWin", "ResultDraw", "ResultWhiteWin"]]

    # Target variable: 0 for BlackWin, 1 for Draw, 2 for WhiteWin
    y = data[["ResultBlackWin", "ResultDraw", "ResultWhiteWin"]].values.argmax(axis=1)
    
    # Feature: 'BetterPlayer' (0 = black better, 1 = white better)
    X = data["BetterPlayer"].values
    
    return X, y


def predict_based_on_better_player(X):
    """
    Predicts outcome based on the BetterPlayer column.
    Predict 2 (WhiteWin) if BetterPlayer == 1, else predict 0 (BlackWin).
    """
    predictions = np.where(X == 1, 2, 0)
    return predictions


def calculate_error_rate(y_true, y_pred):
    """
    Calculate the error rate (1 - accuracy) between true labels and predictions.
    """
    accuracy = np.mean(y_true == y_pred)
    error_rate = 1 - accuracy
    return error_rate


def main():
    input_csv = "../../data/output/project_2_classification_standardized.csv"

    # Load data
    X, y = load_data(input_csv)

    # Make predictions based on BetterPlayer
    y_pred = predict_based_on_better_player(X)

    # Calculate error rate (1 - accuracy)
    error_rate = calculate_error_rate(y, y_pred)
    print(f"The error rate (1 - accuracy) for our basic model is: {error_rate * 100:.2f}%")

    # RESULT:
    # Error rate (1 - accuracy) is: 36.64%

if __name__ == "__main__":
    main()
