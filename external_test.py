"""
Docstring goes here
"""
import json
import argparse
import time as tt
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
from utils import reshape_data_1d, adjust_label, top_n_accuracy
from datasets import load_dataset, DATASETS


def load_label_encodings(data_dir):
    with open(f"{data_dir}/label_encoding.json") as fin:
        _encoding = json.load(fin)
    int_to_label = dict((int(k), v) for k, v in _encoding.items())
    label_to_int = dict((v, int(k)) for k, v in _encoding.items())
    return int_to_label, label_to_int


def external_validation(x, y, data_set, keras_model):
    """Function to gauge model performance on external datasets

    :param x:
    :param y:
    :param data_set:
    :param keras_model:
    """

    # load the trained NN
    pred_prob = keras_model.predict(x)
    pred_labels = np.argmax(pred_prob, axis=1)

    pred_labels = [from_int_to_label[k] for k in pred_labels]

    pred_labels = adjust_label(pred_labels, data_set)
    cm_labels = list(set(pred_labels) | set(y))
    cm_labels.sort()

    confusion_file = f"Confusion_matrix_{data_set}.csv"
    _confusion_matrix = confusion_matrix(y, pred_labels, labels=cm_labels)
    pd.DataFrame(
        _confusion_matrix,
        index=cm_labels,
        columns=cm_labels
    ).to_csv(confusion_file)

    report_file = f"By_Class_metric_{data_set}.txt"
    with open(report_file, "w+") as f:
        report = classification_report(y, pred_labels, labels=cm_labels)
        f.write(report)

    acc = np.sum(_confusion_matrix.diagonal()) / np.sum(_confusion_matrix)
    print(f"Overall {data_set} accuracy: {acc*100}%")

    # top 5 accuracy
    if data_set != "PDX":
        real_int = [from_label_to_int[k] for k in y]
        pred_probs = keras_model.predict(x)
        top5_acc = top_n_accuracy(real_int, pred_probs, n=5)
        print(f"Overall top 5 accuracy {data_set}': {top5_acc*100}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="+", choices=DATASETS.keys())
    parser.add_argument("--data-dir", default="data")
    parser.add_argument(
        "--model", required=True, default="inception",
        choices=["inception", "cnn", "resnet"]
    )
    parser.add_argument("--models-dir", default="models")
    args = parser.parse_args()

    start_time = tt.time()

    model_files = {
        "inception": f"{args.models_dir}/inception.h5",
        "cnn": f"{args.models_dir}/cnn.h5",
        "resnet": f"{args.models_dir}/resnet.h5"
    }

    keras_model = load_model(model_files[args.model])

    from_int_to_label, from_label_to_int = load_label_encodings(args.data_dir)

    for dataset_name in args.datasets:
        external_X, external_Y = load_dataset(args.data_dir, dataset_name)
        test_x = reshape_data_1d(external_X)
        external_validation(test_x, external_Y, dataset_name, keras_model)

    print(f"--- {tt.time() - start_time} seconds ---")
