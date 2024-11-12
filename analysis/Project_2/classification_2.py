import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt

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
    X = data.drop(["ResultBlackWin", "ResultDraw", "ResultWhiteWin"], axis=1)
    y = data[["ResultBlackWin", "ResultDraw", "ResultWhiteWin"]].values.argmax(axis=1)

    return X, y


def evaluate_ridge_classifier(X, y, lambdas, K=10):
    """
    Evaluate Ridge Classification with different regularization parameters using K-fold cross-validation.
    Returns the mean cross-validation error for each lambda.
    """
    cv_errors = []
    kf = KFold(n_splits=K, shuffle=True)

    for lam in lambdas:
        model = RidgeClassifier(alpha=lam)
        # 1 - accuracy is equal to error rate
        error_scores = 1 - cross_val_score(model, X, y, cv=kf, scoring="accuracy")
        mean_error = np.mean(error_scores)
        cv_errors.append(mean_error)

    return cv_errors


def plot_errors(lambdas, cv_errors):
    """
    Plot the estimated generalization error as a function of lambda.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(lambdas, cv_errors, marker="o")
    plt.xscale("log")
    plt.xlabel("Lambda (Regularization Parameter)")
    plt.ylabel("Error (1 - accuracy)")
    plt.title("Generalization Error vs Lambda")
    plt.grid(True)
    plt.show()


def main():
    input_csv = "../../data/output/project_2_classification_standardized.csv"

    X, y = load_data(input_csv)

    lambdas = np.logspace(-3, 5, 100)

    # Evaluate Ridge Regression for different lambdas
    cv_errors = evaluate_ridge_classifier(X, y, lambdas)

    # Plot the generalization error as a function of lambda
    plot_errors(lambdas, cv_errors)

    # Output the optimal lambda value
    optimal_lambda = lambdas[np.argmin(cv_errors)]
    print(f"The optimal lambda value is: {optimal_lambda}")


if __name__ == "__main__":
    main()
