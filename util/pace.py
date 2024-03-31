import os
import numpy as np
import scipy
import io
import json
import librosa
import matplotlib.pyplot as plt
import soundfile as sf
from dotenv import load_dotenv
from openai.types.audio import Transcription
from util.utils import webm_to_wav, bytes_to_str
from util.assistant import *
import soundfile as sf


def wpm(transcript: str, audio: io.BytesIO):
    """
    Returns wpm of the audio.
    """
    words = transcript.split(" ")
    num_words: int = len(words) + 1
    audio.seek(0)
    y, sr = sf.read(audio)
    audio.seek(0)
    duration = librosa.get_duration(y=y, sr=sr)
    avg_pace: float = (
        num_words / duration
    ) * 60  # Average out to num of words per minute
    return avg_pace


# Given a base64 string, the string gets converted to a wav file
if __name__ == "__main__":
    load_dotenv()
    from assistant import *

    path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/test.webm"
    )
    with open(path, "rb") as f:
        # output: io.BytesIO = io.BytesIO(f.read())
        # output.name = "file.webm"
        print(wpm("This is my transcript", audio=webm_to_wav(f.read())))
