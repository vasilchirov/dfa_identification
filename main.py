import flexfringe
import kfold
import experiment

# data = flexfringe.flexfringe("../data/staminadata/1_training.txt.dat", "../FlexFringe/build/",
#                              ini="../ini/edsm.ini")
# flexfringe.show(data, "1_training_final")

# data = flexfringe.flexfringe("../../dfa_identification/datasets/100_training_stamina_train.dat", "../FlexFringe/build/",
#                              ini="../ini/edsm.ini")
#
# start_node_id, m, data_2 = flexfringe.load_model(
#     "../dfa_identification/datasets/100_training_stamina_train.dat.ff.final.json")
#
# with open("datasets/100_training_stamina_test.dat") as test_set:
#     traces = test_set.read()
#
# result = flexfringe.calculate_accuracy(traces, start_node_id, m)
# flexfringe.show(data, "edsm_100")
#
# print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
#       ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])

# results = []
# for k in range(20):
#     total = 0
#     for i in range(5):
#         data = flexfringe.flexfringe(f"../../dfa_identification/k-fold/stamina_train_{(k + 1) * 5}_{i + 1}.dat",
#                                      "../FlexFringe/build/",
#                                      ini="../ini/edsm.ini")
#         start_node_id, m, data_2 = flexfringe.load_model(
#             f"kfold/stamina_train_{(k + 1) * 5}_{i + 1}.dat.ff.final.json")
#
#         with open(f"kfold/stamina_test_{(k + 1) * 5}_{i + 1}.dat") as test_set:
#             traces = test_set.read()
#
#         result = flexfringe.calculate_accuracy(traces, start_node_id, m)
#
#         total += result[6]
#
#     results.append(total / 5)
#
# print(results)

# file_names = []
# for i in range(5):
#     file_names.append(f"../FlexFringe/data/staminadata/{5*(i+1)}_training.txt.dat")
#
#
# kfold.generate_k_folds(100, file_names)

# data = flexfringe.flexfringe("../../dfa_identification/generated-datasets/davidim.dat", "../FlexFringe/build/",
#                              ini="../ini/edsm.ini")
# start_node_id, m, data_2 = flexfringe.load_model(
#             f"../dfa_identification/generated-datasets/davidim.dat.ff.final.json")
#
# with open("generated-datasets/test.dat") as test_set:
#     traces = test_set.read()
#
# result = flexfringe.calculate_accuracy(traces, start_node_id, m)

# print(result[6])

res = experiment.run("../FlexFringe/data/staminadata/100_training.txt.dat", 5, "../FlexFringe/build/",
               "../../dfa_identification/", ini="../ini/edsm.ini")
print("bcr:", res)
