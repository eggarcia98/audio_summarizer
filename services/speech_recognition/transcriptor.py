"""Module to manage speech audio recognition"""

import os

import requests

WHISPER_API_URL = os.getenv(
    "WHSIPER_API_URL", "http://localhost:8081/get-transcript-audio"
)


def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the external API service.
    Returns the parsed transcript data.
    """
    try:
        # Open the audio file in binary mode
        with open(audio_path, "rb") as audio_file:
            print(audio_file)
            # Send a POST request with the audio file
            response = requests.post(
                WHISPER_API_URL,
                files={"file": audio_file},  # Attach the file to the 'file' field
                timeout=60 * 10,  # Set a timeout of 60 * 10 seconds
            )

            # Check if the request was successful
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                print("Response:", response.text)
                return []
            # Parse the JSON response

            data = response.json()

            transcription_raw_data = data.get("transcription", "")

            segments = transcription_raw_data.get("segments", [])

            parsed_segments = [
                {
                    "audio_end_time": segment["end"],
                    "audio_start_time": segment["start"],
                    "transcript": segment["text"].strip(),
                }
                for segment in segments
            ]

            print("Transcription:", parsed_segments)

            return parsed_segments

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
