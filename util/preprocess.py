import base64
import io
import os
import librosa
import librosa.effects as effects
import numpy as np
import soundfile as sf

from constants import SILENCE
import base64
import io
import noisereduce as nr
from dotenv import load_dotenv
from utils import webm_to_wav


def preprocess(
    audio: io.BytesIO,
    remove_bg: bool = True,
    strip_silence: bool = True,
) -> io.BytesIO:
    """
    Preprocesses the audio uses FFmpeg
    - Strips silence from the beginning and end of the recording
    - Removes background noise
    """
    # Load the audio
    print(type(audio))
    print(audio.name)
    y, sr = librosa.load(audio)

    # Remove background noise
    if remove_bg:
        y = nr.reduce_noise(y=y, sr=sr)

        # Normalize the audio
        y = librosa.util.normalize(y)

    if strip_silence:
        # Remove silence from beginning and end of audio
        y, _ = librosa.effects.trim(y, top_db=SILENCE)

    # Save trimmed audio
    output = io.BytesIO()
    # sf.write(file=output, data=y, samplerate=sr, format="wav")
    sf.write(
        file=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/no_bg.wav",
        data=y,
        samplerate=sr,
        format="wav",
    )
    with open(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/no_bg.wav",
        "rb",
    ) as f:
        output.write(f.read())
    os.remove(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/no_bg.wav"
    )
    return output


if __name__ == "__main__":
    load_dotenv()
    path = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "/test_assets/test.webm"
    )
    with open(path, "rb") as f:
        # Encode the file contents as base64 string
        # base64_str = base64.encodebytes(f.read()).decode("utf-8")
        # # Create a StringIO byte buffer from the base64 string
        # audio = io.BytesIO(base64.b64decode(base64_str))

        # Call the preprocess function with the audio
        # output: io.BytesIO = io.BytesIO(f.read())
        # output.name = "file.webm"
        preprocess(audio=webm_to_wav(f.read()))
