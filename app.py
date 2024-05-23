from flask import Flask, request, jsonify
import os
from services.audio_service import process_audio_file
from utils.text_processing_utils import recognize_speech
from lib.ntlp import segment_text

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_audio_file_endpoint():
    # Call audio processing function
    features = process_audio_file(request.files['file'])
    transcript = recognize_speech(features)
    time_stamps = segment_text(transcript)

    return jsonify({'time_stamps': time_stamps})

if __name__ == '__main__':
    app.run(debug=True)