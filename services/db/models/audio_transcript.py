"""Audio Transcriptions Model Class"""

from sqlalchemy import select

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

        results = cls.query.with_entities(*columns).all()
        column_names = [col.key for col in columns]  # Get column names from columns
        return [dict(zip(column_names, row)) for row in results]

    @classmethod
    def select_single_audio_transcript(cls, audio_file_id):
        """Select single audio transcrip filter by id"""

        query = select(AudioTranscript).where(AudioTranscript.id == audio_file_id)
        result = db.session.execute(query).first()

        return result

    @classmethod
    def insert_new_audio_transcript(cls, audio_transcript_data):
        """Function to save a new transcripted audio to the database"""

        db.session.add(audio_transcript_data)
        db.session.commit()

        print("Record inserted successfully.")
