from flask import Flask, jsonify, request
from base64 import b64decode, b64encode
from pdf2image import convert_from_bytes
from io import BytesIO


app = Flask(__name__)

@app.post('/')
def postDefault():
    document = convert_from_bytes(b64decode(request.data), dpi = 450)
    for page in document:
        with BytesIO() as BytesIOFork:
            page.save(BytesIOFork, format = 'JPEG')
            data = b64encode(BytesIOFork.getvalue()).decode(encoding = 'utf-8')
            BytesIOFork.close()
        return jsonify({"base64": data})