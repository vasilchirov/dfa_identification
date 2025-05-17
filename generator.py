import sys
import json
import numpy as np
import random
import copy


### Argument parsing

# The command line arguments. File name is always the first argument
arguments: list = sys.argv
arguments_length: int = len(arguments) # Amount of arguments
# file_name: str = str(input("File/dir name: ") if (arguments_length < 2) else arguments[1])
accepting_count = input("Amount of accepting samples: ") if (arguments_length < 3) else arguments[2]
rejecting_count = input("Amount of rejecting samples: ") if (arguments_length < 4) else arguments[3]
output_file_name: str = str(input("Output file name: ") if (arguments_length < 5) else arguments[4])


### Class Definitions ###

class Edge:

    source: int
    target: int
    symbol: int


    def __init__(self, source, target, symbol):
        self.source = source
        self.target = target
        self.symbol = symbol


    # Create the string representation
    def __repr__(self):
        return str(self)


    # In the form of "source --symbol-> target"
    def __str__(self):
        return "{} --{}-> {}".format(self.source, self.symbol, self.target)



class Node:

    id: int
    edges: dict[int, Edge]
    accept: bool


    def __init__(self, id, edges, accept = False):
        self.id = id
        self.edges = edges
        self.accept = accept


    # Add/remove edges using +/-
    def __add__(self, other):
        self.edges[other.symbol] = other
        return self


    def __sub__(self, other):
        del self.edges[other.symbol]
        return self


    # Create the string representation
    def __repr__(self):
        return str(self)


    # The ID, surrounded by () if accepting
    def __str__(self):
        return "({})".format(self.id) if self.accept else str(self.id)



class DFA:
    alphabet: list[int]
    nodes: dict[int, Node]
    edges: list[Edge]
    # Start is assumed to be -1


    def __init__(self, alphabet = [], nodes = {}, edges = []):
        self.alphabet = alphabet
        self.nodes = nodes
        self.edges = edges


    # Handle nodes using list operators (i.e [key] = value)
    def __getitem__ (self, key) -> Node:
        return self.nodes[key]


    def __setitem__ (self, key, value):
        self.nodes[key] = value


    def __delitem__ (self, key):
        del self.nodes[key]


    # Add/remove edges using (+/-)
    def __add__ (self, other):
        self.edges.append(other)
        self.nodes[other.source] += other
        return self


    def __sub__ (self, other):
        self.edges.remove(other)
        self.nodes[other.source] -= other.target
        return self


    # Create the string representation
    def __repr__(self):
        return str(self)


    def __str__ (self):
        return """
            Alphabet: {},
            Nodes: {},
            Edges: {}
            """.format(self.alphabet, list(self.nodes.values()), self.edges)


    def simulate(self, word: list[int]) -> bool:
        node_id: int = -1
        node: Node = self.nodes[node_id]

        for symbol in word:
            if symbol not in node.edges or node.edges[symbol].target not in self.nodes:
                return False

            node = self.nodes[node.edges[symbol].target]

        return node.accept

    def generate_forest_fire(self, alphabet_size=2, node_count=10, f=0.31, b=0.385, s=0.2):
        self.alphabet = list(range(alphabet_size))
        self.nodes = {}
        self.edges = []

        # Create initial node (-1 is the start state)
        self[-1] = Node(-1, {}, accept=(random.random() < 0.5))

        def geometric(p):
            return np.random.geometric(p)

        visited = set()
        available_symbols = {node_id: set(self.alphabet) for node_id in range(-1, node_count)}

        for node_id in range(node_count):
            self[node_id] = Node(node_id, {}, accept=(random.random() < 0.5))

            # Choose ambassador from existing nodes
            ambassador_id = random.choice(list(self.nodes.keys() - {node_id}))

            # Create edge from ambassador to new node (to ensure reachability)
            src = ambassador_id
            dst = node_id
            symbols = available_symbols[src]
            if symbols:
                symbol = random.choice(list(symbols))
                self += Edge(src, dst, symbol)
                available_symbols[src].remove(symbol)

            # Forest-fire recursion
            queue = [(dst, src)]  # (new_node, parent)
            seen = set()
            while queue:
                v, parent = queue.pop(0)
                if v in seen:
                    continue
                seen.add(v)

                out_deg = geometric(f)
                in_deg = geometric(f * b)

                neighbors = list(self.nodes.keys())
                random.shuffle(neighbors)
                for neighbor in neighbors:
                    if neighbor == v or neighbor in seen:
                        continue

                    # Forward (out) edge
                    if out_deg > 0 and random.random() < 0.5 and available_symbols[v]:
                        sym = random.choice(list(available_symbols[v]))
                        self += Edge(v, neighbor, sym)
                        available_symbols[v].remove(sym)
                        queue.append((neighbor, v))
                        out_deg -= 1

                    # Backward (in) edge
                    if in_deg > 0 and random.random() < 0.5 and available_symbols[neighbor]:
                        sym = random.choice(list(available_symbols[neighbor]))
                        self += Edge(neighbor, v, sym)
                        available_symbols[neighbor].remove(sym)
                        queue.append((neighbor, v))
                        in_deg -= 1

                # Self-loop with probability s
                if random.random() < s and available_symbols[v]:
                    sym = random.choice(list(available_symbols[v]))
                    self += Edge(v, v, sym)
                    available_symbols[v].remove(sym)

        return self

    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            self.alphabet = data["alphabet"]

            for node in data["nodes"]:
                node_id = int(node["id"])
                is_accepting = "final_counts" in node["data"] and "1" in node["data"]["final_counts"] and node["data"]["final_counts"]["1"] > 0
                self[node_id] = Node(node_id, {}, is_accepting)

            for edge in data["edges"]:
                self += Edge(int(edge["source"]), int(edge["target"]), int(edge["name"]))


class TrainingData:
    dfa: DFA
    words: list[list[int]]

    def __init__(self, dfa=None, words=[]):
        self.dfa = dfa
        self.words = words

    def _random_walk(self, max_length=100):
        """
        Perform a random walk starting from the initial state (-1),
        returning a list of symbols representing a word.
        """
        word = []
        current = self.dfa.nodes[-1]
        while len(word) < max_length:
            edges = list(current.edges.values())
            if not edges:
                break

            edge = random.choice(edges)
            word.append(edge.symbol)
            current = self.dfa.nodes[edge.target]

            # Termination probability as described in StaMInA
            if random.random() < 1.0 / (1 + 2 * len(current.edges)):
                break
        return word

    def _depth(self):
        """Estimate DFA depth (longest shortest path from -1) using BFS."""
        from collections import deque
        visited = set()
        queue = deque([(-1, 0)])
        max_depth = 0

        while queue:
            node_id, depth = queue.popleft()
            visited.add(node_id)
            max_depth = max(max_depth, depth)
            for edge in self.dfa.nodes[node_id].edges.values():
                if edge.target not in visited:
                    queue.append((edge.target, depth + 1))
        return max_depth

    def generate_positive(self, count) -> object:
        self.words = []
        depth = self._depth()
        target_mean_length = 5 + depth
        max_attempts = count * 20

        while len(self.words) < count and max_attempts > 0:
            word = []
            node = self.dfa.nodes[-1]
            visited = set()
            steps = int(np.random.normal(loc=target_mean_length, scale=3))
            steps = max(1, min(steps, 2 * target_mean_length))  # Clamp to [1, 2×mean]

            for _ in range(steps):
                if not node.edges:
                    break

                # Higher chance to revisit "hub" nodes
                out_edges = list(node.edges.values())
                weights = [len(self.dfa.nodes[edge.target].edges) + 1 for edge in out_edges]
                edge = random.choices(out_edges, weights=weights, k=1)[0]

                word.append(edge.symbol)
                node = self.dfa.nodes[edge.target]

                # Probabilistic stop based on node's out-degree
                stop_chance = 1.0 / (1 + 2 * len(node.edges))
                if random.random() < stop_chance:
                    break

            if self.dfa.simulate(word):
                self.words.append(word)

            max_attempts -= 1
        return self

    def _edit_word(self, word):
        """Create a negative sample by editing a positive sample."""
        alphabet = self.dfa.alphabet
        max_edits = np.random.poisson(3)
        word = word.copy()

        for _ in range(max_edits):
            if not word:
                break

            operation = random.choice(["substitute", "insert", "delete"])
            index = random.randint(0, len(word) - 1) if word else 0

            if operation == "substitute":
                symbol = random.choice(alphabet)
                word[index] = symbol
            elif operation == "insert":
                symbol = random.choice(alphabet)
                word.insert(index, symbol)
            elif operation == "delete" and word:
                word.pop(index)

        return word

    def generate_negatives(self, count) -> object:
        """Generate `count` negative sequences by editing positives."""
        positives = self.words.copy()
        attempts = 0
        max_attempts = count * 10  # Avoid infinite loops

        while len(self.words) < len(positives) + count and attempts < max_attempts:
            pos = random.choice(positives)
            neg = self._edit_word(pos)
            if not self.dfa.simulate(neg):
                self.words.append(neg)
            attempts += 1
        return self

    def shuffle(self):
        np.random.shuffle(self.words)

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = ""
        for word in self.words:
            is_accepting = "1" if self.dfa.simulate(word) else "0"
            word_length = len(word)
            result += "\n{} {}".format(is_accepting, word_length)
            for symbol in word:
                result += " " + str(symbol)
        return "{} {}".format(len(self.words), len(self.dfa.alphabet)) + result

### Insert your own code here! ###
### Or don't! """"

# Create a sample DFA with alphabet { 0, 1 } and 10 states
example_dfa = DFA()
# example_dfa.load_from_file(file_name)
example_dfa.generate_forest_fire(50, 50)
print(example_dfa)

# Create testing data and shuffle it
example_data = TrainingData(example_dfa)
example_data.generate_positive(int(accepting_count))
example_data.generate_negatives(int(rejecting_count))
example_data.shuffle()
example_data.save_to_file(output_file_name)
print(example_data)
