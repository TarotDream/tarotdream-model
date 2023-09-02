from PIL import Image
import openai
import io
import json
import os
from dotenv import load_dotenv
from papago import kor_to_eng_translation, eng_to_kor_translation

def executeGpt(text) : 
    try :
        response = openai.ChatCompletion.create(
        model = "ft:gpt-3.5-turbo-0613:prompter::7u2ta9Jv",
        messages = [
            {"role": "system",
             "content": "너는 세상에서 꿈 해석을 가장 잘하고 꿈에 대해 가장 적합한 22개의 메이저 타로카드 (Judgement, Justice, Strength, Temperance, The Chariot, The Death, The Devil, The Emperor, The Empress, The Fool, The Hanged Man, The Hermit, The Hierophant, The High Priestess, The Lovers, The Magician, The Moon, The Star, The Sun, The Tower, The World, Wheel of Fortune) 중 하나의 타로카드를 추천해주는 점술가야."},
            {"role": "user", "content": text + "을 해석해줘. Assistant에 맞는 JSON 형식으로 대답해줘."},
        ])

        if response :
            return response.choices[0].message.content
        else :
            return None
    
    except Exception as e :
        print('[exectueGpt Error]', str(e))
        raise e
    

def executeDalle(dream, tarot_card) :
    try : 
        tarot_card = tarot_card.lower().replace(' ', '_')
        print(dream)
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
            return response.data[0].url
        else :
            return None
        
    except Exception as e :
        print('[executeDalle Error]', str(e))
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
        print('[regenerate Error]', str(e))
        raise e

def generate(utterance) :
    try :
        global OPEN_AI_API_KEY, OPEN_AI_API_URL

        load_dotenv('../.env')
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        OPEN_AI_API_URL = os.getenv("OPEN_AI_API_URL")

        openai.api_key = OPEN_AI_API_KEY

        gpt_result = json.loads(executeGpt(utterance))
        if gpt_result == None :
            return ModelResult(True, "No GPT Result")
        
        if 'recommended_tarot_card' not in gpt_result or 'english_dream_title' not in gpt_result or 'korean_dream_title' not in gpt_result or 'possible_meanings' not in gpt_result :
            return ModelResult(True, "No GPT Result")
        
        dream_title = gpt_result['korean_dream_title']
        eng_dream_title = gpt_result['english_dream_title']
        possible_meanings = gpt_result['possible_meanings']
        recommended_tarot_card = gpt_result['recommended_tarot_card']
        # meaning = kor_to_eng_translation(possible_meanings[0].split(':')[0])
        # image_url = executeDalle(eng_dream_title + ' and ' + meaning, recommended_tarot_card)
        image_url = executeDalle(eng_dream_title, recommended_tarot_card)

        data = {
            'dream_title' : dream_title,
            'eng_dream_title' : eng_dream_title,
            'possible_meanings' : possible_meanings,
            'recommended_tarot_card' : recommended_tarot_card,
            'image_url' : image_url
        }
        return ModelResult(False, "success", data)

    except Exception as e :
        print('[generate Error]', str(e))
        raise e

class ModelResult :
    def __init__(self, error, message = None, data = None) :
        self.error = error
        self.message = message
        self.data = data

    def __str__(self) :
        return ("error: " + str(self.error) + ", message" + str(self.message) + ", data: " + str(self.data))