"""Module to manage async functions"""
import asyncio

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import cross_origin

from utils.audio_processor import process_audio_file, audio_remover, get_audio_from_youtube
from utils.transcript_processor import merge_overlapping_transcripts
from services.speech_recognition.recognition import recognize_speech

app = Flask(__name__)


@app.route('/summarize_audio', methods=['POST'])
@cross_origin()
def process_audio_file_endpoint():
    """Return a transcription of an audio"""
    body = {}
    
    audio_bytes = ""
    url = ""
    
    if ('json' in request.content_type):
        body = request.get_json()
        url = body['url']
    else:
        audio_bytes = request.get_data()

    source_audio_path = ""
    wav_audio_path = ""

    if not url and not audio_bytes:
        return jsonify({'error': 'Either a URL or an audio file must be provided.'}), 400
    

    if url:
        source_audio_path = get_audio_from_youtube(url)

    if audio_bytes and source_audio_path == "":
        now = datetime.now()
        source_audio_path = f"{now}.mp3"
        with open(source_audio_path, 'wb') as output_file:
            output_file.write(audio_bytes)

    wav_audio_path = process_audio_file(source_audio_path)
    transcript = asyncio.run(recognize_speech(wav_audio_path))
    
    audio_remover(source_audio_path)
    audio_remover(wav_audio_path)

    merged_transcript = merge_overlapping_transcripts(transcript)
    return jsonify({'data': merged_transcript}), 200

if __name__ == '__main__':
    app.run(debug=True, port=6030)
