"""
REGRESSION - PART A - PART 3

QUESTION:

Explain how the output, y, of the linear model with the lowest generalization
error (as determined in the previous question) is computed for a given input
x. What is the effect of an individual attribute in x on the output, y, of the
linear model? Does the effect of individual attributes make sense based on your
understanding of the problem?

ANSWER:

TBD
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt

# Copyright Josiah Plett 2024


def load_data(csv_file):
    data = pd.read_csv(csv_file)

    data = data[
        [
            "TotalPlies",
            "EloDifference",
            "Middlegame",
            "WhiteOpeningTime",
            "BlackOpeningTime",
            "WhiteTotalTime",
            "BlackTotalTime",
        ]
    ]

    # Separate features and target variable
    X = data.drop("TotalPlies", axis=1)
    y = data["TotalPlies"]

    return X, y


def evaluate_ridge_regression(X, y, lambdas, K=10):
    """
    Evaluate Ridge Regression with different regularization parameters using K-fold cross-validation.
    Returns the mean cross-validation error for each lambda.
    """
    cv_errors = []
    kf = KFold(n_splits=K, shuffle=True, random_state=42)

    for lam in lambdas:
        model = Ridge(alpha=lam)
        # Use negative mean squared error as scoring because cross_val_score maximizes the score
        mse_scores = cross_val_score(
            model, X, y, cv=kf, scoring="neg_mean_squared_error"
        )
        mean_mse = -np.mean(mse_scores)
        cv_errors.append(mean_mse)

    return cv_errors


def plot_errors(lambdas, cv_errors):
    """
    Plot the estimated generalization error as a function of lambda.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(lambdas, cv_errors, marker="o")
    plt.xscale("log")
    plt.xlabel("Lambda (Regularization Parameter)")
    plt.ylabel("Mean Squared Error")
    plt.title("Generalization Error vs Lambda")
    plt.grid(True)
    plt.show()


def print_model_coefficients(X, y, optimal_lambda):
    """
    Train and print coefficients for:
    1. Plain linear regression (lambda = 0).
    2. Ridge regression with the optimal lambda.
    """
    # Plain linear regression (lambda = 0)
    plain_model = Ridge(alpha=0)  # This behaves like a standard linear regression
    plain_model.fit(X, y)
    print("\nCoefficients of plain linear regression (lambda = 0):")
    for feature, coef in zip(X.columns, plain_model.coef_):
        print(f"{feature}: {coef}")

    # Ridge regression with optimal lambda
    ridge_model = Ridge(alpha=optimal_lambda)
    ridge_model.fit(X, y)
    print(f"\nCoefficients of ridge regression with optimal lambda ({optimal_lambda}):")
    for feature, coef in zip(X.columns, ridge_model.coef_):
        print(f"{feature}: {coef}")


def main():
    input_csv = "../../data/output/project_2_part_a_standardized.csv"

    X, y = load_data(input_csv)

    # Define a range of lambdas to search for optimal value
    lambdas = np.linspace(50, 1000, 100)

    # Evaluate Ridge Regression for different lambdas
    cv_errors = evaluate_ridge_regression(X, y, lambdas)

    # Plot the generalization error as a function of lambda
    plot_errors(lambdas, cv_errors)

    # Output the optimal lambda value
    optimal_lambda = lambdas[np.argmin(cv_errors)]
    print(f"The optimal lambda value is: {optimal_lambda}")

    # Print coefficients of the plain linear model and the best-performing ridge model
    print_model_coefficients(X, y, optimal_lambda)


if __name__ == "__main__":
    main()
