from services.db.connection import get_cursor

def fetch_saved_audio_summary():
    """Function to fetch all users"""
    query = "SELECT id, name FROM categories"
    with get_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
