import json
import pickle
import pandas as pd


def load_data():
    with open('df.pickle', 'rb') as handle:
        ldf = pickle.load(handle)
    return ldf;


def get_week(teacher="", week=1):
    df = load_data()
    return_data = []
    line = {}
    item = df.loc[11, :].values.tolist()
    line["inst"] = str(item[0])
    line["groups"] = str(item[1])
    line["num_day"] = str(item[2])
    line["num_subj"] = str(item[3])
    line["week"] = str(item[4])
    line["subj_name"] = str(item[5])
    line["subj_type"] = str(item[6])
    line["teach_name"] = str(item[7])
    line["aud_name"] = str(item[8])
    return_data.append(line)
    return_data.append(line)
    return_data.append(line)
    return_data.append(line)
    print(return_data)
    return return_data


if __name__ == "__main__":
    get_week()
