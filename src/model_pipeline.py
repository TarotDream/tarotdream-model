from PIL import Image
import openai
import io
import json
import os
from dotenv import load_dotenv
from papago import kor_to_eng_translation, eng_to_kor_translation

gpt_template = {
  "dream_title": "A Car Accident on the Highway",
  "possible_meanings": [
    "Loss of Direction: Dreaming of a car accident on the highway could symbolize a feeling of being lost or uncertain about the direction you're taking in life. It might indicate a need to reevaluate your goals and plans.",
    "Speed and Overwhelm: Highways often represent the fast pace of life. A car accident could indicate that you're moving too quickly and are at risk of burning out or facing challenges due to the speed at which you're going.",
    "Conflict or Avoidance: Highways can also be seen as a path to confrontation or avoiding certain issues. This dream might suggest unresolved conflicts or the need to face something you've been avoiding.",
    "Lack of Control: High speeds on the highway can sometimes translate to a lack of control in your waking life. This dream could point to situations where you feel things are moving too fast for you to manage.",
    "Warning of Risks: Dreams of accidents can sometimes serve as warnings. This dream might be encouraging you to slow down, be cautious, and avoid taking unnecessary risks.",
    "Fear and Anxiety: A car accident on the highway might reflect feelings of fear and anxiety about the challenges and uncertainties you're facing."
],
  "recommended_tarot_card": "The Chariot"
}

def executeGpt(text) : 
    try :
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant who interprets dreams and recommends appropriate one tarot card among 22  tarot cards."},
            {"role": "user", "content": """
            I had a dream that I had a car accident on the highway.
            Please interpret this dream and recommend 1 out of 22 tarot cards. (Judgement, Justice, Strength, Temperance, The Chariot, The Death, The Devil, The Emperor, The Empress, The Fool, The Hanged Man, The Hermit, The Hierophant, The High Priestess, The Lovers, The Magician, The Moon, The Star, The Sun, The Tower, The World, Wheel of Fortune)
            Give me the response in JSON format and the format must follow below.""" },
            {"role": "assistant", "content": json.dumps(gpt_template)},
            {"role": "user", "content": text + " Please interpret this dream and recommend 1 out of 22 tarot cards. Give me the resposne in JSON format."}   
        ])

        if response :
            return response['choices'][0]['message']['content']
        else :
            return None
    
    except Exception as e :
        raise e
    

def executeDalle(dream, tarot_card) :
    try : 
        print('dream', dream, 'tart_card', tarot_card)
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
            prompt = "Draw about {dream} by medieval drawing style.".format(dream = dream),
            n = 1,
            size = "1024x1024",
        )

        if response :
            return response['data'][0]['url']
        else :
            return None
        
    except Exception as e :
        raise e

def regenerate(dream, tarot_card) :
    try :
        global OPEN_AI_API_KEY, OPEN_AI_API_URL

        load_dotenv('../.env')
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        OPEN_AI_API_URL = os.getenv("OPEN_AI_API_URL")

        openai.api_key = OPEN_AI_API_KEY

        image_url = executeDalle(dream, tarot_card)
        if image_url == None : 
            return ModelResult(True, "No Dalle Result")
        
        data = {
            'image_url' : image_url
        }
        return ModelResult(False, "success", data)
    
    except Exception as e :
        raise e;


def generate(utterance) :
    try :
        global OPEN_AI_API_KEY, OPEN_AI_API_URL

        load_dotenv('../.env')
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        OPEN_AI_API_URL = os.getenv("OPEN_AI_API_URL")

        openai.api_key = OPEN_AI_API_KEY

        eng_utterance = kor_to_eng_translation(utterance)
        eng_gpt_result = json.loads(executeGpt(eng_utterance))

        if eng_gpt_result == None :
            return ModelResult(True, "No GPT Result")
        
        if 'recommended_tarot_card' not in eng_gpt_result or 'dream_title' not in eng_gpt_result or 'possible_meanings' not in eng_gpt_result :
            return ModelResult(True, "No GPT Result")

        dream_title = eng_gpt_result['dream_title']
        possible_meanings = eng_gpt_result['possible_meanings']
        meaning_key = possible_meanings[0].split(':')[0]
        recommended_tarot_card = eng_gpt_result['recommended_tarot_card']
        # image_url = executeDalle(dream_title, recommended_tarot_card)
        image_url = executeDalle(dream_title + ', ' + meaning_key, recommended_tarot_card)
        kor_dream_title = eng_to_kor_translation(dream_title)
        kor_possible_meanings = [eng_to_kor_translation(meaning) for meaning in possible_meanings]
        kor_possible_meanings = [meaning for meaning in kor_possible_meanings if len(meaning) > 0]

        data = {
            'dream_title' : kor_dream_title,
            'eng_dream_title' : dream_title,
            'possible_meanings' : kor_possible_meanings,
            'recommended_tarot_card' : recommended_tarot_card,
            'image_url' : image_url
        }
        return ModelResult(False, "success", data)

    except Exception as e :
        raise e

class ModelResult :
    def __init__(self, error, message = None, data = None) :
        self.error = error
        self.message = message
        self.data = data

    def __str__(self) :
        return ("error: " + str(self.error) + ", data: " + str(self.data))