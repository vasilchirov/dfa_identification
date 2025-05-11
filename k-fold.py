from math import floor

with open("datasets/100_training_stamina_train.dat") as test_set:
    traces = test_set.read()

rows = traces.split("\n")
train_folds = ['' for _ in range(5)]
test_folds = ['' for _ in range(5)]
fold_size = floor(len(rows) / 5)

for i in range(5):
    if i == 4:
        test_folds[i] = rows[1:][fold_size * i:]
        train_folds[i] = rows[1:][:fold_size * i]
        break
    fr = fold_size * i
    to = fr + fold_size
    test_folds[i] = rows[1:][fr:to]
    train_folds[i] = rows[1:][:fr] + rows[1:][to:]

for i in range(5):
    with open(f"k-fold/stamina_train_100_{i+1}.dat", "w") as f:
        f.write(str(len(train_folds[i])) + " 50\n")
        for row in train_folds[i]:
            f.write(row)
            f.write("\n")
    with open(f"k-fold/stamina_test_100_{i+1}.dat", "w") as f:
        f.write(str(len(test_folds[i])) + " 50\n")
        for row in test_folds[i]:
            f.write(row)
            f.write("\n")
