"""Audio Transcriptions Model Class"""

from typing import Dict, List, Optional, Union

from sqlalchemy.exc import SQLAlchemyError

from services.db import db


class AudioTranscript(db.Model):
    """Model representing an audio transcript in the database."""

    __tablename__ = "audio_transcripts"

    id = db.Column(db.String(200), primary_key=True)
    filename = db.Column(db.String(255))
    transcript = db.Column(db.Text)  # Use Text for potentially longer transcriptions
    source_url = db.Column(db.String(80), nullable=True)
    duration = db.Column(
        db.Integer, nullable=True
    )  # Better to store duration as Integer

    def __repr__(self) -> str:
        return f"<AudioTranscript {self.filename}>"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Convert AudioTranscript object to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "transcript": self.transcript,
            "source_url": self.source_url,
            "duration": self.duration,
        }

    @classmethod
    def get_all_audio_transcripts(cls, *columns) -> List[Dict[str, Union[str, int]]]:
        """Fetch all audio transcriptions with optional specific columns."""

        query = cls.query.with_entities(*columns) if columns else cls.query
        results = query.all()
        column_names = (
            [col.key for col in columns] if columns else cls.__table__.columns.keys()
        )
        return [dict(zip(column_names, row)) for row in results]

    @classmethod
    def get_audio_transcript_by_id(
        cls, audio_file_id: str
    ) -> Optional["AudioTranscript"]:
        """Fetch a single audio transcript by its ID."""

        return cls.query.get(audio_file_id)

    @classmethod
    def insert_new_audio_transcript(
        cls, audio_transcript_data: "AudioTranscript"
    ) -> Optional["AudioTranscript"]:
        """Insert a new audio transcript record into the database.

        Args:
            audio_transcript_data: An instance of AudioTranscript to add.

        Returns:
            The inserted AudioTranscript instance if successful, None otherwise.
        """

        try:
            db.session.add(audio_transcript_data)
            db.session.commit()
            print("Record inserted successfully.")
            return audio_transcript_data
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Failed to insert record: {e}")
            return None
