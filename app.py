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

def check_connection():
    url = f"https://{RAPIDAPI_HOST}/"
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Connection to API successful.")
        else:
            print(f"Connection to API failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

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
        result = f"Error in conversion: {response.text}"

    return render_template('index.html', result=result, input_text=text)

if __name__ == '__main__':
    check_connection()
    app.run(debug=True)