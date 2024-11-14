import numpy as np
import pandas as pd
from scipy.stats import beta, binom
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import KFold, cross_val_score

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
    out_tree_y_pred = []
    out_regression_y_pred = []
    out_baseline_y_pred = []
    out_y = []

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

        tree_y_pred = tree_model.predict(X_test)
        regression_y_pred = regression_model.predict(X_test)
        baseline_y_pred = baseline_model.predict(X_test)

        n_tree_misclassifications = np.not_equal(tree_y_pred, y_test).sum()
        n_regression_misclassifications = np.not_equal(regression_y_pred, y_test).sum()
        n_baseline_misclassifications = np.not_equal(baseline_y_pred, y_test).sum()

        error_rate_tree = n_tree_misclassifications / y_test.shape[0]
        error_rate_regression = n_regression_misclassifications / y_test.shape[0]
        error_rate_baseline = n_baseline_misclassifications / y_test.shape[0]

        out_tree_y_pred.extend(tree_y_pred)
        out_regression_y_pred.extend(regression_y_pred)
        out_baseline_y_pred.extend(baseline_y_pred)
        out_y.extend(y_test)

        fold_ctr += 1

        print(f"Outer Fold {fold_ctr}")
        print( "---------------------")
        print(f"(DecisionTreeClassifier) Optimal Max Depth: {tc_optimal}")
        print(f"(DecisionTreeClassifier) Test Error: {error_rate_tree}")
        print(f"(RidgeClassifier) Optimal Regularization Parameter: {lam_optimal}")
        print(f"(RidgeClassifier) Test Error: {error_rate_regression}")
        print(f"(DummyClassifier) Test Error: {error_rate_baseline}")
        print()
    return np.array(out_tree_y_pred), np.array(out_regression_y_pred), np.array(out_baseline_y_pred), np.array(out_y)


def mcnemar_test(y_pred_a, y_pred_b, y_true):
    """
    return p, ci left, ci right
    """
    n = len(y_true)
    c_a = y_pred_a == y_true
    c_b = y_pred_b == y_true

    n12 = np.sum(np.multiply(c_a, 1 - c_b))
    n21 = np.sum(np.multiply(1 - c_a, c_b))
    
    theta_pred = (n12 - n21) / n
    Q = (n**2 * (n + 1) * (theta_pred + 1) * (1 - theta_pred))/(n*(n12 + n21) - (n12 - n21)**2)
    f = (Q - 1) * (theta_pred + 1) / 2
    g = (Q - 1) * (1 - theta_pred) / 2

    if n12 + n21 < 5:
        print("WARNING: n12 + n21 < 5; confidence interval estimation is probably not accurate")

    significance = 0.05
    theta_l = 2*beta.ppf(significance/2, f, g) - 1
    theta_r = 2*beta.ppf(1 - significance/2, f, g) - 1

    print(f"Estimated accuracy difference (A - B): {theta_pred}")
    print(f"Accuracy difference CI (alpha = {significance}): [{theta_l}, {theta_r}]")

    p = 2*binom.cdf(min(n12, n21), n12 + n21, 0.5)
    print(f"p-value: {p}")

    return p, theta_l, theta_r


def main():
    input_csv = "../../data/output/project_2_classification_standardized.csv"

    X, y = load_data(input_csv)
    lambdas = np.logspace(-8, 0, 50)
    tree_complexities = np.arange(2, 21, 1)

    y_pred_tree, y_pred_regression, y_pred_baseline, y_true = nested_cv(X, y, lambdas, tree_complexities, 10, 10)

    print("McNemar's Test: Tree vs. Baseline")
    print("-----------------------------------")
    mcnemar_test(y_pred_tree, y_pred_baseline, y_true)
    print()
    print("McNemar's Test: Regression vs. Baseline")
    print("-----------------------------------------")
    mcnemar_test(y_pred_regression, y_pred_baseline, y_true)
    print()
    print("McNemar's Test: Tree vs. Regression")
    print("-------------------------------------")
    mcnemar_test(y_pred_tree, y_pred_regression, y_true)
    print()


if __name__ == "__main__":
    main()
