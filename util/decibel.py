# Beat tracking example
import librosa
import librosa.display

# 1. Get the file path to an included audio example


def decibelAnalysis():
    filename = librosa.example('nutcracker')
    # 2. Load the audio as a waveform `y`
    #    Store the sampling rate as `sr`
    y, sr = librosa.load(filename)
    # 3. Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    D = librosa.stft(y)
    D_db = librosa.amplitude_to_db(abs(D))

    librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
    # 4. Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)


decibelAnalysis()
