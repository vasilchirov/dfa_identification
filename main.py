import experiment

# data = flexfringe.flexfringe("../../Research Project/dfa_identification/datasets/100_training_stamina_train.dat", "../../Software Project/FlexFringe/",
#                              ini="ini/edsm.ini")
#
# start_node_id, m, data_2 = flexfringe.load_model(
#     "datasets/100_training_stamina_train.dat.ff.final.json")
#
# with open("datasets/100_training_stamina_test.dat") as test_set:
#     traces = test_set.read()
#
# result = flexfringe.calculate_accuracy(traces, start_node_id, m)
# # flexfringe.show(data, "kurec")
# #
# print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
#       ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])

res = experiment.run("../FlexFringe/data/staminadata/100_training.txt.dat", 5, "../FlexFringe/",
               "../dfa_identification/", ini="ini/edsm.ini")
# res = experiment.run("generated-datasets/4.dat", 5, "../FlexFringe/build/",
#                "../../dfa_identification/", ini="../ini/edsm.ini")
print("bcr:", res)
