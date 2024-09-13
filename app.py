"""Module to manage async functions"""

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import cross_origin

from utils.audio_processor import process_audio_file, audio_remover, get_audio_from_youtube, get_audio_from_audio_file
from services.db.queries import fetch_saved_audio_transcript, insert_new_audio_transcript


import whisper

# Cargar el modelo Whisper
model = whisper.load_model("base")

# Transcribir el archivo de audio


app = Flask(__name__)

@app.route("/",)
@cross_origin()
def root_path():
    """GET - Root path"""

    return jsonify({"data": "saved_audio_summary"}), 200

@app.route('/summarize_audio', methods=['POST'])
@cross_origin()
def process_audio_file_endpoint():
    """Return a transcription of an audio"""
    body = {}
    
    audio_file = ""
    url = ""


    if ('json' in request.content_type):
        body = request.get_json()
        url = body['url']
    elif ('audio' in request.files):
        audio_file = request.files['audio']

    source_audio_path = ""

    if not url and not audio_file:
        return jsonify({'error': 'Either a URL or an audio file must be provided.'}), 400

    if url:
        downloaded_audio_dict = get_audio_from_youtube(url)
        source_audio_path = downloaded_audio_dict['filename']
    elif audio_file and source_audio_path == "":
        downloaded_audio_dict = get_audio_from_audio_file(audio_file)
        source_audio_path = downloaded_audio_dict['filename']    

    saved_audio_transcript = fetch_saved_audio_transcript(downloaded_audio_dict['id'])
    if (saved_audio_transcript and len(saved_audio_transcript) > 0):
        downloaded_audio_dict = jsonify(saved_audio_transcript)
        audio_remover(source_audio_path)
        return downloaded_audio_dict

    # wav_audio_path = process_audio_file(source_audio_path)
    result = model.transcribe(source_audio_path)    
    audio_remover(source_audio_path)
    # audio_remover(wav_audio_path)

    parsed_segments = [
    {
        'audio_end_time': segment['end'],
        'audio_start_time': segment['start'],
        'transcript': segment['text'].strip()
    }
    for segment in result['segments']
    ]

    downloaded_audio_dict['transcript'] = parsed_segments
    insert_new_audio_transcript(downloaded_audio_dict)

    return downloaded_audio_dict, 200

if __name__ == '__main__':
    app.run(debug=True, port=6030, host="0.0.0.0")