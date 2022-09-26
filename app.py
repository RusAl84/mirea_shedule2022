import json
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)
global df
df = ""


def load_data():
    with open('df.pickle', 'rb') as handle:
        ldf = pickle.load(handle)
    global df;
    df = ldf;


@app.route('/')
def dafault_route():
    return 'schedule'


@app.route("/api/schedule", methods=['POST'])
def schedule():
    data = request.json
    teacher = str(data['teacher'])
    week = str(data['week'])
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
    print(return_data)
    str_return_data = json.dumps(return_data)
    return str_return_data
    # return f"{teacher} {str(week)}"


@app.route("/api/teachers", methods=['get'])
def teachers():
    teachers = ["teach1", "teach2"]
    str_return_data = json.dumps(teachers)
    return str_return_data


if __name__ == '__main__':
    load_data()
    app.run(host="0.0.0.0", debug=False)
