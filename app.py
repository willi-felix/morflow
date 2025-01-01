from flask import Flask, render_template, request, jsonify
from morse3 import Morse
import time

app = Flask(__name__)

def is_morse_code(text):
    return all(c in '.- ' for c in text.strip())

async def convert_morse(text):
    if is_morse_code(text):
        return Morse(text).morseToString()
    else:
        return Morse(text).stringToMorse()

@app.route('/')
def index():
    return render_template('index.html', input_text='', result='', processing_time=None)

@app.route('/convert', methods=['POST'])
async def convert():
    text = request.form.get('text', '').strip()
    start_time = time.time()

    try:
        result = await convert_morse(text)
    except Exception as e:
        result = f"Error: {e}"

    processing_time = round(time.time() - start_time, 4)

    return render_template('index.html', result=result, input_text=text, processing_time=processing_time)

@app.route('/api/convert', methods=['POST'])
async def api_convert():
    data = request.get_json()
    text = data.get('text', '').strip()

    try:
        result = await convert_morse(text)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)