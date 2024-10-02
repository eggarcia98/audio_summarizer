"""Module to define Database Transactions"""

import json
from services.db.connection import get_cursor

def fetch_saved_audio_transcript(audio_file_id):
    """Function to fetch all saved audio trancriptions"""
    query = f'SELECT * FROM audio_transcripts WHERE id = \'{audio_file_id}\''
    with get_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()


def insert_new_audio_transcript(downloaded_audio):
    """Function to save a new transcripted audio to the database"""
    insert_query = """
            INSERT INTO audio_transcripts (id, filename, transcript)
            VALUES (%s, %s, %s);"""

    with get_cursor() as cursor:
        audio_id = downloaded_audio['id']
        filename = downloaded_audio['filename']
        transcript = json.dumps(downloaded_audio['transcript'])
        cursor.execute(insert_query, (audio_id, filename, transcript))

        print("Record inserted successfully.")
