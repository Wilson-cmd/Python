import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
load_dotenv()

file = open('schema.json', 'r')
data = json.load(file)
file.close()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/api', methods=['GET'])
def api():
    id = request.args.get('id', type = int)
    if(id == 0 or id == None):
        return jsonify(data)
    else:
       for index in range(len(data)):
            while(data[index]['Id']==id):
                return jsonify(data[index])
            
        
app.run(host='127.0.0.1', port=3000, debug=True) 