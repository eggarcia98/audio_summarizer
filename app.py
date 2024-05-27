from flask import Flask, request, jsonify
from services.audio_service import process_audio_file
from utils.text_processing_utils import recognize_speech
from lib.ntlp import segment_text
import asyncio


app = Flask(__name__)



@app.route('/process', methods=['POST'])
def process_audio_file_endpoint():
    print("HERE")
    # Call audio processing function
    file = request.data
    print("HERE2")


     # Define the path and name for the output file
    output_file_path = 'output.mp3'
    with open(output_file_path, 'wb') as output_file:
        output_file.write(file)

    print("HERE3")

    output_file_path = process_audio_file(output_file_path)

    transcript = asyncio.run(recognize_speech(output_file_path))
    print("HERE 5")
    # time_stamps = segment_text(transcript)


    return transcript

    # return jsonify({'time_stamps': time_stamps})

@app.route('/')
def process_home():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, port=6030)