import json
import pandas as pd


def load_json(fname):
    with open(fname, encoding="utf-8") as f:
        json_obj = json.load(f)
    return json_obj

def dataLoad(path:str='../dataset/'):
    item_names_table = pd.read_parquet(path + "item_names_table.parquet")
    train_user_seq_log = pd.read_parquet(path + "train_user_seq_log.parquet")
    test_user_label = pd.read_parquet(path + "test_user_label.parquet")
    test_user_seq_log = pd.read_parquet(path + "test_user_seq_log.parquet")
    return item_names_table, train_user_seq_log, test_user_label, test_user_seq_log

def fe_trainLoad(path:str='../dataset/'):
    fe_train_user_seq_log = pd.read_parquet(path + "fe_train_user_seq_log.parquet")
    return fe_train_user_seq_log

def trainValidLoad(path:str='../dataset/'):
    train = pd.read_parquet(path + "train.parquet")
    train_valid = pd.read_parquet(path + "train_valid.parquet")
    sample_sumbission = pd.read_parquet(path + "sample_sumbission.parquet")
    return train, train_valid, sample_sumbission

def testLoad(path:str='../dataset/'):
    fe_test = pd.read_parquet(path + "fe_test.parquet")
    final_submission = pd.read_parquet(path + "final_sumbission.parquet")
    test_user_label = pd.read_parquet(path + "test_user_label.parquet")
    return fe_test, final_submission, test_user_label
