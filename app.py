from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = 'gsamuel-morse-code-v1.p.rapidapi.com'

def is_morse_code(text):
    return all(c in '.- ' for c in text.strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    if is_morse_code(text):
        convert_type = 'decode'
    else:
        convert_type = 'encode'

    url = f"https://{RAPIDAPI_HOST}/{convert_type}"
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    payload = {'text': text}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json().get('morse', 'Error in conversion')
    else:
        result = 'Error in conversion'

    return render_template('index.html', result=result, input_text=text)

if __name__ == '__main__':
    app.run(debug=True)