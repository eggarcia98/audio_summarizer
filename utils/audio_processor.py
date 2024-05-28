"""Module to load local audios"""
from pydub import AudioSegment
import os

def process_audio_file(output_audio_path):
    """Function to convert format audio to wav"""
    output_wav_audio_path = f"{output_audio_path}.wav"

    audio_no_wav = AudioSegment.from_file(output_audio_path)
    audio_no_wav.export(output_wav_audio_path, format="wav", codec="pcm_s16le")
    
    return output_wav_audio_path


def audio_remover(audio_path):
    """Function to remove files"""
    if os.path.exists(audio_path):
        os.remove(audio_path)
    else:
        print("The file does not exist")
