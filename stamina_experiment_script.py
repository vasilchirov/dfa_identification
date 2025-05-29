import os
import shutil
import time

import flexfringe
import experiment
import kfold

with open("experiment_setups/stamina_experiment.txt") as f:
    data = f.read()
for line in data.split("\n"):
    data_edsm = ['', '', '', '', '']
    state_counts_edsm = [-1, -1, -1, -1, -1]
    state_counts_edsm_1000 = [-1, -1, -1, -1, -1]

    os.makedirs("kfold", exist_ok=True)
    kfold.generate_k_folds(5, line)

    for i in range(5):
        data_edsm[i], state_counts_edsm[i] = flexfringe.flexfringe(
            "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
            , "../FlexFringe/", ini="ini/edsm.ini")
        _, state_counts_edsm_1000[i] = flexfringe.flexfringe(
            "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
            , "../FlexFringe/", ini="ini/edsm.ini", aptabound="1000")

    shutil.rmtree("kfold")

    bcr_edsm, bcrs_list_edsm, state_counts_edsm_kfold = experiment.run_kfold(line, 5, "../FlexFringe/",
                                                                             "../dfa_identification/",
                                                                             ini="ini/edsm.ini")
    offsets = [str(state_counts_edsm[i] - state_counts_edsm_1000[i])
               if state_counts_edsm[i] - state_counts_edsm_1000[i] <= 12 else "12" for i in range(5)]

    dfa_bounds = [str(state_counts_edsm[i] - 12)
                  if state_counts_edsm[i] - state_counts_edsm_1000[i] > 12 else str(state_counts_edsm[i]) for i in
                  range(5)]

    apta_bounds = ["1000" if state_counts_edsm[i] - state_counts_edsm_1000[i] <= 12 else "0" for i in range(5)]

    start = time.perf_counter()
    bcr, bcrs_list, state_counts = experiment.run_kfold(line, 5, "../FlexFringe/", "../dfa_identification/",
                                                        ini="ini/edsm.ini", mode="satsolver", satgreedy="1",
                                                        aptabound=apta_bounds, satoffset=offsets,
                                                        dfabound=dfa_bounds)
    end = time.perf_counter()

    with open("logs/stamina_experiment_updated_log.txt", "a") as f:
        f.write(line + " = ")
        f.write("offsets:" + str(offsets) + ", aptabounds:" + str(apta_bounds) + ". dfabounds:" + str(dfa_bounds))
        f.write(", bcr: " + str(bcr))
        f.write(", bcrs_list: " + str(bcrs_list))
        f.write(", time: " + str(end - start))
        f.write(", state_counts: " + str(state_counts))
        f.write("\n")
        f.write("bcr edsm: " + str(bcr_edsm))
        f.write(", bcrs edsm: " + str(bcrs_list_edsm))
        f.write(", edsm state counts kfold: " + str(state_counts_edsm_kfold))
        f.write("\n")
