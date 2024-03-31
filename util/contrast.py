import io
import os
from dotenv import load_dotenv
import librosa

from utils import webm_to_wav


def contrast(audio: io.BytesIO) -> dict:
    """
    Measure the contrast of a speaker's voice;
    the higher the contrast, the more dynamic the speech is and the more likely
    it is to be engaging.
    Returns the stddev of contrast for the user's speech.
    """

    y, sr = librosa.load(audio)
    audio.seek(0)
    contrast_values = librosa.feature.spectral_contrast(y=y, sr=sr)

    contrast = contrast_values.std()
    return {"contrast": contrast}


if __name__ == "__main__":
    load_dotenv("../.env")
    path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/test.webm"
    )
    with open(path, "rb") as f:
        contrast(audio=webm_to_wav(f.read()))
