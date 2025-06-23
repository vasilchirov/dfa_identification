from stamina_experiment_script import experiment_binary_search_dfabound, experiment_binary_search_satoffset

# Running the experiments
apta_bounds = ["1000", "1500"]

for bound in apta_bounds:
    experiment_binary_search_dfabound(f"D_stamina_exp_binsearch_dfabound_apta={bound}_log.txt", apta_bound=bound)
    experiment_binary_search_satoffset(f"D_stamina_exp_binsearch_satoffset_apta={bound}_log.txt", apta_bound=bound)

# Calculating the correlations
bcrs_edsm = []
bcrs_offset = []

with open("logs/stamina_exp_binsearch_satoffset_apta=1000_log.txt", "r") as f:
    data = f.read().split("\n")

for i in range(len(data)):
    if data[i].split(": ")[0] == "edsm state count average":
        bcrs_edsm.append(float(data[i].split(": ")[1]))
    elif data[i].split(": ")[0] == "state count avarage":
        bcrs_offset.append(float(data[i].split(": ")[1]))

differences = [(c - a) for a, c in zip(bcrs_edsm, bcrs_offset)]

sum_alphabet_sizes = [0.0, 0.0, 0.0, 0.0, 0.0]
sum_sparsity = [0.0, 0.0, 0.0, 0.0]

for i in range(len(differences)):
    if i in range(0, 4):
        sum_alphabet_sizes[0] += differences[i]
    elif i in range(4, 8):
        sum_alphabet_sizes[1] += differences[i]
    elif i in range(8, 12):
        sum_alphabet_sizes[2] += differences[i]
    elif i in range(12, 16):
        sum_alphabet_sizes[3] += differences[i]
    elif i in range(16, 20):
        sum_alphabet_sizes[4] += differences[i]

for i in range(20):
    if i == 0:
        sum_sparsity[0] += differences[i]
    elif i == 1:
        sum_sparsity[1] += differences[i]
    elif i == 2:
        sum_sparsity[2] += differences[i]
    elif i == 3:
        sum_sparsity[3] += differences[i]
    elif i == 4:
        sum_sparsity[0] += differences[i]
    elif i == 5:
        sum_sparsity[1] += differences[i]
    elif i == 6:
        sum_sparsity[2] += differences[i]
    elif i == 7:
        sum_sparsity[3] += differences[i]
    elif i == 8:
        sum_sparsity[0] += differences[i]
    elif i == 9:
        sum_sparsity[1] += differences[i]
    elif i == 10:
        sum_sparsity[2] += differences[i]
    elif i == 11:
        sum_sparsity[3] += differences[i]
    elif i == 12:
        sum_sparsity[0] += differences[i]
    elif i == 13:
        sum_sparsity[1] += differences[i]
    elif i == 14:
        sum_sparsity[2] += differences[i]
    elif i == 15:
        sum_sparsity[3] += differences[i]
    elif i == 16:
        sum_sparsity[0] += differences[i]
    elif i == 17:
        sum_sparsity[1] += differences[i]
    elif i == 18:
        sum_sparsity[2] += differences[i]
    elif i == 19:
        sum_sparsity[3] += differences[i]

avg_diff_alphabet_sizes = [i / 4.0 for i in sum_alphabet_sizes]
avg_diff_sparsity = [i / 5.0 for i in sum_sparsity]

from scipy.stats import pearsonr, wilcoxon

r, p = pearsonr([1, 0.5, 0.25, 0.125], avg_diff_sparsity)
print(r, p)

r, p = pearsonr([0.04, 0.1, 0.2, 0.4, 1], avg_diff_alphabet_sizes)
print(r, p)

print(avg_diff_alphabet_sizes, avg_diff_sparsity)
stat, p = wilcoxon(bcrs_offset, bcrs_edsm)

print(stat, p)

zipped = zip(bcrs_edsm, differences)
zipped = sorted(zipped, key=lambda x: x[0])

print(zipped)

r, p = pearsonr([i[0] for i in zipped], [i[1] for i in zipped])

print(r, p)
