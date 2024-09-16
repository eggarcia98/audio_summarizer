"""Module to manage async functions for audio processing and summarization"""

import json

from flask import Flask, request, jsonify
from flask_cors import cross_origin

from utils.audio_processor import handle_audio_input, audio_remover
from services.speech_recognition.transcriptor import transcribe_audio
from services.db.queries import fetch_saved_audio_transcript

app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def root_path():
    """GET - Root path"""
    return jsonify({"data": "root path"}), 200

@app.route('/summarize_audio', methods=['POST'])
@cross_origin("*")
def process_audio_file_endpoint():
    """
    POST - Summarize an audio file or a YouTube video.
    Transcribes audio from either a file or a URL and returns the transcript.
    """
    audio_file = request.files.get('audio', None)
    url = None

    if 'form-data' not in request.content_type:
        try:
            body = json.loads(request.data)
            url = body.get('url', None)
        except (json.JSONDecodeError, KeyError):
            return jsonify({'error': 'Invalid request format or missing URL'}), 400

    if not url and not audio_file:
        return jsonify({'error': 'Either a URL or an audio file must be provided.'}), 400

    downloaded_audio = handle_audio_input(url, audio_file)
    if not downloaded_audio:
        return jsonify({'error': 'Error processing audio input.'}), 500

    audio_path = downloaded_audio.get("filename")
    audio_id = downloaded_audio.get("id")
    transcript_data = fetch_saved_audio_transcript(audio_id)
    if transcript_data:
        audio_remover(downloaded_audio.get("filename"))
        return jsonify(transcript_data), 200

    transcript_data = transcribe_audio(audio_path)
    audio_remover(audio_path)

    return jsonify(transcript_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=6030, host="0.0.0.0")
