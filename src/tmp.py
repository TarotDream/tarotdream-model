# def exectueGpt1(text) :
#     headers = {
#         "Authorization" : "Bearer " + OPEN_AI_API_KEY,
#         "Content-Type" : "application/json"
#     }

#     url = OPEN_AI_API_URL + "/chat/completions"
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant who interprets dreams and recommends appropriate tarot cards."},
#         {"role": "user", "content": "I had a dream about a car accident. Please interpret this dream and recommend 1 out of 78 tarot cards. Give me the respone in JSON format."},
#         {"role": "assistant", "content": json.dumps(gpt_template)},
#         {"role": "user", "content": text + " Please interpret this dream and recommend 1 out of 78 tarot cards. Give me the respone in JSON format."}   
#     ]

#     data = {
#         "model": "gpt-3.5-turbo",
#         "messages": messages,
#     }

#     response = requests.post(url, data = json.dumps(data), headers = headers)
#     if response.status_code != 200 :
#         # 에러 처리
#         sys.exit(1)
#     if response.json() :
#         return response.json()['choices'][0]['message']['content']
#     else :
#         return None

# def executeDalle1(dream) :
#     headers = {
#         "Authorization" : "Bearer " + OPEN_AI_API_KEY,
#         "Content-Type" : "application/json"
#     }
#     url = OPEN_AI_API_URL + "/images/edits"
#     data = {
#         "prompt": "Draw a tarot card about {dream}.".format(dream = dream),
#         "n": 1,
#         "size": "1024x1024"
#     }

#     image = Image.open("./img/image/peng.png").convert("RGBA")
#     mask = Image.open("./img/mask/pengmask2.png").convert("RGBA")
#     b1 = io.BytesIO()
#     b2 = io.BytesIO()
#     image.save(b1, format="PNG")
#     b1.seek(0)
#     mask.save(b2, format="PNG")
#     b2.seek(0)
#     files = {
#         "image": ("./img/image/peng.png", b1, "image/png"),
#         "mask": ("./img/image/pengmask2.png", b2, "image/png")
#     }

#     response = requests.post(url, headers = headers, files = files, json = data, )
#     print(response.json())
#     if response.status_code != 200 :
#         # 에러 처리
#         sys.exit(1)
#     else :
#         return response.json()