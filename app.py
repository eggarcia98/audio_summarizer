from flask import Flask, request, jsonify
from services.audio_service import process_audio_file
from utils.text_processing_utils import recognize_speech
from lib.ntlp import segment_text
import asyncio
from datetime import datetime



app = Flask(__name__)



@app.route('/summarize_audio', methods=['POST'])
def process_audio_file_endpoint():
    file = request.data

    now = datetime.now()

    output_audio_path = f"{now} + .mp3"
    with open(output_audio_path, 'wb') as output_file:
        output_file.write(file)

    output_audio_path = process_audio_file(output_audio_path)

    transcript = asyncio.run(recognize_speech(output_audio_path))
    print("HERE 5")
    # time_stamps = segment_text(transcript)


    return transcript

    # return jsonify({'time_stamps': time_stamps})

@app.route('/')
def process_home():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, port=6030)