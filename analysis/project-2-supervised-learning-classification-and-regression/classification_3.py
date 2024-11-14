import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.dummy import DummyClassifier
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
    X = data.drop(["ResultBlackWin", "ResultDraw", "ResultWhiteWin"], axis=1).to_numpy()
    y = data[["ResultBlackWin", "ResultDraw", "ResultWhiteWin"]].to_numpy().argmax(axis=1)

    return X, y


def nested_cv(X, y, lambdas, tree_complexities, K1, K2):
    out_tc_optimal = []
    out_error_rate_tree = []  # E_test
    out_lam_optimal = []
    out_error_rate_regression = []  # E_test
    out_error_rate_baseline = []  # E_test

    fold_ctr = 0
    outer_cv = KFold(n_splits=K1, shuffle=True)
    for par_idx, test_idx in outer_cv.split(X):
        X_par = X[par_idx, :]
        y_par = y[par_idx]
        X_test = X[test_idx, :]
        y_test = y[test_idx]

        inner_cv = KFold(n_splits=K2, shuffle=True)

        # inner cv on tree model
        tc_optimal = 0
        min_tree_error = np.inf
        for tc in tree_complexities:
            tree_model = DecisionTreeClassifier(criterion="gini", max_depth=tc)
            error = 1 - cross_val_score(tree_model, X_par, y_par, cv=inner_cv, scoring="accuracy")
            mean_error = np.mean(error)
            if mean_error < min_tree_error:
                min_tree_error = mean_error
                tc_optimal = tc

        # inner cv on regression model
        lam_optimal = 0
        min_regression_error = np.inf
        for lam in lambdas:
            regression_model = RidgeClassifier(alpha=lam)
            error = 1 - cross_val_score(regression_model, X_par, y_par, cv=inner_cv, scoring="accuracy")
            mean_error = np.mean(error)
            if mean_error < min_regression_error:
                min_regression_error = mean_error
                lam_optimal = lam
        
        # test models against test set
        tree_model = DecisionTreeClassifier(criterion="gini", max_depth=tc_optimal)
        regression_model = RidgeClassifier(alpha=lam_optimal)
        baseline_model = DummyClassifier(strategy="most_frequent")

        tree_model.fit(X_par, y_par)
        regression_model.fit(X_par, y_par)
        baseline_model.fit(X_par, y_par)

        n_tree_misclassifications = np.not_equal(tree_model.predict(X_test), y_test).sum()
        n_regression_misclassifications = np.not_equal(regression_model.predict(X_test), y_test).sum()
        n_baseline_misclassifications = np.not_equal(baseline_model.predict(X_test), y_test).sum()

        error_rate_tree = n_tree_misclassifications / y_test.shape[0]
        error_rate_regression = n_regression_misclassifications / y_test.shape[0]
        error_rate_baseline = n_baseline_misclassifications / y_test.shape[0]

        out_tc_optimal.append(tc_optimal)
        out_error_rate_tree.append(error_rate_tree)
        out_lam_optimal.append(lam_optimal)
        out_error_rate_regression.append(error_rate_regression)
        out_error_rate_baseline.append(error_rate_baseline)

        fold_ctr += 1

        print(f"Outer Fold {fold_ctr}")
        print( "---------------------")
        print(f"(DecisionTreeClassifier) Optimal Max Depth: {tc_optimal}")
        print(f"(DecisionTreeClassifier) Test Error: {error_rate_tree}")
        print(f"(RidgeClassifier) Optimal Regularization Parameter: {lam_optimal}")
        print(f"(RidgeClassifier) Test Error: {error_rate_regression}")
        print(f"(DummyClassifier) Test Error: {error_rate_baseline}")
        print()
    return out_tc_optimal, out_error_rate_tree, out_lam_optimal, out_error_rate_regression, out_error_rate_baseline


def plot_errors(tc_optimal, error_tree, lam_optimal, error_regression, error_baseline):
    """
    Plot the estimated generalization error as a function of lambda.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(lam_optimal) + 1), lam_optimal, marker="o")
    plt.plot(range(1, len(error_regression) + 1), error_regression, marker="x")
    plt.xscale("log")
    plt.xlabel("Outer Fold")
    plt.ylabel("Lambda (o) / Error Rate (x)")
    plt.title("Outer Fold Results for RidgeClassifier")
    plt.grid(True)
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(tc_optimal) + 1), tc_optimal, marker="o")
    plt.plot(range(1, len(error_tree) + 1), error_tree, marker="x")
    plt.xscale("log")
    plt.xlabel("Outer Fold")
    plt.ylabel("Max Depth (o) / Error Rate (x)")
    plt.title("Outer Fold Results for DecisionTreeClassifier")
    plt.grid(True)
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(error_baseline) + 1), error_baseline, marker="x")
    plt.xscale("log")
    plt.xlabel("Outer Fold")
    plt.ylabel("Error Rate (x)")
    plt.title("Outer Fold Results for DummyClassifier")
    plt.grid(True)
    plt.show()


def main():
    input_csv = "../../data/output/project_2_classification_standardized.csv"

    X, y = load_data(input_csv)
    lambdas = np.logspace(-8, 0, 50)
    tree_complexities = np.arange(2, 21, 1)

    tc_optimal, error_tree, lam_optimal, error_regression, error_baseline = nested_cv(X, y, lambdas, tree_complexities, 10, 10)

    print("Tree Complexity*:", tc_optimal)
    print("Test Error (Tree):", error_tree)
    print("Lambda*: lam_optimal", lam_optimal)
    print("Test Error (Regression):", error_regression)
    print("Test Error (Baseline):", error_baseline)

    plot_errors(tc_optimal, error_tree, lam_optimal, error_regression, error_baseline)


if __name__ == "__main__":
    main()
