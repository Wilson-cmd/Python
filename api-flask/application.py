from flask import Flask, jsonify, request
from base64 import b64decode, b64encode
from pdf2image import convert_from_bytes
from io import BytesIO
import requests
import asyncio
from jinja2 import Template
import json
import ast

API_KEY = ""
HEADERS = {"Content-Type": "application/json", "api-key": API_KEY,}
ENDPOINT = "https://<hub>.openai.azure.com/openai/deployments/<model-name>/chat/completions?api-version=2024-02-15-preview"

app = Flask(__name__)

# CREATE REQUEST TO AZURE OPENAI
async def requestsPostAPI(payload: object):
    return requests.post(ENDPOINT, headers=HEADERS, json=payload)

#  PARSER TO JSON
async def astLiteralEvalToJson(literalString: str) -> json:
    return json.loads(json.dumps(ast.literal_eval(literalString)))

# CREATE LIST'S BASE64
async def createBase64FromList(document: list) -> list:
    listDataBase64 = list()
    for page in document:
        with BytesIO() as BytesIOFork:
            page.save(BytesIOFork, format = 'JPEG')
            listDataBase64.append(b64encode(BytesIOFork.getvalue()).decode(encoding = 'utf-8'))
            BytesIOFork.close()
    return listDataBase64
# CREATE TEMPLATE FOR CONTENT

async def createContent(listDataBase64: list):
    returnAsync = await astLiteralEvalToJson(Template(
        '{%- set listToSetBase64 = [] -%} \
        {%- macro content(listDataBase64, arr) -%} \
            {%- for base64 in listDataBase64 -%} \
                {{ arr.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,%s" % base64}})|replace("None", "") }} \
            {%- endfor -%} \
        {{listToSetBase64|list}} \
        {%- endmacro -%} \
        {{ content(listDataBase64, listToSetBase64) }} \
    ').render(listDataBase64 = listDataBase64))
    return returnAsync




async def createPayloadWithFullMessage(*args):
    returnAsync = await astLiteralEvalToJson(Template("{'messages': [{'role': 'system','content': '{{ prompt }}'}, \
    {'role': 'user','content': {{imageURLWithContextType}}} \
    ],'max_tokens': {{ maxToken }},'stream': {{ stream }}}").render(
        maxToken = args[0] ,stream = args[1]
        ,prompt = args[2] ,imageURLWithContextType = args[3]
    ))
    return returnAsync



@app.post('/')
def postDefault():
    parseToBytes = b64decode(request.data, validate = True)
    if parseToBytes.startswith(b'%PDF'):
        document = convert_from_bytes(b64decode(request.data), dpi = 450)
        
        listDataBase64 = asyncio.run(createBase64FromList(document))
        imageURLWithContextType = asyncio.run(createContent(listDataBase64))
        
        payload = asyncio.run(createPayloadWithFullMessage(
        800
        ,"False"
        ,"Voce e uma ia que le imagens e descreve o conteudo EM PORTUGUES"
        ,imageURLWithContextType))
        
        response = asyncio.run(requestsPostAPI(payload))
        return response.json()           



            
if __name__ == '__main__':      
    app.run(host = '127.0.0.1', port = 3000, debug = True) 
