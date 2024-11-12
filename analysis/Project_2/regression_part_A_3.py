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

    # Full model with all parameters
    full_data = data[
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

    X_reduced = data[
        [
            "WhiteTotalTime",
            "BlackTotalTime",
        ]
    ]
    X_full = full_data.drop("TotalPlies", axis=1)
    y = full_data["TotalPlies"]

    return X_full, X_reduced, y


def evaluate_ridge_regression(X, y, lambdas, K=10):
    """
    Evaluate Ridge Regression with different regularization parameters using K-fold cross-validation.
    Returns the mean cross-validation error for each lambda.
    """
    cv_errors = []
    # Set random state to an arbitrary number so we can reproduce results + decrease variance.
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


def plot_errors(lambdas, cv_errors_full, cv_errors_reduced):
    """
    Plot the estimated generalization error as a function of lambda for both models.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(
        lambdas,
        cv_errors_full,
        marker="o",
        label="Full Model (All Parameters)",
    )
    plt.plot(
        lambdas,
        cv_errors_reduced,
        marker="o",
        label="Reduced Model (WhiteTotalTime, BlackTotalTime)",
        color="red",
    )
    plt.xscale("log")
    plt.xlabel("Lambda (Regularization Parameter)")
    plt.ylabel("Mean Squared Error")
    plt.title("Generalization Error vs Lambda")
    plt.legend()
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

    X_full, X_reduced, y = load_data(input_csv)

    # Define a range of lambdas to search for optimal value
    lambdas = np.logspace(-1, 4, 100)

    # Evaluate Ridge Regression for different lambdas for both models
    cv_errors_full = evaluate_ridge_regression(X_full, y, lambdas)
    cv_errors_reduced = evaluate_ridge_regression(X_reduced, y, lambdas)

    # Plot the generalization error as a function of lambda for both models
    plot_errors(lambdas, cv_errors_full, cv_errors_reduced)

    # Output the optimal lambda value for the full model
    optimal_lambda_full = lambdas[np.argmin(cv_errors_full)]
    print(f"The optimal lambda value for the full model is: {optimal_lambda_full}")

    # Output the optimal lambda value for the reduced model
    optimal_lambda_reduced = lambdas[np.argmin(cv_errors_reduced)]
    print(
        f"The optimal lambda value for the reduced model is: {optimal_lambda_reduced}"
    )

    # Print coefficients of the plain linear model and the best-performing ridge model for the full model
    print("\nFull Model Coefficients:")
    print_model_coefficients(X_full, y, optimal_lambda_full)

    # Print coefficients of the plain linear model and the best-performing ridge model for the reduced model
    print("\nReduced Model Coefficients:")
    print_model_coefficients(X_reduced, y, optimal_lambda_reduced)


if __name__ == "__main__":
    main()
