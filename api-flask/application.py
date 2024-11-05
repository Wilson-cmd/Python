from flask import Flask, jsonify, request
from base64 import b64decode, b64encode
from pdf2image import convert_from_bytes
from io import BytesIO
import requests
import time

API_KEY = ""
HEADERS = {"Content-Type": "application/json", "api-key": API_KEY,}
ENDPOINT = "https://<hub>.openai.azure.com/openai/deployments/<mode-name>/chat/completions?api-version=2024-02-15-preview"

app = Flask(__name__)

def requestsPostAPI(payload):
    time.sleep(10)
    return requests.post(ENDPOINT, headers=HEADERS, json=payload).json()

@app.post('/')
def postDefault():
    document = convert_from_bytes(b64decode(request.data), dpi = 450)
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
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 800
                }
            response = requestsPostAPI(payload)
        return response
            
        
app.run(host = '127.0.0.1', port = 3000, debug = True) 
