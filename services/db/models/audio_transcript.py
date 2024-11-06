"""Audio Transcriptions Model Class"""

from services.db import db


class AudioTranscript(db.Model):
    """Audio Transcript Model Configuration"""

    __tablename__ = "audio_transcripts"

    id = db.Column(db.String(200), primary_key=True)
    filename = db.Column(db.String(255))
    transcript = db.Column(db.String(255))
    source_url = db.Column(db.String(80), nullable=True)
    duration = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f"<AudioTranscript {self.filename}>"

    def to_dict(self):
        """Convert AudioTranscript object to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "transcript": self.transcript,
            "source_url": self.source_url,
            "duration": self.duration,
        }

    @classmethod
    def select_all_audio_transcript(cls, *columns):
        """Get all the audio transcriptions saved"""
        return cls.query.with_entities(*columns).all()
