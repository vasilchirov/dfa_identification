import experiment
import flexfringe

data = flexfringe.flexfringe("data/staminadata/100_training.txt.dat", "../FlexFringe/",
                             ini="ini/edsm.ini", mode="satsolver", satoffset="0", satgreedy="1", dfabound="14")
#
# data = flexfringe.flexfringe("../dfa_identification/generated-datasets/train_data.dat", "../FlexFringe/",
#                              ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="3", aptabound="500")

start_node_id, m, data_2 = flexfringe.load_model(
    "datasets/50_training_stamina_train.dat.ff.final.json")

with open("datasets/50_training_stamina_test.dat") as test_set:
    traces = test_set.read()

result = flexfringe.calculate_accuracy(traces, start_node_id, m)
flexfringe.show(data, "kurchec")

print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
      ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])

# res = experiment.run_kfold("../FlexFringe/data/staminadata/2_training.txt.dat", 5, "../FlexFringe/",
#                "../dfa_identification/", ini="ini/edsm.ini")
# res = experiment.run_kfold("generated-datasets/some_data.dat", 5, "../FlexFringe/",
#                "../dfa_identification/", ini="ini/edsm.ini")
# res = experiment.run_kfold("../FlexFringe/data/staminadata/2_training.txt.dat", 5, "../FlexFringe/",
#                "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", aptabound="6000", satoffset="0",
#                      satsolver="./glucose-syrup")
# res = experiment.run("generated-datasets/train_data.dat", "generated-datasets/test_data.dat", "../FlexFringe",
#                      "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="3", aptabound="500")
# print("bcr:", res)
