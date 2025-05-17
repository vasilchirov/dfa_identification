import flexfringe
import kfold
import os
import shutil


def run(*args, **kwargs):
    """
    Performs k-fold cross validation on a given set of traces using FlexFringe in a certain setting.

     Arguments:
    - position 0 -- path to input file with trace samples (path from FlexFringe root)
    - position 1 -- k (for k-fold cross validation) (k > 1)
    - position 2 -- location of the FlexFringe root (e.g. ../FlexFringe/)
    - position 3 -- location of dfa_identification from FlexFringe root (e.g. ../dfa_identification/)
    - kwargs -- list of key=value arguments to pass as command line arguments to FlexFringe
    """
    file_name = args[0]
    k = args[1]
    build_dir = args[2]
    dfa_identification_dir = args[3]

    os.makedirs("kfold", exist_ok=True)
    try:
        kfold.generate_k_folds(k, file_name)

        total = 0.0
        for i in range(k):
            train_fold_name = file_name.split("/")[-1] + f"_train_{i + 1}.dat"
            test_fold_name = file_name.split("/")[-1] + f"_test_{i + 1}.dat"
            data = flexfringe.flexfringe(dfa_identification_dir + "kfold/" + train_fold_name, build_dir, **kwargs)
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
