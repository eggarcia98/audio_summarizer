import speech_recognition as sr

async def transcribe_audio(recognizer, audio):
    """Transcribe a chunk of audio using Google Web Speech API."""
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return f"API request error: {e}"