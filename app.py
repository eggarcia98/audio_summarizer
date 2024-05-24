from flask import Flask, request, jsonify
from services.audio_service import process_audio_file
from utils.text_processing_utils import recognize_speech
from lib.ntlp import segment_text

app = Flask(__name__)



@app.route('/process', methods=['POST'])
def process_audio_file_endpoint():

    # Call audio processing function
    file = request.data

     # Define the path and name for the output file
    output_file_path = 'output.mp3'
    with open(output_file_path, 'wb') as output_file:
        output_file.write(file)

    output_file_path = process_audio_file(output_file_path)
    transcript = recognize_speech(output_file_path)
    time_stamps = segment_text(transcript)

    print(transcript)
   

    return "Done!"

    # return jsonify({'time_stamps': time_stamps})


if __name__ == '__main__':
    app.run(debug=True, port=6030)