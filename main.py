from math import floor

import flexfringe

# data = flexfringe.flexfringe("../data/staminadata/1_training.txt.dat", "../FlexFringe/build/",
#                              ini="../ini/edsm.ini")
# flexfringe.show(data, "1_training_final")

data = flexfringe.flexfringe("../../dfa_identification/datasets/100_training_stamina_train.dat", "../FlexFringe/build/",
                             ini="../ini/edsm.ini")
# flexfringe.show(data, "1_training_final")

# start_node_id, m, data = flexfringe.load_model("../FlexFringe/data/staminadata/1_training.txt.dat.ff.final.json")
#
# positive = ["1 0 0 0 0 0 0 0 0", "0 1 1 0 0 0 1 0 1 0 1 0 1 0 0", "1 0 1 0 0"]
# negative = ["0 1 0 0 0", "1 1 0 0 0 0 0 0 0 1 0 0", "0 0 0 0 0 1"]
#
# for sample in positive:
#   print("positive: ", flexfringe.traverse(start_node_id, m, sample))
#
# for sample in negative:
#   print("negative: ", flexfringe.traverse(start_node_id, m, sample))

start_node_id, m, data = flexfringe.load_model("../dfa_identification/datasets/100_training_stamina_train.dat.ff.final.json")

with open("datasets/100_training_stamina_test.dat") as test_set:
    traces = test_set.read()

rows = traces.split("\n")
samples = []

for i in range(len(rows)):
    if i == 0:
        continue
    path = rows[i].split(" ")
    samples.append([" ".join(path[2:]), path[0]])

counter = 0
for sample in samples:
    if sample[1] == '1':
        is_positive = True
    else:
        is_positive = False
    counter += (flexfringe.traverse(start_node_id, m, sample[0]) == is_positive)

print("correct:", counter, "/", len(samples), ", accuracy:", str(counter * 100 / (len(samples))) + "%")
