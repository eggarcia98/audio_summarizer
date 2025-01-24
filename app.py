"""Module to manage async functions for audio processing and summarization"""

from backend.factory import create_flask_app

if __name__ == "__main__":
    app = create_flask_app()
    app.run(host="0.0.0.0", port=8080)
