from http import HTTPStatus
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from model_pipeline import execute

app = Flask(__name__)
CORS(app, resources={r"/": {"origins" : "*"}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods = ['POST'])
def generate_dream() :
    body = request.get_json()
    utterance = body['utterance']
    modelResult = execute(utterance)

    if modelResult.error == True :
        return jsonify({
            "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
        })
    
    return jsonify({
        "status" : HTTPStatus.OK,
        "dream_title" : modelResult.data['dream_title'],
        "possible_meanings" : modelResult.data['possible_meanings'],
        # "recommended_tarot_card" : data['recommended_tarot_card'],
        "image_url" : modelResult.data['image_url']
    })

if __name__ == "__main__":
    app.run(debug = True, port = 5000)