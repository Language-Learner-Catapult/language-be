import os
import numpy as np
import scipy
import io
import json
import librosa
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai.types.audio import Transcription

# load_dotenv()
# import assistant as whisper

# Faster speech - faster pitch fluctuations
# Spectral feature analysis
# def pace(audio: bytes) -> int:
#     """
#     Returns pace metrics about the audio.
#     This includes:
#     - Average pace throughout the audio file
#     - Lists any abnormalities in pace
#     """
#     # 20hz to 20000hz

#     # Load audio into time series and sampling rate
#     ts, sr = librosa.load(audio)

#     # Calculate the contrast for each unit of time in the audio
#     sc = librosa.feature.spectral_contrast(y=ts, sr=sr)

#     # Find the peaks in the spectral contrast
#     peaks, _ = scipy.signal.find_peaks(sc[0])

#     # Calculate the average spectral contrast
#     pace = np.diff(peaks).mean()

#     # Calculate the standard deviation
#     std_dev = np.diff(peaks).std()

#     # Find any abnormalities (more than 2 standard deviations from the mean)
#     abnormalities = np.where(np.diff(peaks) > pace + 2 * std_dev)[0]

#     # Get the timestamps of the abnormalities
#     abnormalities = librosa.frames_to_time(abnormalities, sr=sr)

#     print(pace)
#     print(abnormalities)

#     # Plot the spectral contrast graph
#     plt.figure()
#     plt.plot(sc[0])
#     plt.title("Spectral Contrast")
#     plt.xlabel("Time")
#     plt.ylabel("Contrast")
#     plt.show()

#     return pace, abnormalities


# Given a base64 string
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
