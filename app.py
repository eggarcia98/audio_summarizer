"""Module to manage async functions for audio processing and summarization"""

import os

from backend.factory import create_flask_app

if __name__ == "__main__":
    app = create_flask_app()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
