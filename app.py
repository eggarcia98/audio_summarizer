"""Module to manage async functions"""
import asyncio

from datetime import datetime
from flask import Flask, request

from utils.audio_processor import process_audio_file
from services.speech_recognition.recognition import recognize_speech

app = Flask(__name__)

@app.route('/summarize_audio', methods=['POST'])
def process_audio_file_endpoint():
    """Return a transcription of an audio"""
    file = request.data
    now = datetime.now()

    output_audio_path = f"{now} + .mp3"
    with open(output_audio_path, 'wb') as output_file:
        output_file.write(file)

    output_audio_path = process_audio_file(output_audio_path)
    transcript = asyncio.run(recognize_speech(output_audio_path))
    
    return transcript

if __name__ == '__main__':
    app.run(debug=True, port=6030)
