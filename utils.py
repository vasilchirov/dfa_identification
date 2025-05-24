def remove_duplicate_traces(traces: str) -> str:
    """
    Function to remove duplicate traces from a traces string

    :param traces: traces string
    :return: unique traces string
    """
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

    return "\n".join(new_rows)


def prepare_test_set(test: list[str], train: list[str]):
    """
    Removes duplicate traces from a test traces array

    :param test: list of test traces
    :param train: list of train traces
    :return: unique test traces array
    """
    train_set = set(train)
    test_set = set()
    new_test = []
    for trace in test:
        if trace in train_set or trace in test_set:
            continue
        new_test.append(trace)
        test_set.add(trace)

    return new_test
