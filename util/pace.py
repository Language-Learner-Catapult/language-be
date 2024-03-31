import os
import numpy as np
import scipy
import io
import json
import librosa
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai.types.audio import Transcription
from utils import webm_to_wav


def wpm(audio: io.BytesIO) -> dict:
    """
    Returns wpm of the audio.
    """
    transcript: Transcription = whisper_stt(audio)
    words = transcript.text.split(" ")
    num_words: int = len(words) + 1
    y, sr = librosa.load(audio)
    duration = librosa.get_duration(y=y, sr=sr)
    avg_pace: float = (
        num_words / duration
    ) * 60  # Average out to num of words per minute
    return {"wpm": avg_pace}


# Given a base64 string, the string gets converted to a wav file
if __name__ == "__main__":
    load_dotenv()
    from assistant import *

    path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/test.webm"
    )
    with open(path, "rb") as f:
        wpm(audio=webm_to_wav(f.read()))
