import numpy as np
import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

def load_metastatic_dataset(data_dir):
    try:
        df_meta = pd.read_csv(f'{data_dir}/ExternalDataMeta.csv', index_col=0)
    except FileNotFoundError as err:
        print("Cannot find external data---did you `bunzip2` it?")
        raise err

    string_labels_meta = df_meta['tumor.type']
    df_meta = df_meta.drop(['tumor.type'], axis=1)

    common_columns = pd.read_csv(f"{data_dir}/features_791.csv", header=None, index_col=0).index
    df_meta = df_meta.loc[:, common_columns]

    scaler = StandardScaler()
    meta_X = df_meta.transpose().values
    scaler.fit(meta_X)
    meta_X = scaler.transform(meta_X)
    meta_X = np.transpose(meta_X)

    meta_Y = string_labels_meta
    meta_Y[meta_Y=='COAD'] = 'COADREAD'

    print("meta labels:", string_labels_meta)
    print("meta data size:", meta_X.shape)
    print("meta label size:", meta_Y.shape)
    print(meta_X)
    return meta_X, meta_Y


DATASETS = {
    "metastatic": load_metastatic_dataset
}


def load_dataset(data_dir, data_set_name):

    assert data_set_name in DATASETS.keys()

    print(f"Loading {data_set_name} data from {data_dir}")
    return DATASETS[data_set_name](data_dir)
