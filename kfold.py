from math import floor

import utils
import numpy as np


def generate_k_folds(k: int, file_name):
    """
    Generates k-fold files from a given traces file

    :param k: number of folds
    :param file_name: path to the traces file
    """
    with open(file_name) as test_set:
        traces = test_set.read()
    rows = traces.split("\n")

    header = rows[0]
    data_rows = rows[1:]
    np.random.shuffle(data_rows)
    data_rows.remove("") if "" in data_rows else data_rows
    train_folds = [[] for _ in range(k)]
    test_folds = [[] for _ in range(k)]
    fold_size = floor(len(data_rows) / k)

    for i in range(k):
        if i == k - 1:
            test_folds[i] = data_rows[1:][fold_size * i:]
            train_folds[i] = data_rows[1:][:fold_size * i]
            test_folds[i] = utils.prepare_test_set(test_folds[i], train_folds[i])
            break
        fr = fold_size * i
        to = fr + fold_size
        test_folds[i] = data_rows[1:][fr:to]
        train_folds[i] = data_rows[1:][:fr] + data_rows[1:][to:]
        test_folds[i] = utils.prepare_test_set(test_folds[i], train_folds[i])

    for i in range(k):
        with open("kfold/" + file_name.split("/")[-1] + f"_train_{i + 1}.dat", "w") as f:
            f.write(str(len(train_folds[i])) + " " + str(header.split(" ")[1]) + "\n")
            for j in range(len(train_folds[i])):
                f.write(train_folds[i][j])
                if j != len(train_folds[i]) - 1:
                    f.write("\n")
        with open("kfold/" + file_name.split("/")[-1] + f"_test_{i + 1}.dat", "w") as f:
            f.write(str(len(test_folds[i])) + " " + str(header.split(" ")[1]) + "\n")
            for j in range(len(test_folds[i])):
                f.write(test_folds[i][j])
                if j != len(test_folds[i]) - 1:
                    f.write("\n")
