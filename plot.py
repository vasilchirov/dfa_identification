import matplotlib.pyplot as plt
import ast

from matplotlib.ticker import FuncFormatter


def offset_exp_state_count_plot():
    with open("logs/stamina_exp_binsearch_satoffset_apta=1000_log.txt", "r") as f:
        data_1000 = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_satoffset_apta=1500_log.txt", "r") as f:
        data_1500 = f.read().split("\n")

    avg_edsm = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "edsm state count average":
            avg_edsm.append(float(data_1000[i].split(": ")[1]))

    avg_1000 = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "state count average":
            avg_1000.append(float(data_1000[i].split(": ")[1]))

    avg_1500 = []

    for i in range(len(data_1500)):
        if data_1500[i].split(": ")[0] == "state count average":
            avg_1500.append(float(data_1500[i].split(": ")[1]))

    min_len = min(len(avg_1000), len(avg_1500), len(avg_edsm))
    avg_1000 = avg_1000[:min_len]
    avg_1500 = avg_1500[:min_len]
    avg_edsm = avg_edsm[:min_len]

    # Generate x-axis values as multiples of 5
    x_values = [5 * (i + 1) for i in range(min_len)]

    # Plot the differences
    diff_1000_edsm = [b - a for a, b in zip(avg_edsm, avg_1000)]
    diff_1500_edsm = [c - a for a, c in zip(avg_edsm, avg_1500)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_1000_edsm, label="apta 1000", marker='o')
    plt.plot(x_values, diff_1500_edsm, label="apta 1500", marker='x')
    plt.title("State count difference compared to a full EDSM run (Average from 5-fold cv) (offset experiment)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("Difference")
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def offset_exp_bcr_plot():
    with open("logs/stamina_exp_binsearch_satoffset_apta=1000_log.txt", "r") as f:
        data_1000 = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_satoffset_apta=1500_log.txt", "r") as f:
        data_1500 = f.read().split("\n")

    bcrs_edsm = []

    bcrs_1000 = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "bcr edsm":
            bcrs_edsm.append(float(data_1000[i].split(": ")[1]))
            bcrs_1000.append(float(data_1000[i+1].split(": ")[1]))

    bcrs_1500 = []

    for i in range(len(data_1500)):
        if data_1500[i].split(": ")[0] == "bcr edsm":
            bcrs_1500.append(float(data_1500[i+1].split(": ")[1]))

    min_len = min(len(bcrs_1000), len(bcrs_1500), len(bcrs_edsm))
    bcrs_1000 = bcrs_1000[:min_len]
    bcrs_1500 = bcrs_1500[:min_len]
    bcrs_edsm = bcrs_edsm[:min_len]

    # Generate x-axis values as multiples of 5
    x_values = [5 * (i + 1) for i in range(min_len)]

    diff_1000 = [(b - a) * 100 for a, b in zip(bcrs_edsm, bcrs_1000)]
    diff_1500 = [(c - a) * 100 for a, c in zip(bcrs_edsm, bcrs_1500)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_1000, label="apta 1000", marker='o')
    plt.plot(x_values, diff_1500, label="apta 1500", marker='x')
    plt.title("BCR difference compared to a full EDSM run (Average from 5-fold cv) (offset experiment)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("BCR accuracy difference (%)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:+.1f}%'))
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def dfabound_exp_state_count_plot():
    with open("logs/stamina_exp_binsearch_dfabound_apta=1000_log.txt", "r") as f:
        data_1000 = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_dfabound_apta=1500_log.txt", "r") as f:
        data_1500 = f.read().split("\n")

    avg_edsm = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "edsm_state_counts":
            edsm_state_counts = ast.literal_eval(data_1000[i].split(": ")[1])
            avg_edsm.append(sum([float(j) for j in edsm_state_counts]) / 5.0)

    avg_1000 = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "state count avarage":
            avg_1000.append(float(data_1000[i].split(": ")[1]))

    avg_1500 = []

    for i in range(len(data_1500)):
        if data_1500[i].split(": ")[0] == "state count avarage":
            avg_1500.append(float(data_1500[i].split(": ")[1]))

    min_len = min(len(avg_1000), len(avg_1500), len(avg_edsm))
    avg_1000 = avg_1000[:min_len]
    avg_1500 = avg_1500[:min_len]
    avg_edsm = avg_edsm[:min_len]

    # Generate x-axis values as multiples of 5
    x_values = [5 * (i + 1) for i in range(min_len)]

    # Plot the differences
    diff_1000_edsm = [b - a for a, b in zip(avg_edsm, avg_1000)]
    diff_1500_edsm = [c - a for a, c in zip(avg_edsm, avg_1500)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_1000_edsm, label="apta 1000", marker='o')
    plt.plot(x_values, diff_1500_edsm, label="apta 1500", marker='x')
    plt.title("State count difference compared to a full EDSM run (Average from 5-fold cv) (dfabound experiment)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("Difference")
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def dfabound_exp_bcr_plot():
    with open("logs/stamina_exp_binsearch_dfabound_apta=1000_log.txt", "r") as f:
        data_1000 = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_dfabound_apta=1500_log.txt", "r") as f:
        data_1500 = f.read().split("\n")

    bcrs_edsm = []

    bcrs_1000 = []

    for i in range(len(data_1000)):
        if data_1000[i].split(": ")[0] == "bcr edsm":
            bcrs_edsm.append(float(data_1000[i].split(": ")[1]))
            bcrs_1000.append(float(data_1000[i+1].split(": ")[1]))

    bcrs_1500 = []

    for i in range(len(data_1500)):
        if data_1500[i].split(": ")[0] == "bcr edsm":
            bcrs_1500.append(float(data_1500[i+1].split(": ")[1]))

    min_len = min(len(bcrs_1000), len(bcrs_1500), len(bcrs_edsm))
    bcrs_1000 = bcrs_1000[:min_len]
    bcrs_1500 = bcrs_1500[:min_len]
    bcrs_edsm = bcrs_edsm[:min_len]

    # Generate x-axis values as multiples of 5
    x_values = [5 * (i + 1) for i in range(min_len)]

    diff_1000 = [(b - a) * 100 for a, b in zip(bcrs_edsm, bcrs_1000)]
    diff_1500 = [(c - a) * 100 for a, c in zip(bcrs_edsm, bcrs_1500)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_1000, label="apta 1000", marker='o')
    plt.plot(x_values, diff_1500, label="apta 1500", marker='x')
    plt.title("BCR accuracy comparison to a full EDSM run (Average from 5-fold cv) (dfabound experiment)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("BCR accuracy difference (%)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:+.1f}%'))
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compare_dfabound_offset_bcrs_plot():
    with open("logs/stamina_exp_binsearch_satoffset_apta=1500_log.txt", "r") as f:
        data_offset = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_dfabound_apta=1500_log.txt", "r") as f:
        data_dfabound = f.read().split("\n")

    bcrs_offset = []
    bcrs_edsm = []

    for i in range(len(data_offset)):
        if data_offset[i].split(": ")[0] == "bcr edsm":
            bcrs_offset.append(float(data_offset[i+1].split(": ")[1]))
            bcrs_edsm.append(float(data_offset[i].split(": ")[1]))

    bcrs_dfabound = []

    for i in range(len(data_dfabound)):
        if data_dfabound[i].split(": ")[0] == "bcr edsm":
            bcrs_dfabound.append(float(data_dfabound[i+1].split(": ")[1]))

    min_len = min(len(bcrs_offset), len(bcrs_dfabound))
    bcrs_dfabound = bcrs_dfabound[:min_len]
    bcrs_offset = bcrs_offset[:min_len]

    x_values = [5 * (i + 1) for i in range(min_len)]

    diff_offset = [(a - b) * 100 for a, b in zip(bcrs_offset, bcrs_edsm)]
    diff_dfabound = [(a - b) * 100 for a, b in zip(bcrs_dfabound, bcrs_edsm)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_dfabound, label="dfabound experiment", marker='o')
    plt.plot(x_values, diff_offset, label="offset experiment", marker='x')
    plt.title("BCR accuracy difference compared to a full EDSM run (Average from 5-fold cv)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("BCR accuracy difference (%)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:+.1f}%'))
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compare_dfabound_offset_state_counts_plot():
    with open("logs/stamina_exp_binsearch_satoffset_apta=1500_log.txt", "r") as f:
        data_offset = f.read().split("\n")

    with open("logs/stamina_exp_binsearch_dfabound_apta=1500_log.txt", "r") as f:
        data_dfabound = f.read().split("\n")

    state_counts_offset = []
    state_counts_edsm = []

    for i in range(len(data_offset)):
        if data_offset[i].split(": ")[0] == "state count average":
            state_counts_offset.append(float(data_offset[i].split(": ")[1]))
        if data_offset[i].split(": ")[0] == "edsm state count average":
            state_counts_edsm.append(float(data_offset[i].split(": ")[1]))

    state_counts_dfabound = []

    for i in range(len(data_dfabound)):
        if data_dfabound[i].split(": ")[0] == "state count avarage":
            state_counts_dfabound.append(float(data_dfabound[i].split(": ")[1]))

    min_len = min(len(state_counts_offset), len(state_counts_dfabound), len(state_counts_edsm))
    state_counts_dfabound = state_counts_dfabound[:min_len]
    state_counts_offset = state_counts_offset[:min_len]
    state_counts_edsm = state_counts_edsm[:min_len]

    x_values = [5 * (i + 1) for i in range(min_len)]

    diff_offset = [a - b for a, b in zip(state_counts_offset, state_counts_edsm)]
    diff_dfabound = [a - b for a, b in zip(state_counts_dfabound, state_counts_edsm)]

    plt.figure(figsize=(7, 3))
    plt.plot(x_values, diff_offset, label="offset experiment", marker='o')
    plt.plot(x_values, diff_dfabound, label="dfabound experiment", marker='x')
    plt.title("State count difference compared to a full EDSM run (Average from 5-fold cv)", fontsize=9)
    plt.xlabel("STAMINA dataset")
    plt.ylabel("State count difference")
    plt.xticks(x_values)  # Apply custom x-axis labels
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


offset_exp_state_count_plot()
offset_exp_bcr_plot()
dfabound_exp_state_count_plot()
dfabound_exp_bcr_plot()
compare_dfabound_offset_bcrs_plot()
compare_dfabound_offset_state_counts_plot()
