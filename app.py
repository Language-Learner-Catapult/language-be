import base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import sys
from util.utils import webm_to_wav
from util.decibel import *
from util.assistant import *
from util.pace import *
load_dotenv()

# from util.sentiment import *

server = Flask(__name__)
server.config["CORS_HEADERS"] = "Content-Type"
CORS(server, resources={r"/*": {"origins": "*"}})
client = OpenAI()


def cors_response(object):
    response = jsonify(object)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@server.route("/")
def index():
    return "Hello, World!"


@server.route("/create_thread", methods=["POST"])
def create_thread():
    # Create a new thread and run it for intial message
    data = request.json
    thread_id, response = init_and_run_thread(data)
    print("CALLED /create_thread, created thread: ", thread_id)

    # Get tts audio and encode
    encoded_response = str(base64.b64encode(whisper_tts(response)), encoding="utf-8")

    return cors_response({"thread_id": thread_id, "audio": encoded_response}), 200


@server.route("/messages/<string:thread_id>/send", methods=["POST"])
def send_message(thread_id):
    data = request.json
    if "audio" in data:
        # Get stats (just wpm right now)
        raw = base64.b64decode(data["audio"].split(",")[1])
        out = io.BytesIO(raw)
        out.name = "input.webm"
        wav = webm_to_wav(raw)

        message = whisper_stt(client, audio_file=wav)
        pace = wpm(message, audio=wav)
        print(pace, file=sys.stderr)
        # decibel = decibelAnalysis(audio=wav)
        # print(decibel, file=sys.stderr)
        # contrast = contrast(audio=wav)
        # print(contrast)
        print(f"WPM: {pace}", file=sys.stderr)

        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message
        )
        # sentiment_score, sentiment_magnitude = analyzeSentiment(message)
        # print(sentiment_score, sentiment_magnitude)
        # response = run_assistant(thread_id)
        # encoded_response = str(
        #     base64.b64encode(whisper_tts(client, response)), encoding="utf-8"
        # )

        # Run the model with on the thread and get response
        response = run_assistant(thread_id)

        # Get fluency score
        current_fluency_score = data["proficiency"]
        # fluency_score = get_fluency_score(message, pace, proficiency) * 0.2 + proficiency * 0.8
        fluency_score = fluency({"buffer":wav}, current_fluency_score, 1, "english", data["language"]) * 0.5 + current_fluency_score * 0.5


        encoded_response = str(base64.b64encode(whisper_tts(response)), encoding="utf-8")

        return cors_response({
            "response": response,
            "fluency": fluency_score,
            "audio": encoded_response,
            "pace": pace
        }), 200
    else:
        return "no message provided", 405


@server.route("/messages/<string:thread_id>")
def get_messages(thread_id):
    thread = client.beta.threads.messages.list(thread_id)
    messages = [
        {"role": message.role, "content": message.content[0].text.value} for message in thread.data
    ]


    return cors_response(messages), 200


if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=5001)
