"""Module to manage async functions"""
import asyncio

from datetime import datetime
from flask import Flask, request
from flask_cors import cross_origin

from utils.audio_processor import process_audio_file, audio_remover
from utils.transcript_processor import merge_overlapping_transcripts
from services.speech_recognition.recognition import recognize_speech

app = Flask(__name__)


@app.route('/summarize_audio', methods=['POST'])
@cross_origin()
def process_audio_file_endpoint():
    """Return a transcription of an audio"""
    audio_bytes = request.data
    now = datetime.now()

    print(audio_bytes)


    new_audio_path = f"{now}.mp3"
    with open(new_audio_path, 'wb') as output_file:
        output_file.write(audio_bytes)

    wav_audio_path = process_audio_file(new_audio_path)
    transcript = asyncio.run(recognize_speech(wav_audio_path))
    
    audio_remover(new_audio_path)
    audio_remover(wav_audio_path)

    merged_transcript = merge_overlapping_transcripts(transcript)
    return merged_transcript

if __name__ == '__main__':
    app.run(debug=True, port=6030)
