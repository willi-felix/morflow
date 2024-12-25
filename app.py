from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

def is_morse_code(text):
    return all(c in '.- ' for c in text.strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    if is_morse_code(text):
        convert_type = 'from_morse'
    else:
        convert_type = 'to_morse'

    url = f"https://{RAPIDAPI_HOST}/morse.json"
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    querystring = {"text": text} if convert_type == 'from_morse' else {"text": text, "speed": "5", "tone": "700"}
    response = requests.post(url, headers=headers, params=querystring)

    result = response.json().get('morse', 'Error in conversion')
    return render_template('index.html', result=result, input_text=text)

if __name__ == '__main__':
    app.run(debug=True)