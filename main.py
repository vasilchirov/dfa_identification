import os
import shutil

import count_nodes
import experiment
import flexfringe
import time

import kfold

# data = flexfringe.flexfringe("data/staminadata/2_training.txt.dat", "../FlexFringe/",
#                              ini="ini/edsm.ini", mode="satsolver", satoffset="23", satgreedy="1", aptabound="2000")
# #
# # data = flexfringe.flexfringe("../dfa_identification/generated-datasets/train_data.dat", "../FlexFringe/",
# #                              ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="3", aptabound="500")
#
# start_node_id, m, data_2 = flexfringe.load_model(
#     "datasets/50_training_stamina_train.dat.ff.final.json")
#
# with open("datasets/50_training_stamina_test.dat") as test_set:
#     traces = test_set.read()
#
# result = flexfringe.calculate_accuracy(traces, start_node_id, m)
# flexfringe.show(data, "kurchec")
#
# print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
#       ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])

# res = experiment.run_kfold("../FlexFringe/data/staminadata/2_training.txt.dat", 5, "../FlexFringe/",
#                "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", aptabound="1000", satoffset="3")
# res = experiment.run("../FlexFringe/data/staminadata/20_training.txt.dat", "../FlexFringe/data/staminadata/20_training.txt.dat", "../FlexFringe",
#                      "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="5", aptabound="1000")
# res = experiment.run("generated-datasets/easy_small_train.dat", "generated-datasets/easy_small_test.dat", "../FlexFringe",
#                      "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="0", aptabound="1000")
# print("bcr:", res)

# with open("experiment_setups/switch_time_test.txt") as f:
#     data = f.read()
# for line in data.split("\n"):
#     setup_arr = line.split(" ")
#     start = time.perf_counter()
#     res, state_count = experiment.run(setup_arr[0], setup_arr[1], "../FlexFringe/", "../dfa_identification/", ini="ini/edsm.ini",
#                          mode="satsolver", satgreedy="1", satoffset=setup_arr[2], aptabound=setup_arr[3])
#     end = time.perf_counter()
#     with open("logs/switch_time_test_log.txt", "a") as f:
#         f.write(setup_arr[0] + " = ")
#         f.write("offset:" + setup_arr[2] + ", aptabound:" + setup_arr[3])
#         f.write(", bcr: " + str(res))
#         f.write(", time: " + str(end - start))
#         f.write(", state_count: " + str(state_count))
#         f.write("\n")

