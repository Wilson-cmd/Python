from flask import Flask, jsonify, request
from base64 import b64decode, b64encode
from pdf2image import convert_from_bytes
from jinja2 import Template
from io import BytesIO
import requests
import asyncio
import json
import ast

app = Flask(__name__)

API_KEY = ""
HEADERS = {"Content-Type": "application/json", "api-key": API_KEY,}
ENDPOINT = "https://<hub>.openai.azure.com/openai/deployments/<model-name>/chat/completions?api-version=2024-02-15-preview"
MaxToken = 1500
Temperature = 0.0
Stream = False
Prompt = "Apos analisar o conteudo recebido, relate todas as informacoes que considerar relevante. Explique o porque considerou relevante a linha logica. Responda em pt-BR"


# CREATE REQUEST TO AZURE OPENAIMaxToken
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

# CREATEA PAYLOAD
async def createPayloadWithFullMessage(*args):
    returnAsync = await astLiteralEvalToJson(Template("{'messages': [{'role': 'system','content': '{{ prompt }}'}, \
    {'role': 'user','content': {{imageURLWithContextType}}} \
    ],'max_tokens': {{ maxToken }},'stream': {{ stream }}, 'temperature': {{temperature}}}").render(
        maxToken = args[0] ,stream = args[1], prompt = args[2] ,imageURLWithContextType = args[3], temperature = args[4]
    ))
    return returnAsync
arrayStartWithBytes = [b'\x89PNG', b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1']
@app.post('/')
def postDefault():
    parseToBytes = b64decode(request.data, validate = True)
    if parseToBytes.startswith(b'%PDF'):
        document = convert_from_bytes(b64decode(request.data), dpi = 450)
        
        listDataBase64 = asyncio.run(createBase64FromList(document))
        imageURLWithContextType = asyncio.run(createContent(listDataBase64))
        
        payload = asyncio.run(createPayloadWithFullMessage(MaxToken, Stream
        ,Prompt
        ,imageURLWithContextType, Temperature))
        
        response = asyncio.run(requestsPostAPI(payload))
        return response.json()
    else:
        for checkStartByte in arrayStartWithBytes:
            if parseToBytes.startswith(checkStartByte):
                imageURLWithContextType = asyncio.run(createContent([request.data.decode(encoding = 'utf-8')]))
                payload = payload = asyncio.run(createPayloadWithFullMessage(MaxToken, Stream
                ,Prompt
                ,imageURLWithContextType, Temperature))
                response = asyncio.run(requestsPostAPI(payload))
                return response.json()
            else:
                return jsonify({"code": "401", "message": "check if your base64 match JPEG, PDF or PNG"})




            
if __name__ == '__main__':      
    app.run(host = '0.0.0.0', port = 3000, debug = True) 
