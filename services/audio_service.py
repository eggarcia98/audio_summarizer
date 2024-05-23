# process_audio_file.py
import librosa
import numpy as np


# get the current working directory


from pydub import AudioSegment

# Extract audio track from video (if applicable)
def process_audio_file(file_path):
    output_file = f"{file_path}.wav"

    audio_no_wav = AudioSegment.from_file(file_path)
    audio_no_wav.export(output_file, format="wav")

    audio_wav, sr = librosa.load(output_file, sr=44100)
    audio_spect = librosa.feature.melspectrogram(y=audio_wav, sr=sr)

    # Convert to log scale (dB). We'll use the peak power as reference.
    log_s = librosa.amplitude_to_db(S=audio_spect, ref=np.max )
    features = librosa.feature.mfcc(S=log_s, n_mfcc=13)

    return features
