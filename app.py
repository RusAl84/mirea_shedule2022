from flask import Flask, request, jsonify
from flask_cors import CORS
from data_manager import DataManager

app = Flask(__name__)
CORS(app)

@app.route('/')
def dafault_route():
    return 'schedule'


@app.route("/api/schedule/", methods=['post'])
def schedule():
    return_data = data_manager.get_week(request.form['teacher'], request.form['week'])
    return return_data


@app.route("/api/teachers", methods=['get'])
def all_teachers():
    teachers = data_manager.get_teachers()
    return teachers


@app.route("/api/empty_auds", methods=['post'])
def empty_auds():
    auds = data_manager.get_empty_auds(int(request.form['subj']), bool(request.form['komp']))
    return auds


if __name__ == '__main__':
    data_manager = DataManager()
    app.run(host="0.0.0.0", debug=False, port=26508)
