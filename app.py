"""Module to manage async functions for audio processing and summarization"""

import json

from flask import Flask, jsonify, request
from flask_cors import cross_origin

from services.db.queries import (
    fetch_saved_audio_transcript,
    insert_new_audio_transcript,
)
from services.db import init_db
from services.speech_recognition.transcriptor import transcribe_audio
from utils.audio_processor import (
    audio_remover,
    get_audio_identificator,
    handle_audio_input,
)

app = Flask(__name__)



# Initialize the database
init_db(app)


@app.route("/", methods=["GET"])
@cross_origin()
def root_path():
    """GET - Root path"""
    return jsonify({"data": "root path"}), 200


def is_json_request(req):
    """Check if the request content type is JSON."""
    return "form-data" not in req.content_type


def handle_json_request(req):
    """Parse and validate the JSON request body."""
    try:
        body = json.loads(req.data)
        return body.get("url", None)
    except (json.JSONDecodeError, KeyError) as exc:
        raise ValueError("Invalid request format or missing URL") from exc


@app.route("/summarize_audio", methods=["POST"])
@cross_origin("*")
def process_audio_file_endpoint():
    """
    POST - Summarize an audio file or a YouTube video.
    Transcribes audio from either a file or a URL and returns the transcript.
    """
    audio_source = None

    try:
        if is_json_request(request):
            audio_source = handle_json_request(request)
        else:
            audio_source = request.files.get("audio", None)
    except ValueError as e:
        return jsonify({"error": e}), 400

    if not audio_source:
        return (
            jsonify({"error": "Either a URL or an audio file must be provided."}),
            400,
        )

    audio_id = get_audio_identificator(audio_source, is_json_request(request))
    transcript_data = fetch_saved_audio_transcript(audio_id)
    if transcript_data:
        audio_remover(transcript_data.get("filename"))
        return jsonify(transcript_data), 200

    downloaded_audio = handle_audio_input(audio_source, is_json_request(request))
    downloaded_audio["id"] = audio_id
    if not downloaded_audio:
        return jsonify({"error": "Error processing audio input."}), 500

    audio_filename_result = downloaded_audio.get("filename")
    transcript = transcribe_audio(audio_filename_result)
    fragments_size = len(transcript)

    downloaded_audio["transcript"] = transcript
    downloaded_audio["size"] = fragments_size

    audio_remover(audio_filename_result)

    # insert_new_audio_transcript(downloaded_audio)
    return jsonify(downloaded_audio), 200


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
