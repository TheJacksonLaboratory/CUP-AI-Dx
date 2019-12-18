import numpy as np
from keras import backend as K


def reshape_data_1d(data):
    data = np.expand_dims(data, axis=2)
    return data


def top_n_accuracy(truths, preds, n):
    # truths: int true label
    # preds: vector prob prediction
    best_n = np.argsort(preds, axis=1)[:, -n:]  # index sorted
    ts = np.array(truths)
    successes = 0

    for i in range(ts.shape[0]):
        if ts[i] in list(best_n[i, :]):
            successes += 1

    return float(successes)/ts.shape[0]


def adjust_label(pred_labels, data_set):
    # no object option will truncate the string length
    pred_labels = np.array(pred_labels, dtype=object)
    if data_set == 'PDX':
        pred_labels[np.isin(pred_labels, ("LGG", "GBM"))] = 'LGG/GBM'
        pred_labels[np.isin(pred_labels, ('KIRC', 'KIRP', 'KIRH'))] = 'KIRC/KIRP/KIRH'
        pred_labels[np.isin(pred_labels, ('LUAD', 'LUSC'))] = 'LUAD/LUSC'

    return pred_labels


def reset_weights(model):
    session = K.get_session()
    for layer in model.layers:
        if hasattr(layer, 'kernel_initializer'):
            layer.kernel.initializer.run(session=session)
