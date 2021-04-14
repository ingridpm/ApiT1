from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def principal():
    return "Api Taller 1"

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)