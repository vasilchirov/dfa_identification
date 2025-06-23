import subprocess
import graphviz

import json
import re
from collections import defaultdict

import count_nodes


def flexfringe(*args, **kwargs) -> tuple[str | None, int, bool]:
    """Wrapper to call the FlexFringe binary

     Keyword arguments:
    - position 0 -- path to input file with trace samples (from flexfringe root)
    - position 1 -- location of the FlexFringe root directory (e.g. ../Flexfringe/)
    - kwargs -- list of key=value arguments to pass as command line arguments

    :return: tuple of: resulting dfa as str, number of states in the dfa, satisfiable or not (false when satsolver mode is not selected)
    """
    command = ["--help"]

    if len(kwargs) >= 1:
        command = []
        for key in kwargs:
            command += ["--" + key + "=" + kwargs[key]]

    try:
        result = subprocess.run(["./build/flexfringe", ] + command + [args[0]], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, universal_newlines=True, cwd=args[1], timeout=300)

        print(result.returncode, result.stdout, result.stderr)

        is_satisfiable = False

        if "mode" in kwargs.keys() and kwargs["mode"] == "satsolver":
            with open("logs/DELETE_tracker_binsearch_exp_2000.txt", "a") as f:
                if "SATISFIABLE" in result.stderr.split("\n"):
                    print("<<<<SATISFIABLE>>>>")
                    f.write("<<<<SATISFIABLE>>>>\n")
                    is_satisfiable = True
                elif "UNSATISFIABLE" in result.stderr.split("\n"):
                    print("<<<<UNSATISFIABLE>>>>")
                    f.write("<<<<UNSATISFIABLE>>>>\n")
                else:
                    print("<<<<NEITHER?>>>>")
                    f.write("<<<<NEITHER?>>>>\n")

        try:
            with open(args[1] + args[0] + ".ff.final.dot") as fh:
                state_count = count_nodes.count_states(args[1] + args[0] + ".ff.final.dot")
                print(state_count)
                return fh.read(), state_count, is_satisfiable
        except FileNotFoundError as e:
            print(e)

        return None, 0, is_satisfiable
    except subprocess.TimeoutExpired:
        print("<<<<TIMEOUT>>>>")
        with open("logs/DELETE_tracker_binsearch_exp_2000.txt", "a") as f:
            f.write("<<<<TIMEOUT>>>>\n")
        return "timeout", -1, False


def show(data, filename="output_DFA"):
    """Save a .png representation of the graph in output_DFAs/

     Keyword arguments:
    - data -- string formated in graphviz dot language to visualize
    - filename -- output file name
    """
    if not data:
        pass
    else:
        g = graphviz.Source(data, format="png")
        g.render("output_DFAs/" + filename, cleanup=True)


def load_model(model_file_json: str):
    """Wrapper to load resulting model json file

       Keyword arguments:
       model_file_json -- path to the json model file

       :return: tuple[start_node, dfa as dict, json as dict]
      """
    with open(model_file_json) as fh:
        data = fh.read()

    data = re.sub(r'\"label\" : \"([^\n|]*)\n([^\n]*)\"', r'"label" : "\1 \2"', data)

    machine = json.loads(data)

    dfa = defaultdict(lambda: defaultdict(str))

    for edge in machine["edges"]:
        dfa[str(edge["source"])][str(edge["label"])] = str(edge["target"])

    # somtimes in the json of the inferred dfa accepting states are marked 0 and not 1
    if machine['types'][0] == "0":
        is_accepting_1 = True
    else:
        is_accepting_1 = False

    for node in machine["nodes"]:
        if 'final_counts' not in node['data'].keys():
            node_type = '-1'
        elif '0' in node['data']['final_counts'].keys() and node['data']['final_counts']['0'] > 0:
            if is_accepting_1:
                node_type = '0'
            else:
                node_type = '1'
        elif '1' in node['data']['final_counts'].keys() and node['data']['final_counts']['1'] > 0:
            if is_accepting_1:
                node_type = '1'
            else:
                node_type = '0'
        else:
            node_type = '-1'

        dfa[str(node['id'])]["type"] = node_type

    return machine["nodes"][0]["id"], dfa, machine


def traverse(start_node_id, dfa, sequence):
    """Wrapper to traverse a given model with a string

     Keyword arguments:
    - dfa -- loaded model
    - sequence -- space-separated string to accept/reject in dfa
      """

    state = str(start_node_id)
    counter = 0

    for event in sequence.split(" "):
        sym = event.split(":")[0]
        try:
            state = dfa[state][sym]
        except KeyError:
            return False

        counter += 1
        # if state == "":
        #     print("Out of alphabet: non-existent")
        # else:
        #     try:
        #         # take target id, discard counts
        #         state = state[0]
        #     except IndexError:
        #         # print("Out of alphabet: alternatives")
        #         return -1

    return dfa[state]["type"] == '1'


def calculate_accuracy(test_traces, start_node_id, dfa_model):
    """
    Function that calculates the accuracy of an inferred DFA model

    :param test_traces: unseen test traces
    :param start_node_id: id of the start node of the DFA
    :param dfa_model: loaded model
    :return: the following array [#tp, #tn, #fp, #fn, # correct predictions, total number of predictions, bcr accuracy]
    """
    rows = test_traces.split("\n")
    samples = []

    for i in range(len(rows)):
        if i == 0:
            continue
        path = rows[i].split(" ")
        samples.append([" ".join(path[2:]), path[0]])

    counter = 0
    tp = 0;
    tn = 0;
    fp = 0;
    fn = 0
    for sample in samples:
        if sample[1] == '1':
            is_positive = True
        else:
            is_positive = False

        is_accepted = traverse(start_node_id, dfa_model, sample[0])

        if is_accepted == is_positive:
            counter += 1
        if is_accepted:
            if is_positive:
                tp += 1
            else:
                fp += 1
        else:
            if is_positive:
                fn += 1
            else:
                tn += 1
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 1
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 1
    bcr = 2 * sensitivity * specificity / (sensitivity + specificity)
    return [tp, tn, fp, fn, counter, len(samples), bcr]
