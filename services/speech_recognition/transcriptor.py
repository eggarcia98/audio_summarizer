"""Module to manage speech audio recognition"""

import whisper
from services.db.queries import insert_new_audio_transcript

MODEL = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the Whisper model.
    Returns the parsed transcript data.
    """
    result = MODEL.transcribe(audio_path)

    parsed_segments = [
        {
            'audio_end_time': segment['end'],
            'audio_start_time': segment['start'],
            'transcript': segment['text'].strip()
        }
        for segment in result['segments']
    ]

    audio_data = {'transcript': parsed_segments}
    insert_new_audio_transcript(audio_data)

    return audio_data
