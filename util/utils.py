import io
import os
from pyffmpeg import FFmpeg
from util.constants import ff
import soundfile as sf


def webm_to_wav(raw: bytes) -> io.BytesIO:
    # Convert webm to wav
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(base_path + "/file.webm", "wb") as f:
        f.write(raw)
        # ff.options(
        #     "-i "
        #     + base_path
        #     + "/file.webm"
        #     + " -vn -acodec copy "
        #     + base_path
        #     + "/file.wav"
        # )
    commands = [
        "-i",
        base_path + "/file.webm",
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        base_path + "/file.wav",
    ]
    ff.options(commands)
    # output_file = ff.convert(base_path + "/file.webm", base_path + "/file.wav")
    os.remove(base_path + "/file.webm")
    output = None
    with open(base_path + "/file.wav", "rb") as f:
        output = io.BytesIO(f.read())
        output.name = "file.wav"
    # os.remove(base_path + "/file.wav")
    return output


def bytes_to_str(b: io.BytesIO) -> io.StringIO:
    # assume bytes_io is a `BytesIO` object
    byte_str = b.read()

    # Convert to a "unicode" object
    text_obj = byte_str.decode("UTF-8")  # Or use the encoding you expect

    # Use text_obj how you see fit!
    return io.StringIO(text_obj)
