# 🎧 Audio Processing and Summarization API

This is a RESTful API built using Flask to handle the processing and summarization of audio files. The API supports audio file uploads and URLs, transcribes the audio, and stores the results in a database. It also provides functionality to fetch saved transcripts.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Folder Structure](#folder-structure)
- [License](#license)

## ✨ Features
- **Audio Transcription**: Transcribe audio files or YouTube videos to text.
- **Audio Summarization**: Generate a summarized transcript of the audio.
- **Database Integration**: Store and retrieve audio transcripts.
- **Cross-Origin Resource Sharing (CORS)**: Handle requests from different origins.
- **File Upload & URL Processing**: Accept audio files or URLs to process.

## 🛠 Installation

Follow the steps below to install and run the project locally.

### Prerequisites
- Python 3.x
- Docker (optional for containerized setup)

### Step 1: Clone the repository
```sh
git clone https://github.com/your-username/audio-processing-api.git
cd audio-processing-api
```

### Step 2: Create a virtual environment
If you’re using a virtual environment:
```sh
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

### Step 3: Install dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a 

.env

 file in the root directory and add your configuration values:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URI=your-database-uri-here
SECRET_KEY=your-secret-key-here
```

### Step 5: Initialize the Database
Run the database initialization:
```sh
python app.py
```

## ⚙️ Configuration

You can customize the following configurations:
- **Database**: The app supports integration with a PostgreSQL database. Configure the database URI in the .envfile.
- **CORS**: CORS settings are enabled for all routes by default, allowing requests from any origin.

## 🚀 Usage

Once the API is running, you can interact with the endpoints.

### Starting the API Server
To start the Flask application, run the following command:

```sh
python app.py
```
This will start the Flask server on `http://localhost:8080`.

## 📡 API Endpoints

### GET /
Root path to check if the server is running.

**Response:**

```json
{
  "data": "root"
}
```

### GET /saved_audio_transcripts
Retrieve a list of all saved audio transcripts.

**Response:**

```json
{
  "data": [
    { "id": "123", "transcript": "This is an example transcript." },
    { "id": "124", "transcript": "Another example transcript." }
  ]
}
```

### POST /summarize_audio
Summarize an audio file or URL. The audio can either be uploaded as a file or provided as a URL in a JSON payload.

**Request:**

```json
{
  "url": "https://example.com/audio.mp3"
}
```

**OR via file upload:**
- Form data with `audio` as the key.

**Response:**
```json
{
  "id": "12345",
  "transcript": "This is a summarized transcript of the audio.",
  "size": 123,
  "duration": 56,
  "source_url": "https://example.com/audio.mp3"
}
```

## 🧪 Testing

### Step 1: Install Test Dependencies
```sh
pip install -r requirements-dev.txt
```

### Step 2: Run Tests
We use `pytest` for running tests. You can execute all the tests using:
```sh
pytest tests/
```

### Writing Tests
- Place your test files in the tests folder.
- Use `pytest` assertions for testing endpoints and functionality.

## 🗂 Folder Structure

The project follows a modular structure for maintainability and scalability:
```
├── Dockerfile                 # Docker configuration
├── app.py                     # Main entry point to run the Flask app
├── myenv                      # Virtual environment folder (do not commit)
├── requirements.txt           # Dependencies for the project
├── requirements-dev.txt       # Development dependencies for testing
├── services                   # Business logic and database interaction
│   ├── db                     # Database models and queries
│   ├── speech_recognition     # Speech recognition processing
│   └── ...
├── tests                      # Unit tests
│   ├── test_app.py            # Tests for app.py
│   └── ...
└── utils                      # Helper functions
    └── audio_processor.py     # Audio processing utilities
```

- app.py: Main Flask application and entry point.

- services: Contains all business logic, including speech recognition and database interaction.
- utils: Helper functions like audio file handling and processing.
- testt: Unit tests for the application.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Flask for the web framework.
- Whisper and yt-dlp for audio processing and YouTube video handling.
- PostgreSQL for database management.