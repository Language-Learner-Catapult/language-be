# Beat tracking example
import librosa
import numpy as np
import base64
import io
# import librosa.display
# import matplotlib.pyplot as plt 

# 1. Get the file path to an included audio example
base64_audio_string = ""
with open("encoded-20240330185923.txt", "r") as file:
    base64_audio_string = file.read()
audio_bytes = base64.b64decode(base64_audio_string)
def decibelAnalysis(file):
    # filename = librosa.example('nutcracker')
    # print(filename)
    y, sr = librosa.load(file, sr=None)
    D = librosa.stft(y)
    D_db = librosa.amplitude_to_db(D, top_db=None, ref = np.min)
    print("average decibels: ", np.nanmean(D_db))
    print("max decibels: ", np.nanmax(D_db))
    return (np.nanmean(D_db), np.nanmax(D_db))
decibelAnalysis(io.BytesIO(audio_bytes))   