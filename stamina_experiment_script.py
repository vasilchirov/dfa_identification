import os
import shutil
import time
from datetime import datetime

import flexfringe
import experiment
import kfold

def experiment_binary_search_dfabound(log_filename: str, apta_bound="2000"):
    with open("logs/tracker_binsearch_exp_2000.txt", "a") as f:
        f.write("<<<<<<" + log_filename + "; apta bound:" + apta_bound + ">>>>>>\n")
    with open("logs/" + log_filename, "a") as f:
        f.write(log_filename + "; apta bound:" + apta_bound + "\n")
    with open("experiment_setups/stamina_experiment.txt") as f:
        data = f.read()
    for line in data.split("\n"):
        os.makedirs("kfold", exist_ok=True)
        kfold.generate_k_folds(5, line)
        bcrs_list = [0.0 for _ in range(5)]
        state_counts = [-1 for _ in range(5)]
        is_satisfiable = [False for _ in range(5)]
        state_counts_edsm = [-1 for _ in range(5)]
        state_counts_edsm_2000 = [-1 for _ in range(5)]
        dfa_bounds = [-1 for _ in range(5)]

        start = time.perf_counter()
        for i in range(5):
            _, state_counts_edsm[i], _ = flexfringe.flexfringe(
                "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                , "../FlexFringe/", ini="ini/edsm.ini")
            _, state_counts_edsm_2000[i], _ = flexfringe.flexfringe(
                "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                , "../FlexFringe/", ini="ini/edsm.ini", aptabound=apta_bound)

            with open("logs/tracker_binsearch_exp_2000.txt", "a") as f:
                f.write(line + f"; {i + 1}:\n")

            final_is_sat = False
            final_state_count = -1
            final_dfa_bound = -1

            low = state_counts_edsm_2000[i]
            high = state_counts_edsm[i]

            while low <= high:
                mid = (low + high) // 2
                dfa_bounds[i] = mid

                now = datetime.now()
                readable_time = now.strftime("%Y-%m-%d %H:%M:%S")

                msg = "starting: " + line.split("/")[
                    -1] + f"_train_{i + 1}.dat : " + f"fold: {i + 1} ; dfa_bound: " + str(
                    dfa_bounds[i]) + " ; started at: " + readable_time
                with open("logs/tracker_binsearch_exp_2000.txt", "a") as f:
                    f.write(msg)
                    print(msg)

                diff = int(state_counts_edsm[i]) - int(dfa_bounds[i])
                offset = 3 if diff > 2 else 0

                _, state_counts[i], is_satisfiable[i] = flexfringe.flexfringe(
                    "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                    , "../FlexFringe/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1",
                    dfabound=str(dfa_bounds[i]), satoffset=str(offset))

                if is_satisfiable[i]:
                    final_is_sat = True
                    final_state_count = state_counts[i]
                    final_dfa_bound = dfa_bounds[i]

                    start_node_id, m, data_2 = flexfringe.load_model(
                        "kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat" + ".ff.final.json")

                    with open(f"kfold/" + line.split("/")[-1] + f"_test_{i + 1}.dat") as test_set:
                        traces = test_set.read()

                    bcrs_list[i] = flexfringe.calculate_accuracy(traces, start_node_id, m)[6]

                    high = mid - 1
                else:
                    low = mid + 1

            is_satisfiable[i] = final_is_sat
            state_counts[i] = final_state_count
            dfa_bounds[i] = final_dfa_bound

        epsilon = 0.0000000001
        number_of_sat_folds = 0.0 + epsilon
        for i in range(len(is_satisfiable)):
            if is_satisfiable[i]:
                number_of_sat_folds += 1.0
            else:
                state_counts[i] = 0

        shutil.rmtree("kfold")
        end = time.perf_counter()
        bcr_edsm, bcrs_list_edsm, _ = experiment.run_kfold(line, 5, "../FlexFringe/",
                                                           "../dfa_identification/",
                                                           ini="ini/edsm.ini")
        with open("logs/" + log_filename, "a") as f:
            f.write(line + "\n")
            f.write("state count avarage: " + str(sum(state_counts) / number_of_sat_folds) + "\n")
            f.write("state_counts: " + str(state_counts) + "\n")
            f.write("edsm_state_counts: " + str(state_counts_edsm) + "\n")
            f.write("edsm_state_counts_2000: " + str(state_counts_edsm_2000) + "\n")
            f.write("final dfa_bounds: " + str(dfa_bounds) + "\n")
            f.write("bcrs list edsm: " + str(bcrs_list_edsm) + "\n")
            f.write("bcrs list: " + str(bcrs_list) + "\n")
            f.write("bcr edsm: " + str(bcr_edsm) + "\n")
            f.write("bcr: " + str(sum(bcrs_list) / 5.0) + "\n")
            f.write("is_satisfiable: " + str(is_satisfiable) + "\n")
            f.write("time: " + str(end - start) + "\n")
            f.write("//////////////////////////////\n")


def experiment_binary_search_satoffset(log_filename, apta_bound="2000"):
    with open("logs/DELETE_tracker_binsearch_exp_2000.txt", "a") as f:
        f.write("<<<<<<" + log_filename + "; apta bound:" + apta_bound + ">>>>>>\n")
    with open("logs/" + log_filename, "a") as f:
        f.write(log_filename + "; apta bound:" + apta_bound + "\n")
    with open("experiment_setups/stamina_experiment_2.txt") as f:
        data = f.read()
    for line in data.split("\n"):
        os.makedirs("kfold", exist_ok=True)
        kfold.generate_k_folds(5, line)
        bcrs_list = [0.0 for _ in range(5)]
        state_counts = [-1 for _ in range(5)]
        is_satisfiable = [False for _ in range(5)]
        state_counts_edsm = [-1 for _ in range(5)]
        state_counts_edsm_2000 = [-1 for _ in range(5)]
        offsets = [-1 for _ in range(5)]

        start = time.perf_counter()
        for i in range(5):
            _, state_counts_edsm[i], _ = flexfringe.flexfringe(
                "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                , "../FlexFringe/", ini="ini/edsm.ini")
            _, state_counts_edsm_2000[i], _ = flexfringe.flexfringe(
                "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                , "../FlexFringe/", ini="ini/edsm.ini", aptabound=apta_bound)

            with open("logs/DELETE_tracker_binsearch_exp_2000.txt", "a") as f:
                f.write(line + f"; {i + 1}:\n")

            final_is_sat = False
            final_state_count = -1
            final_offset = -1

            low = state_counts_edsm_2000[i]
            high = state_counts_edsm[i]

            use_dfa_bound = False
            dfa_bound = state_counts_edsm_2000[i]
            if high - low > 12:
                use_dfa_bound = True
                dfa_bound = high - 12
                low = dfa_bound

            while low <= high:
                mid = (low + high) // 2
                offsets[i] = mid - dfa_bound

                now = datetime.now()
                readable_time = now.strftime("%Y-%m-%d %H:%M:%S")

                msg = "starting: " + line.split("/")[
                    -1] + f"_train_{i + 1}.dat : " + f"fold: {i + 1} ; satoffset: " + str(
                    offsets[i]) + " ; range: [" + str(dfa_bound) + ";" + str(
                    state_counts_edsm[i]) + "] ; started at: " + readable_time
                with open("logs/DELETE_tracker_binsearch_exp_2000.txt", "a") as f:
                    f.write(msg)
                    print(msg)

                if use_dfa_bound:
                    _, state_counts[i], is_satisfiable[i] = flexfringe.flexfringe(
                        "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                        , "../FlexFringe/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1",
                        satoffset=str(offsets[i]), dfabound=str(dfa_bound))
                else:
                    _, state_counts[i], is_satisfiable[i] = flexfringe.flexfringe(
                        "../dfa_identification/kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat"
                        , "../FlexFringe/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1",
                        satoffset=str(offsets[i]), aptabound=apta_bound)

                if is_satisfiable[i]:
                    final_is_sat = True
                    final_state_count = state_counts[i]
                    final_offset = offsets[i]

                    start_node_id, m, data_2 = flexfringe.load_model(
                        "kfold/" + line.split("/")[-1] + f"_train_{i + 1}.dat" + ".ff.final.json")

                    with open(f"kfold/" + line.split("/")[-1] + f"_test_{i + 1}.dat") as test_set:
                        traces = test_set.read()

                    bcrs_list[i] = flexfringe.calculate_accuracy(traces, start_node_id, m)[6]

                    high = mid - 1
                else:
                    low = mid + 1

            is_satisfiable[i] = final_is_sat
            state_counts[i] = final_state_count
            offsets[i] = final_offset

        epsilon = 0.0000000001
        number_of_sat_folds = 0.0 + epsilon
        for i in range(len(is_satisfiable)):
            if is_satisfiable[i]:
                number_of_sat_folds += 1.0
            else:
                state_counts[i] = 0

        shutil.rmtree("kfold")
        end = time.perf_counter()
        bcr_edsm, bcrs_list_edsm, _ = experiment.run_kfold(line, 5, "../FlexFringe/",
                                                           "../dfa_identification/",
                                                           ini="ini/edsm.ini")

        with open("zaleza.txt", "a") as f:
            f.write(str(sum(bcrs_list) / number_of_sat_folds) + "\n")

        with open("logs/" + log_filename, "a") as f:
            f.write(line + "\n")
            f.write("state count average: " + str(sum(state_counts) / number_of_sat_folds) + "\n")
            f.write("state_counts: " + str(state_counts) + "\n")
            f.write("edsm_state_counts: " + str(state_counts_edsm) + "\n")
            f.write("edsm state count average: " + str(sum(state_counts_edsm) / 5.0) + "\n")
            f.write("edsm_state_counts_2000: " + str(state_counts_edsm_2000) + "\n")
            f.write("final satoffsets: " + str(offsets) + "\n")
            f.write("bcrs list edsm: " + str(bcrs_list_edsm) + "\n")
            f.write("bcrs list: " + str(bcrs_list) + "\n")
            f.write("bcr edsm: " + str(bcr_edsm) + "\n")
            f.write("bcr: " + str(sum(bcrs_list) / number_of_sat_folds) + "\n")
            f.write("is_satisfiable: " + str(is_satisfiable) + "\n")
            f.write("time: " + str(end - start) + "\n")
            f.write("//////////////////////////////\n")

