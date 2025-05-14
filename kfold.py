from math import floor

def generate_k_folds(k: int, file_name):
    with open(file_name) as test_set:
        traces = test_set.read()

    rows = traces.split("\n")
    train_folds = ['' for _ in range(k)]
    test_folds = ['' for _ in range(k)]
    fold_size = floor(len(rows) / k)

    for i in range(k):
        if i == k - 1:
            test_folds[i] = rows[1:][fold_size * i:]
            train_folds[i] = rows[1:][:fold_size * i]
            break
        fr = fold_size * i
        to = fr + fold_size
        test_folds[i] = rows[1:][fr:to]
        train_folds[i] = rows[1:][:fr] + rows[1:][to:]

    for i in range(k):
        with open("kfold/" + file_name.split("/")[-1] + f"_train_{i+1}.dat", "w") as f:
            f.write(str(len(train_folds[i])) + " 50\n")
            for j in range(len(train_folds[i])):
                f.write(train_folds[i][j])
                if j != len(train_folds[i]) - 1:
                    f.write("\n")
        with open("kfold/" + file_name.split("/")[-1] + f"_test_{i+1}.dat", "w") as f:
            f.write(str(len(test_folds[i])) + " 50\n")
            for j in range(len(test_folds[i])):
                f.write(test_folds[i][j])
                if j != len(test_folds[i]) - 1:
                    f.write("\n")
