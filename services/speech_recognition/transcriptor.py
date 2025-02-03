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

        formatted_transcript = format_transcript(transcript)

        return formatted_transcript

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def ms_to_seconds(ms):
    """Convert milliseconds to seconds."""
    return round(ms / 1000, 2)


def format_transcript(transcript):
    """Format the transcript data for the API response."""

    words_dict_list = [word.__dict__ for word in transcript.words]

    # Process word-level timestamps into sentence-level timestamps
    sentences = []
    current_sentence = []
    sentence_start_time = None

    for word in words_dict_list:
        if sentence_start_time is None:
            sentence_start_time = ms_to_seconds(word["start"])

        current_sentence.append(word["text"])

        # If the word ends with a sentence-ending punctuation, finalize the sentence
        if word["text"].endswith((".", "!", "?")):
            sentence_text = " ".join(current_sentence)
            sentence_end_time = ms_to_seconds(word["end"])

            sentences.append(
                {
                    "audio_start_time": sentence_start_time,
                    "audio_end_time": sentence_end_time,
                    "transcript": sentence_text,
                }
            )

            # Reset for the next sentence
            current_sentence = []
            sentence_start_time = None

    # Print the formatted transcript
    formatted_output = {"transcript": sentences}

    return formatted_output
