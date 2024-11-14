# exercise 2.1.1
import matplotlib.pyplot as plt
import os
import numpy as np
import csv
from scipy.linalg import svd

dir_path = os.path.dirname(os.path.realpath(__file__))

relevant_attributes = {
    "WhiteElo",
    "BlackElo",
    "EloDifference",
    "Middlegame",
    "Endgame",
    "TotalMoves",
    "Result"
}

# Read data from csv
with open(f"{dir_path}/../data/output/parsed_output.csv") as csvfile:
    reader = csv.reader(csvfile)

    # find which elements of the row to not prune
    attribute_names = next(reader)
    kept_indices = []
    for i in range(len(attribute_names)):
        attr = attribute_names[i]
        if attr in relevant_attributes:
            kept_indices.append(i)
    attribute_names = [attribute_names[i] for i in kept_indices][1:]

    data_matrix = []
    for row in reader:
        data_matrix.append([row[i] for i in kept_indices])
    data_matrix = np.asarray(data_matrix)

# Extract and encode classes
class_labels = [str(class_name) for class_name in data_matrix[:, 0]]
class_names = sorted(set(class_labels))
class_dict = dict(zip(class_names, range(len(class_names))))

# Get vector y
y = np.asarray([class_dict[label] for label in class_labels])

# Get matrix X
X = data_matrix[:, 1:].astype(np.float32)
X = (X - X.mean(axis=0)) / X.std(axis = 0)

# Get N, M, C
N = len(y)
M = len(attribute_names)
C = len(class_names)

# Subtract mean from data
Y = X - X.mean(axis=0).T
Y = Y[:45000, :]

# SVD
U, S, Vh = svd(Y, full_matrices=True)
V = Vh.T

# Get variance via principal components
rho = (S * S) / (S * S).sum()

threshold = 0.9

# Plot variance explained
print(attribute_names)

plt.figure()
plt.plot(range(1, len(rho) + 1), rho, "x-")
plt.plot(range(1, len(rho) + 1), np.cumsum(rho), "o-")
plt.plot([1, len(rho)], [threshold, threshold], "k--")
plt.title("Variance explained by principal components")
plt.xlabel("Principal component")
plt.ylabel("Variance explained")
plt.legend(["Individual", "Cumulative", "Threshold"])
plt.grid()

plt.figure()
pcs = [0, 1, 2, 3, 4]
legendStrs = ["PC" + str(e + 1) for e in pcs]
c = ["r", "g", "b"]
bw = 0.2
r = np.arange(1, M + 1)
for i in pcs:
    plt.bar(r + i * bw, V[:, i], width=bw)
plt.xticks(r + bw, attribute_names)
plt.xlabel("Attributes")
plt.ylabel("Component coefficients")
plt.legend(legendStrs)
plt.grid()
plt.title("Lichess 960: PCA Component Coefficients")
plt.show()
