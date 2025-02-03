"""Route definitions for the Flask app."""

from flask import jsonify, request
from flask_cors import cross_origin

from services.db.queries import (
    add_new_audio_transcript,
    get_all_audio_transcripts,
    get_single_audio_transcript,
)
from services.speech_recognition.transcriptor import transcribe_audio
from utils.audio_processor import (
    audio_remover,
    get_audio_duration,
    get_audio_identificator,
    handle_audio_input,
)
from utils.request_helpers import (
    is_json_request,
    handle_audio_source,
)


def register_routes(app):
    """Register all routes for the Flask application."""

    @app.route("/", methods=["GET"])
    @cross_origin("*")
    def root_path():
        """Root endpoint."""
        return jsonify({"data": "root"}), 200

    @app.route("/saved_audio_transcripts", methods=["GET"])
    @cross_origin()
    def get_saved_audio_transcripts():
        """Retrieve saved audio transcripts."""
        audio_transcripts = get_all_audio_transcripts()
        return jsonify({"data": audio_transcripts})

    @app.route("/summarize_audio", methods=["POST"])
    @cross_origin("*")
    def summarize_audio():
        """
        Summarize audio from a file or URL.
        Transcribes audio and returns the transcript.
        """
        try:
            audio_source = handle_audio_source(request)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        if not audio_source:
            return (
                jsonify({"error": "Either a URL or an audio file must be provided."}),
                400,
            )

        return process_audio(audio_source)


def process_audio(audio_source):
    """Process and summarize the provided audio source."""
    audio_id = get_audio_identificator(audio_source, is_json_request(request))
    duration = get_audio_duration(audio_source, is_json_request(request))
    source_url = audio_source if is_json_request(request) else ""

    # existing_transcript = get_single_audio_transcript(audio_id)
    # if existing_transcript:
    #     audio_remover(existing_transcript.get("filename"))
    #     return jsonify(existing_transcript), 200

    downloaded_audio = handle_audio_input(audio_source, is_json_request(request))
    if not downloaded_audio:
        return jsonify({"error": "Error processing audio input."}), 500

    downloaded_audio["transcript"] = transcribe_audio(downloaded_audio["filename"])
    downloaded_audio.update(
        {
            "id": audio_id,
            "size": len(downloaded_audio["transcript"]),
            "duration": duration,
            "source_url": source_url,
        }
    )

    audio_remover(downloaded_audio["filename"])
    # add_new_audio_transcript(downloaded_audio)
    return jsonify(downloaded_audio), 200
