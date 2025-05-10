import flexfringe

data = flexfringe.flexfringe("../data/staminadata/1_training.txt.dat", "../FlexFringe/build/",
                             ini="../ini/edsm.ini",
                             symbol_count="25", state_count="25")
flexfringe.show(data, "1_training_final")

m, data = flexfringe.load_model("../old_flexfringe/FlexFringe/data/staminadata/1_training.txt.dat.ff.final.json")

positive = ["1 0 0 0 0 0 0 0 0", "0 1 1 0 0 0 1 0 1 0 1 0 1 0 0", "1 0 1 0 0"]
negative = ["0 1 0 0 0", "1 1 0 0 0 0 0 0 0 1 0 0", "0 0 0 0 0 1"]

for sample in positive:
  print("positive: ", flexfringe.traverse(m, sample))

for sample in negative:
  print("negative: ", flexfringe.traverse(m, sample))