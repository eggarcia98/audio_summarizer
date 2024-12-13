"""Module to manage speech audio recognition"""

import os
import whisper

# Get model name from env
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "./tiny.pt")
MODEL = whisper.load_model(WHISPER_MODEL)


def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the Whisper model.
    Returns the parsed transcript data.
    """

    result = MODEL.transcribe(audio_path)

    parsed_segments = [
        {
            "audio_end_time": segment["end"],
            "audio_start_time": segment["start"],
            "transcript": segment["text"].strip(),
        }
        for segment in result["segments"]
    ]

    transcript = parsed_segments

    return transcript
