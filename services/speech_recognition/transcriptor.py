from services.db.queries import insert_new_audio_transcript

def transcribe_audio(model, audio_path):
    """
    Transcribes the audio file using the Whisper model.
    Returns the parsed transcript data.
    """
    result = model.transcribe(audio_path)

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


