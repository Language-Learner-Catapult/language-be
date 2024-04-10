import base64
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import io
import sys
import filetype
import openai
import assemblyai as aai
from util.utils import webm_to_wav

load_dotenv()

from util.assistant import *
from util.pace import wpm
from util.contrast import contrast
from util.decibel import *
from util.sentiment import *

server = Flask(__name__)
server.config["CORS_HEADERS"] = "Content-Type"
CORS(server, resources={r"/*": {"origins": "*"}})
openai = OpenAI()

# Add blueprints here
# from routes.service import service
# server.register_blueprint(service, url_prefix='/service')


@server.route("/")
def index():
    return "Hello, World!"


@server.route("/create_thread", methods=["POST"])
def create_thread():
    thread = client.beta.threads.create()

    data = request.json
    response, fluency = run_assistant(thread.id, data["name"], data["language"], 0)
    encoded_response = str(
        base64.b64encode(whisper_tts(client, response)), encoding="utf-8"
    )

    return {"thread_id": thread.id, "audio": encoded_response}, 200


@server.route("/messages/<string:thread_id>/send", methods=["POST"])
def send_message(thread_id):
    data = request.json
    if "audio" in data:
        raw = base64.b64decode(data["audio"].split(",")[1])
        wav = webm_to_wav(raw)

        message = whisper_stt(client, audio_file=wav)
        pace = wpm(message, audio=wav)
        print(pace)
        decibel = decibelAnalysis(audio=wav)
        print(decibel)
        contrast = contrast(audio=wav)
        print(contrast)

        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message
        )
        sentiment_score, sentiment_magnitude = analyzeSentiment(message)
        print(sentiment_score, sentiment_magnitude)
        response, fluency = run_assistant(thread_id, data["name"], data["language"], 30)
        encoded_response = str(
            base64.b64encode(whisper_tts(client, response)), encoding="utf-8"
        )

        return {
            "response": response,
            "fluency": fluency,
            "audio": encoded_response,
        }, 200
    else:
        return "no message provided", 405


@server.route("/messages/<string:thread_id>")
def get_messages(thread_id):
    thread = client.beta.threads.messages.list(thread_id)
    messages = [
        {"role": message.role, "content": message.content[0].text.value}
        for message in thread.data
    ]
    return messages, 200


if __name__ == "__main__":
    server.run(debug=True)
