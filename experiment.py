import flexfringe
import kfold
import os
import shutil
import count_nodes


def run_kfold(*args, **kwargs):
    """
    Performs k-fold cross validation on a given set of traces using FlexFringe in a certain setting.

     Arguments:
    - position 0 -- path to input file with trace samples (path from dfa_identification root) (e.g. datasets/train.dat)
    - position 1 -- k (for k-fold cross validation) (k > 1)
    - position 2 -- location of the FlexFringe root dir (path from dfa_identification root) (e.g. ../FlexFringe/)
    - position 3 -- location of dfa_identification from FlexFringe root (e.g. ../dfa_identification/)
    - **kwargs** -- list of key=value arguments to pass as command line arguments to FlexFringe

    **Example:** ``run_kfold("generated-datasets/train_data.dat", "generated-datasets/test_data.dat", "../FlexFringe", "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="3", aptabound="500")``
    """
    file_name = args[0]
    k = args[1]
    flexfringe_root_dir = args[2]
    dfa_identification_dir = args[3]

    os.makedirs("kfold", exist_ok=True)
    try:
        kfold.generate_k_folds(k, file_name)

        total = 0.0
        for i in range(k):
            train_fold_name = file_name.split("/")[-1] + f"_train_{i + 1}.dat"
            test_fold_name = file_name.split("/")[-1] + f"_test_{i + 1}.dat"
            data = flexfringe.flexfringe(dfa_identification_dir + "kfold/" + train_fold_name, flexfringe_root_dir, **kwargs)
            # flexfringe.show(data, "etukaeitei") if i == 4 else None
            start_node_id, m, data_2 = flexfringe.load_model("kfold/" + train_fold_name + ".ff.final.json")
            with open(f"kfold/" + test_fold_name) as test_set:
                traces = test_set.read()
            result = flexfringe.calculate_accuracy(traces, start_node_id, m)
            print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
                  ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])
            total += result[6]

        shutil.rmtree("kfold")
    except Exception as e:
        shutil.rmtree("kfold")
        print(e)
        return None
    return total / k

def run(*args, **kwargs):
    """
    Creates a model given a training set using FlexFringe in a certain setting, and returns the performance of the model on a given test set.

     Arguments:
    - position 0 -- path to train file with trace samples (path from dfa_identification root) (e.g. datasets/train.dat)
    - position 1 -- path to test file with trace samples (path from dfa_identification root) (e.g. datasets/test.dat)
    - position 2 -- location of the FlexFringe root dir (path from dfa_identification root) (e.g. ../FlexFringe/)
    - position 3 -- location of dfa_identification from FlexFringe root (e.g. ../dfa_identification/)
    - **kwargs** -- list of key=value arguments to pass as command line arguments to FlexFringe

    **Example:** ``run("generated-datasets/train_data.dat", "generated-datasets/test_data.dat", "../FlexFringe", "../dfa_identification/", ini="ini/edsm.ini", mode="satsolver", satgreedy="1", satoffset="3", aptabound="500")``
    """
    train_file_path = args[0]
    train_file_name = train_file_path.split("/")[-1]
    test_file_path = args[1]
    flexfringe_root_dir = args[2]
    dfa_identification_dir = args[3]

    os.makedirs("run_dir", exist_ok=True)
    try:
        with open(dfa_identification_dir + train_file_path) as train_file:
            train_data = train_file.read()
        with open("run_dir/" + train_file_name + "_temp.dat", "w") as f:
            f.write(train_data)

        data = flexfringe.flexfringe(dfa_identification_dir + "run_dir/" + train_file_name + "_temp.dat", flexfringe_root_dir, **kwargs)
        flexfringe.show(data, "some_name")
        start_node_id, m, data_2 = flexfringe.load_model("run_dir/" + train_file_name + "_temp.dat.ff.final.json")
        count_nodes.count_states("run_dir/" + train_file_name + "_temp.dat.ff.final.dot")

        with open(dfa_identification_dir + test_file_path) as test_set:
            test_traces = test_set.read()

        result = flexfringe.calculate_accuracy(test_traces, start_node_id, m)
        # flexfringe.show(data, "some_name")
        print("tp:", result[0], ", fp:", result[2], ", tn:", result[1], ", fn:", result[3],
              ", bcr accuracy:", result[6], ", ratio:", result[4] / result[5])
        shutil.rmtree("run_dir")
    except Exception as e:
        shutil.rmtree("run_dir")
        print(e)
        return None
    return result[6]