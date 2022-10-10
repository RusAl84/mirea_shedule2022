import json
from flask import Flask, request, jsonify
from flask_cors import CORS

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
    lis1 = [teacher, week]
    str_return_data = json.dumps(lis1)
    return str_return_data


@app.route("/api/teachers/<int:id>", methods=['get'])
def teachers(id):
    from get_urls import get_urls
    urls = get_urls()

    return f"ezh {id} {urls}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
app.run(host="0.0.0.0", debug=False)