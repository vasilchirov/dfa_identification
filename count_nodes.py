def count_states(input_file) -> int:
    """
    Function to count the number of states in the DFA input file (.dot)

    :param input_file: DFA input file (.dot)
    :return: number of states
    """
    with open(input_file, "rb") as f:
        data = str(f.read())

    counter = 0
    for word in data.split(" "):
        if word == "fin:":
            counter += 1

    print("<<<<<<<<<STATE COUNT: " + str(counter) + ">>>>>>>>")
    return counter
