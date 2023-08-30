from http import HTTPStatus
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from model_pipeline import generate, regenerate

app = Flask(__name__)
CORS(app, resources={r"/": {"origins" : "*"}})

@app.route('/')
def health_check():
    return 'OK!'

@app.route('/dream/generate', methods = ['POST'])
def generate_dream() :
    try : 
        body = request.get_json()
        utterance = body['utterance']
        modelResult = generate(utterance)

        if modelResult.error == True :
            return Response(modelResult.message, status = HTTPStatus.BAD_REQUEST)
    
        return jsonify({
            "message" : modelResult.message,
            "dream_title" : modelResult.data['dream_title'],
            "eng_dream_title" : modelResult.data['eng_dream_title'],
            "possible_meanings" : modelResult.data['possible_meanings'],
            "recommended_tarot_card" : modelResult.data['recommended_tarot_card'],
            "image_url" : modelResult.data['image_url']
        })
    
    except Exception as e :
        return Response(str(e), status = HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/dream/regenerate', methods = ['POST'])
def regenerate_dream() :
    try :     
        body = request.get_json()
        dream = body['dream']
        tarot_card = body['tarot_card']
        modelResult = regenerate(dream, tarot_card)

        if modelResult.error == True :
            return Response(modelResult.message, status = HTTPStatus.INTERNAL_SERVER_ERROR)
        
        return jsonify({
            "message" : modelResult.message,
            "image_url" : modelResult.data['image_url']
        })

    except Exception as e :
        return Response(str(e), status = HTTPStatus.INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    app.run(debug = True, port = 5000, host = '0.0.0.0')