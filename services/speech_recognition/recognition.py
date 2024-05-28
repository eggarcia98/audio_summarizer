"""Module to manage async functions"""
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
from services.speech_recognition.transcriptor import transcribe_audio
from utils.audio_processor import audio_splitter, queue_audios_chunks

async def recognize_audio_speech(audio_chunk, initial_time=0):
    """Recognize speech in a given audio segment."""
    recognizer = sr.Recognizer()
    segment_duration_ms = len(audio_chunk)
    
    segment_chunk_duration_ms = 5000  
    transcripts = []

    for start_offset in range(0, segment_duration_ms, segment_chunk_duration_ms):
        end_offset = min(start_offset + segment_chunk_duration_ms, segment_duration_ms)

        segment_chunk = audio_chunk[start_offset:end_offset]
        wav_segment_chunk = segment_chunk.export(format="wav", codec="pcm_s16le")
        with sr.AudioFile(wav_segment_chunk) as audio_source:
            audio_data = recognizer.record(audio_source)
            transcript = await transcribe_audio(recognizer, audio_data)
            if transcript:
                transcripts.append(dict(
                    {
                        "transcript": transcript,
                        "chunk_start_time": initial_time,
                        "audio_start_time": initial_time + (start_offset / 1000),
                        "audio_end_time": initial_time + (end_offset / 1000),
                    }
                ))
    return transcripts


async def recognize_speech(audio_file_path):
    """Recognize speech in an audio file by splitting it into chunks."""
    audio = AudioSegment.from_wav(audio_file_path)

    audio_chunks = audio_splitter(audio, 120000)
    audios_to_process = queue_audios_chunks(audio_chunks, recognize_audio_speech)

    transcripts = await asyncio.gather(*audios_to_process)
    return [transcript for sublist in transcripts for transcript in sublist]
