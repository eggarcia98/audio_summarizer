from pydub import AudioSegment

def process_audio_file(output_audio_path):
    output_wav_audio_path = f"{output_audio_path}.wav"

    audio_no_wav = AudioSegment.from_file(output_audio_path)
    audio_no_wav.export(output_wav_audio_path, format="wav")

    return output_wav_audio_path