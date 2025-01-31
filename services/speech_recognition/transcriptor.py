"""Module to manage speech audio recognition"""

import os

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "api_key")


def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the external API service.
    Returns the parsed transcript data.
    """
    try:
        # Open the audio file in binary mode
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)

        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
            return []

        print(transcript.text)
        return transcript.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
