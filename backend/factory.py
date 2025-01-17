"""Application factory for creating the Flask app."""

from flask import Flask
from backend.routes import register_routes

from services.db import init_db


def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    init_db(app)  # Initialize the database
    register_routes(app)  # Register application routes
    return app
