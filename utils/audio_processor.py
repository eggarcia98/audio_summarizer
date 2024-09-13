"""Module to manage async functions"""
import asyncio
import os
from operator import itemgetter
from pydub import AudioSegment
import  yt_dlp
 # client to many multimedia portals

def get_audio_from_youtube(yt_url):
    """function to get an audio from youtube"""

    downloaded_audio_dict = dict({})

    def progress_hook(d):
        nonlocal downloaded_audio_dict

        if d['status'] == 'finished':
            downloaded_audio_dict = dict({
                'filename': f'{d["filename"].split(".")[0]}.mp3',
                'id': d['info_dict']['id']
            })

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    
    return downloaded_audio_dict

import hashlib


def generate_audio_hash_identificator(audio_payload):
    """Create a new SHA-256 hash object"""
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the file
    sha256_hash.update(audio_payload)

    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

def get_audio_from_audio_file(audio_file):
    """Function to get an audio from audio bytes"""
    audio_bytes = audio_file.read()
    audio_name = audio_file.filename

    destine_audio_path = f"{audio_name}.mp3"

    with open(destine_audio_path, 'wb') as output_file:
        output_file.write(audio_bytes)

    return dict({
        'filename': destine_audio_path,
        "id": generate_audio_hash_identificator(audio_bytes)
    })


def process_audio_file(output_audio_path):
    """Function to convert format audio to wav"""
    output_wav_audio_path = f"{output_audio_path}.wav"

    audio_no_wav = AudioSegment.from_file(output_audio_path)
    audio_no_wav.export(output_wav_audio_path, format="wav", codec="pcm_s16le")
   
    return output_wav_audio_path

def audio_splitter(audio, chunk_length_ms=30000):
    """Function to split an audio into chunks with a specific length in ms"""
    audio_chunks = []

    for start_ms in range(0, len(audio), chunk_length_ms):
        end_ms = min(start_ms + chunk_length_ms, len(audio))
        audio_content = audio[start_ms:end_ms]
        start_time = start_ms / 1000
        chunk_data = dict({"start_time": start_time, "audio_content": audio_content})
        audio_chunks.append(chunk_data)

    return audio_chunks

def queue_audios_chunks(audio_chunks, promise_recognize_speech):
    """Function that create a list of audios chunks pending to process"""
    audios_to_process = []

    for audio_chunk in audio_chunks:
        audio_content, start_time = itemgetter('audio_content', 'start_time')(audio_chunk)
        task = asyncio.create_task(promise_recognize_speech(audio_content, start_time))
        audios_to_process.append(task)

    return audios_to_process


def audio_remover(audio_path):
    """Function to remove files"""
    if os.path.exists(audio_path):
        os.remove(audio_path)
    else:
        print("The file does not exist")
