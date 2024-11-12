"""
REGRESSION - PART A - PART 2

QUESTION:

Introduce a regularization parameter λ as discussed in chapter 14 of the lecture
notes, and estimate the generalization error for different values of λ. Specifi-
cally, choose a reasonable range of values of λ (ideally one where the general-
ization error first drop and then increases), and for each value use K = 10 fold
cross-validation (algorithm 5) to estimate the generalization error.
Include a figure of the estimated generalization error as a function of λ in the
report and briefly discuss the result.

ANSWER:

We experimented with different ranges of regularization parameter λ being applied
to our basic Linear Regression model and assessed them via 10-fold cross-
validation, until we found the global minima and its corresponding λ. The first
graph is the result when using our full 45,343-game standardized data set, and
the second is when using a random 500-game subset.

It's immediately apparent that the change in Mean Squared Error is miniscule at
these global minima. In fact, across the range -10^(-6) < λ < 10^(2) on both
datasets, the Mean Squared Error never deviates by more than 0.005.

Due to our highly variable yet undoubtedly correlated game data, it makes sense
that regularization doesn't have a big effect. Linear regression relies on plain
old probabilities more than other models, so given how linear in nature our data
is, "punishing overfitting" isn't really very punishing.

Put simply, linear regression is so good at its job on our data that regulariza-
tion can barely help.

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


def main():
    input_csv = "../../data/output/project_2_part_a_standardized.csv"

    X, y = load_data(input_csv)

    # Attempt 1: 10^-4 to 10^4, 16 instances
    # 251.2
    # Attempt 2: 10^-6 to 10^6, 80 instances
    # 455.2
    # Attempt 3: 10^1.5 to 10^3.5, 80 instances
    # 519.0
    # TRANSITION TO LINEAR SCALE
    # Attempt 4: 250 to 750, 50 instances
    # 525.5
    # Attempt 5: 50 to 1000, 100 instances
    # 520.0
    lambdas = np.linspace(50, 1000, 100)

    # Evaluate Ridge Regression for different lambdas
    cv_errors = evaluate_ridge_regression(X, y, lambdas)

    # Plot the generalization error as a function of lambda
    plot_errors(lambdas, cv_errors)

    # Output the optimal lambda value
    optimal_lambda = lambdas[np.argmin(cv_errors)]
    print(f"The optimal lambda value is: {optimal_lambda}")


if __name__ == "__main__":
    main()
