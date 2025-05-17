import numpy as np

def remove_duplicate_traces(traces: str):
    rows = traces.split("\n")
    seen = set()
    new_rows = []
    for i in range(len(rows)):
        if i == 0:
            new_rows.append(rows[i])
            continue
        if rows[i] in seen:
            continue
        else:
            seen.add(rows[i])
            new_rows.append(rows[i])

    print("LEEEEEVSKI", len(new_rows), len(rows))

    return "\n".join(new_rows)


def prepare_test_set(test: list[str], train: list[str]):
    train_set = set(train)
    test_set = set()
    new_test = []
    for trace in test:
        if trace in train_set or trace in test_set:
            continue
        new_test.append(trace)
        test_set.add(trace)

    return new_test

arr = [1, 2, 3, 4, 5, 6]
np.random.shuffle(arr)
print(arr)