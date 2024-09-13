from services.db.connection import get_cursor
import json

def fetch_saved_audio_transcript(audio_file_id):
    """Function to fetch all users"""
    query = f'SELECT * FROM audio_transcripts WHERE id = \'{audio_file_id}\''
    with get_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()

def insert_new_audio_transcript(downloaded_audio):
    insert_query = """
            INSERT INTO audio_transcripts (id, filename, transcript)
            VALUES (%s, %s, %s);"""
        
    with get_cursor() as cursor:
        id = downloaded_audio['id']
        filename = downloaded_audio['filename']
        transcript = json.dumps(downloaded_audio['transcript'])
        cursor.execute(insert_query, (id, filename, transcript))
        
        print("Record inserted successfully.")
    