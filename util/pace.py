import os
import numpy as np
import scipy
import io
import json
import librosa
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai.types.audio import Transcription


def wpm(file: io.BufferedReader, audio: io.BytesIO) -> dict:
    """
    Returns wpm of the audio.
    """
    transcript: Transcription = whisper.whisper_stt(file)
    words = transcript.text.split(" ")
    num_words: int = len(words) + 1
    y, sr = librosa.load(audio)
    duration = librosa.get_duration(y=y, sr=sr)
    avg_pace: float = (
        num_words / duration
    ) * 60  # Average out to num of words per minute
    return {"wpm": avg_pace}


# Given a base64 string, the string gets converted to a wav file
# if __name__ == "__main__":
#     path = (
#         os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         + "/test_assets/harvard.wav"
#     )
#     with open(path, "rb") as f:
#         wpm(file=f, audio=io.BytesIO(f.read()))
