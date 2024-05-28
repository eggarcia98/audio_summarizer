"""Module to manage async functions"""
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
from transcriptor import transcribe_audio

async def recognize_speech_chunk(audio_chunk, start_time):
    """Recognize speech in a given audio chunk."""
    recognizer = sr.Recognizer()
    transcripts = []
    chunk_length_ms = 3000
    duration_ms = len(audio_chunk)

    for start_ms in range(0, duration_ms, chunk_length_ms):
        end_ms = min(start_ms + chunk_length_ms, duration_ms)
        audio_chunk_part = audio_chunk[start_ms:end_ms]
        with sr.AudioFile(audio_chunk_part.export(format="wav", codec="pcm_s16le")) as source:
            audio_data = recognizer.record(source)
            transcript = await transcribe_audio(recognizer, audio_data)
            if transcript:
                transcripts.append(
                    (transcript, start_time, start_time + (start_ms / 1000), start_time + (end_ms / 1000))
                )
    return transcripts

async def recognize_speech(audio_file_path, chunk_length_ms=30000):
    """Recognize speech in an audio file by splitting it into chunks."""
    audio = AudioSegment.from_wav(audio_file_path)

    tasks = []
    for start_ms in range(0, len(audio), chunk_length_ms):
        end_ms = min(start_ms + chunk_length_ms, len(audio))
        audio_chunk = audio[start_ms:end_ms]
        start_time = start_ms / 1000
        task = asyncio.create_task(recognize_speech_chunk(audio_chunk, start_time))
        tasks.append(task)

    transcripts = await asyncio.gather(*tasks)
    return [transcript for sublist in transcripts for transcript in sublist]
