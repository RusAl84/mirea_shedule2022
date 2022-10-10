import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import get_week

app = Flask(__name__)
CORS(app)

@app.route('/')
def dafault_route():
    return 'schedule'


@app.route("/api/schedule", methods=['POST'])
def schedule():
    data = request.json
    teacher = str(data['teacher'])
    week = str(data['week'])
    return_data = get_week.get_week(teacher, week)
    str_return_data = json.dumps(return_data)
    return str_return_data
    # return f"{teacher} {str(week)}"


@app.route("/api/teachers", methods=['get'])
def teachers():
    teachers = ["teach1", "teach2"]
    str_return_data = json.dumps(teachers)
    return str_return_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
