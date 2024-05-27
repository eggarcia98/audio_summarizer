# segment_text.py
import nltk
# from utils.text_processing_utils import extract_audio_segment_times

def segment_text(transcript):
    # Tokenize the transcript into sentences using NLTK
    nltk.download('punkt')
    sentences = nltk.sent_tokenize(transcript)
    print("SEN: ", sentences)

    # Calculate time stamps for each sentence based on audio/video file timestamp information
    time_stamps = []
    current_timestamp = 0
    for sentence in sentences:
        print("SEN: ", sentence)
        # Use a library like pydub to get the start and end times of the sentence's corresponding audio segment
        # start_time, end_time = extract_audio_segment_times(file_path, current_timestamp)
        # time_stamps.append({'text': sentence, 'start_time': start_time, 'end_time': end_time})
        # current_timestamp += (end_time - start_time)

    return time_stamps