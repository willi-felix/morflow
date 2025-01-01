import os
from flask import Flask, send_from_directory, render_template, request, jsonify
from morse3 import Morse
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import time
import gevent
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=4)

def is_morse_code(text):
    return all(c in '.- ' for c in text.strip())

@lru_cache(maxsize=128)
def convert_morse(text):
    if is_morse_code(text):
        return Morse(text).morseToString()
    else:
        return Morse(text).stringToMorse()

@app.route('/')
def index():
    return render_template('index.html', input_text='', result='', processing_time=None)

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'public'), 'sitemap.xml', mimetype='application/xml')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text', '').strip()
    start_time = time.time()

    try:
        result = convert_morse(text)
    except Exception as e:
        result = f"Error: {e}"

    processing_time = round(time.time() - start_time, 4)

    return render_template('index.html', result=result, input_text=text, processing_time=processing_time)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json()
    text = data.get('text', '').strip()

    try:
        result = convert_morse(text)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()