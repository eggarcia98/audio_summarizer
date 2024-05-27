import speech_recognition as sr
import asyncio
from pydub import AudioSegment

async def transcribe_audio_chunk(recognizer, audio_chunk):
    try:
        return recognizer.recognize_google(audio_chunk)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return f"API request error: {e}"

# async def recognize_speech_chunk(audio_file_path, chunk_length_ms=1000):
    
#     recognizer = sr.Recognizer()
#     audio = AudioSegment.from_wav(audio_file_path)
#     duration_ms = len(audio)
    
#     transcripts = []
#     for start_ms in range(0, duration_ms, chunk_length_ms):
#         end_ms = min(start_ms + chunk_length_ms, duration_ms)
#         audio_chunk = audio[start_ms:end_ms]
#         with sr.AudioFile(audio_chunk.export("chunk.wav", format="wav")) as source:
#             audio_data = recognizer.record(source)
#             transcript = transcribe_audio_chunk(recognizer, audio_data)
#             if transcript:
#                 transcripts.append((transcript, start_ms / 1000, end_ms / 1000))
    
#     return transcripts

async def recognize_speech_chunk(audio_chunk, start_time):
    recognizer = sr.Recognizer()
    transcripts = []
    chunk_length_ms = 3000
    duration_ms = len(audio_chunk)


    for start_ms in range(0, duration_ms, chunk_length_ms):
        end_ms = min(start_ms + chunk_length_ms, duration_ms)
        audio_chunk_2 = audio_chunk[start_ms:end_ms]
        with sr.AudioFile(audio_chunk_2.export(format="wav", codec="pcm_s16le")) as source:
            audio_data = recognizer.record(source)
            transcript = await transcribe_audio_chunk(recognizer, audio_data)
            if transcript:
                transcripts.append((transcript, start_time, start_time + (start_ms / 1000), start_time + (end_ms / 1000)))
    return transcripts
        

async def recognize_speech(audio_file_path, chunk_length_ms=1000):
    audio = AudioSegment.from_wav(audio_file_path)
    chunk_length_ms = 30000  # Split the audio into 1-minute chunks

    tasks = []
    for start_ms in range(0, len(audio), chunk_length_ms):
        end_ms = min(start_ms + chunk_length_ms, len(audio))
        audio_chunk = audio[start_ms:end_ms]
        start_time = start_ms / 1000
        task = asyncio.create_task(recognize_speech_chunk(audio_chunk, start_time))
        tasks.append(task)

    transcripts = await asyncio.gather(*tasks)
    return transcripts
