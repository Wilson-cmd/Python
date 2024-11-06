from flask import Flask, jsonify, request
from base64 import b64decode, b64encode
from pdf2image import convert_from_bytes
from io import BytesIO
import requests
import asyncio


eventLoop = asyncio.new_event_loop()

API_KEY = ""
HEADERS = {"Content-Type": "application/json", "api-key": API_KEY,}
ENDPOINT = "https://<hub>.openai.azure.com/openai/deployments/<model-name>/chat/completions?api-version=2024-02-15-preview"

app = Flask(__name__)

async def requestsPostAPI(payload: object):
    return requests.post(ENDPOINT, headers=HEADERS, json=payload)

@app.post('/')
def postDefault():
    parseToBytes = b64decode(request.data, validate = True)
    if parseToBytes.startswith(b'%PDF'):
        document = convert_from_bytes(b64decode(request.data), dpi = 450)
        len(document) # COUNT PAGES: MAKE TEMPLATE
        for page in document:
            with BytesIO() as BytesIOFork:
                page.save(BytesIOFork, format = 'JPEG')
                data = b64encode(BytesIOFork.getvalue()).decode(encoding = 'utf-8')
                BytesIOFork.close()
                payload = {
                    "messages": [
                        {"role": "system","content": "Voce e uma ia que le imagens e descreve o conteudo EM PORTUGUES"},
                        {"role": "user","content": [{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{data}"}}]}
                    ],
                    "temperature": 0.0,
                    "top_p": 0.95,
                    "max_tokens": 800
                }
        response = eventLoop.run_until_complete(requestsPostAPI(payload))

        return response.json()
    else:
        arrayStartWithBytes = [b'\x89PNG', b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1'] #Default bytes to check PNG JPEG JPG
        for checkItem in arrayStartWithBytes:
            if parseToBytes.startswith(checkItem):
                return jsonify({"message": "waiting"})
            else:
                return jsonify({"message": "None"})
            
if __name__ == '__main__':      
    app.run(host = '127.0.0.1', port = 3000, debug = True) 
