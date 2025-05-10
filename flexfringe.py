import subprocess
import sys
import graphviz

import json
import re
from collections import defaultdict


def flexfringe(*args, **kwargs):
    """Wrapper to call the flexfringe binary

     Keyword arguments:
     position 0 -- input file with trace samples (from flexfringe build)
     position 1 -- location of the FlexFringe build directory (e.g. ../Flexfringe/build/)
     kwargs -- list of key=value arguments to pass as command line arguments
    """
    command = ["--help"]

    if len(kwargs) >= 1:
        command = []
        for key in kwargs:
            command += ["--" + key + "=" + kwargs[key]]

    result = subprocess.run(["./flexfringe", ] + command + [args[0]], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, cwd=args[1])
    print(result.returncode, result.stdout, result.stderr)

    try:
        with open(args[1] + args[0] + ".ff.final.dot") as fh:
            return fh.read()
    except FileNotFoundError:
        pass

    return None


def show(data, filename="output_DFA"):
    """Save a .png representation of the graph in output_DFAs/

      Keyword arguments:
      data -- string formated in graphviz dot language to visualize
      filename -- output file name
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
      """
    with open(model_file_json) as fh:
        data = fh.read()

    data = re.sub(r'\"label\" : \"([^\n|]*)\n([^\n]*)\"', r'"label" : "\1 \2"', data)

    machine = json.loads(data)

    dfa = defaultdict(lambda: defaultdict(str))

    for edge in machine["edges"]:
        dfa[edge["source"]][edge["name"]] = edge["target"]

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
       dfa -- loaded model
       sequence -- space-separated string to accept/reject in dfa
      """

    state = str(start_node_id)
    counter = 0

    for event in sequence.split(" "):
        sym = event.split(":")[0]

        state = dfa[state][sym]

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