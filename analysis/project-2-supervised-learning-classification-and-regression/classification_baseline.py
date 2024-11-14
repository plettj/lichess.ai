import numpy as np
import pandas as pd

# Copyright Josiah Plett 2024

def load_data(csv_file):
    data = pd.read_csv(csv_file)

    # Target variable: 0 for BlackWin, 1 for Draw, 2 for WhiteWin
    y = data[["ResultBlackWin", "ResultDraw", "ResultWhiteWin"]].values.argmax(axis=1)
    
    return y


def predict_most_common(y):
    """
    Baseline prediction model that always predicts the most common class.
    """
    # Find the most common class in y
    most_common_class = np.bincount(y).argmax()
    predictions = np.full_like(y, fill_value=most_common_class)
    
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
    y = load_data(input_csv)

    # Make predictions based on the most common outcome
    y_pred = predict_most_common(y)

    # Calculate error rate (1 - accuracy)
    error_rate = calculate_error_rate(y, y_pred)
    print(f"The error rate (1 - accuracy) for the baseline model is: {error_rate * 100:.2f}%")

if __name__ == "__main__":
    main()
