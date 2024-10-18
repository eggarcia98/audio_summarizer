"""Module to handle audio tasks"""

import hashlib
import os

import yt_dlp


def set_youtube__config_downloader(downloaded_audio_dict):
    """Youtube download options"""

    def progress_hook(d):
        nonlocal downloaded_audio_dict

        if d["status"] == "finished":
            downloaded_audio_dict = dict(
                {
                    "filename": f'{d["filename"].split(".")[0]}.mp3',
                    "id": d["info_dict"]["id"],
                }
            )

    ydl_opts = {
        "format": "bestaudio/best",
        "restrictfilenames": True,
        "noplaylist": True,
        "extractor_retries": 4,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "source_address": "0.0.0.0",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "progress_hooks": [progress_hook],
    }

    return ydl_opts


def generate_audio_hash_identificator(audio_payload):
    """Create a new SHA-256 hash object"""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(audio_payload)

    return sha256_hash.hexdigest()


def get_audio_identificator(audio_source, is_json_request):
    """
    Get audio ID, necessary to use it to check if it already
    existed on database
    """

    if is_json_request:
        return get_youtube_audio_id(audio_source)

    return generate_audio_hash_identificator(audio_source.read())


def get_youtube_audio_id(yt_url):
    """Getting youtube audio identificator"""
    downloaded_audio_dict = dict({})

    ydl_opts = set_youtube__config_downloader(downloaded_audio_dict)

    # Extract metadata without downloading
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_url, download=False)
        return info_dict.get("id")


def get_audio_from_youtube(yt_url):
    """function to get an audio from youtube"""

    downloaded_audio_dict = dict({})
    ydl_opts = set_youtube__config_downloader(downloaded_audio_dict)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

    return downloaded_audio_dict


def get_audio_from_audio_file(audio_file):
    """Function to get an audio from audio bytes"""
    audio_bytes = audio_file.read()
    audio_name = audio_file.filename

    destine_audio_path = f"{audio_name}"

    with open(destine_audio_path, "wb") as output_file:
        output_file.write(audio_bytes)

    return dict(
        {
            "filename": destine_audio_path,
            "id": generate_audio_hash_identificator(audio_bytes),
        }
    )


def audio_remover(audio_path):
    """Function to remove files"""
    if os.path.exists(audio_path):
        os.remove(audio_path)
    else:
        print("The file does not exist")


def handle_audio_input(audio_source, is_json_request):
    """
    Handle fetching or processing of audio input from a URL or file.
    Returns the path to the audio file.
    """
    if is_json_request:
        downloaded_audio = get_audio_from_youtube(audio_source)
    else:
        downloaded_audio = get_audio_from_audio_file(audio_source)

    return downloaded_audio
