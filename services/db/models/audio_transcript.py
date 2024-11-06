"""Audio Transcriptions Model Class"""

from services.db import db


class AudioTranscript(db.Model):
    """Audio Transcript Model Configuration"""

    __tablename__ = "audio_transcripts"

    id = db.Column(db.String(200), primary_key=True)
    filename = db.Column(db.String(255))
    transcript = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.filename}>"
