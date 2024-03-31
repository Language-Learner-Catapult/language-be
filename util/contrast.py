import io
import os
import librosa


def contrast(file: io.BufferedReader, audio: io.BytesIO) -> dict:
    """
    Measure the contrast of a speaker's voice;
    the higher the contrast, the more dynamic the speech is and the more likely
    it is to be engaging.
    Returns the stddev of contrast for the user's speech.
    """

    y, sr = librosa.load(audio)
    contrast_values = librosa.feature.spectral_contrast(y=y, sr=sr)

    contrast = contrast_values.std()
    return {"contrast": contrast}


if __name__ == "__main__":
    path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/harvard.wav"
    )
    with open(path, "rb") as f:
        contrast(file=f, audio=io.BytesIO(f.read()))
