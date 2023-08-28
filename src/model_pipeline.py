from PIL import Image
import openai
import io
import sys
import requests
import json
import os
import time
from dotenv import load_dotenv
from papago import kor_to_eng_translation, eng_to_kor_translation

gpt_template = {
  "dream_title": "Dream About a Car Accident",
  "possible_meanings": [
    "Loss of Control: Car accidents often relate to a loss of control in some area of your life. It could indicate that you're feeling overwhelmed or struggling with a situation where you feel like you're not in control.",
    "Fear of Change: Cars in dreams can also represent the path we're on in life. An accident might indicate a fear of change or unexpected disruptions that could derail your plans.",
    "Conflict or Negativity: Car accidents might symbolize conflicts, arguments, or negative experiences that you fear or are currently facing.",
    "Life's Fragility: Car accidents can remind us of the fragility of life and the unpredictability of events. It could prompt you to reflect on your priorities and make sure you're living in alignment with what truly matters to you.",
    "Anxiety and Stress: Dreams about accidents can be linked to anxiety or stress in your waking life. It could suggest that you're grappling with these emotions.",
    "Warning Sign: Sometimes, dreams of accidents might serve as a symbolic warning to pay attention to something in your life that needs your immediate attention."
  ],
  "recommended_tarot_card": "The Tower"
}

def exectueGpt(text) : 
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
        {"role": "system", "content": "You are a helpful assistant who interprets dreams and recommends appropriate tarot cards."},
        {"role": "user", "content": "I had a dream about a car accident. Please interpret this dream and recommend 1 out of 78 tarot cards. Give me the respone in JSON format."},
        {"role": "assistant", "content": json.dumps(gpt_template)},
        {"role": "user", "content": text + " Please interpret this dream and recommend 1 out of 78 tarot cards. Give me the respone in JSON format."}   
    ])


    if response :
        return response['choices'][0]['message']['content']
    else :
        return None

def executeDalle(dream, tarot_card) :
    tarot_card = tarot_card.lower().replace(' ', '_')
    image = Image.open("./img/image/{tarot_card}.png".format(tarot_card = tarot_card)).convert("RGBA")
    mask = Image.open("./img/mask/{tarot_card}_mask.png".format(tarot_card = tarot_card)).convert("RGBA")
    b1 = io.BytesIO()
    b2 = io.BytesIO()

    image.save(b1, format = "PNG")
    b1.seek(0)
    mask.save(b2, format = "PNG")
    b2.seek(0)

    response = openai.Image.create_edit(
        image = b1,
        mask = b2,
        prompt = "Draw a tarot card about {dream}.".format(dream = dream),
        n = 1,
        size = "1024x1024",
    )

    # if response.status_code != 200 :
    #     # 에러 처리
    #     sys.exit(1)
    if response :
        return response['data'][0]['url']
    else :
        return None


def execute(utterance) :
    global OPEN_AI_API_KEY, OPEN_AI_API_URL

    load_dotenv('../.env')
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
    OPEN_AI_API_URL = os.getenv("OPEN_AI_API_URL")

    openai.api_key = OPEN_AI_API_KEY

    eng_utterance = kor_to_eng_translation(utterance)
    eng_gpt_result = json.loads(exectueGpt(eng_utterance))

    if eng_gpt_result == None :
        return ModelResult(None, None)

    dream_title = eng_gpt_result['dream_title']
    possible_meanings = eng_gpt_result['possible_meanings']
    recommended_tarot_card = eng_gpt_result['recommended_tarot_card']

    image_url = executeDalle(dream_title, recommended_tarot_card)

    # meaining_keys = [meaning.split(':')[0] for meaning in possible_meanings]
    kor_dream_title = eng_to_kor_translation(dream_title)
    kor_possible_meanings = [eng_to_kor_translation(meaning) for meaning in possible_meanings]

    data = {
        'dream_title' : kor_dream_title,
        'possible_meanings' : kor_possible_meanings,
        'image_url' : image_url
    }
    return ModelResult(False, data)

class ModelResult :
    def __init__(self, error, data = None) :
        self.error = error
        self.data = data

    def __str__(self) :
        return ("error: " + str(self.error) + ", data: " + str(self.data))