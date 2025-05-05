import flexfringe

data = flexfringe.flexfringe("../data/staminadata/95_training.txt.dat", "../FlexFringe/build/",
                             ini="../ini/edsm.ini",
                             symbol_count="25", state_count="25")
flexfringe.show(data, "95_training_final")
