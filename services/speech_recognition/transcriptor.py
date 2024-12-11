"""Module to manage speech audio recognition"""

import os
import torch

import whisper

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"  
print("Device: ", DEVICE)

MODEL = whisper.load_model(WHISPER_MODEL, device=DEVICE)


def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the Whisper model.
    Returns the parsed transcript data.
    """

    print("Device: ", DEVICE)
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
