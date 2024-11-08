"""Module to define Database Transactions"""

import json

from .models.audio_transcript import AudioTranscript


def get_all_audio_transcripts():
    """Get all saved audio transcript from Database"""
    return AudioTranscript.select_all_audio_transcript(
        AudioTranscript.id,
        AudioTranscript.duration,
        AudioTranscript.filename,
        AudioTranscript.source_url,
    )


def get_single_audio_transcript(audio_file_id):
    """Function to fetch all saved audio trancriptions"""

    required_audio = AudioTranscript(id=audio_file_id)
    result = required_audio.select_single_audio_transcript()

    return result.to_dict()


def add_new_audio_transcript(downloaded_audio):
    """Function to save a new transcripted audio to the database"""

    new_audio_transcript = AudioTranscript(
        id=downloaded_audio["id"],
        filename=downloaded_audio["filename"],
        transcript=json.dumps(downloaded_audio["transcript"]),
    )

    return AudioTranscript.insert_new_audio_transcript(new_audio_transcript)
