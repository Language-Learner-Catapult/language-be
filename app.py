import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os

load_dotenv()

from util.assistant import client

server = Flask(__name__)
socketio = SocketIO(server, cors_allowed_origins="*")
server.config["CORS_HEADERS"] = "Content-Type"
CORS(server, resources={r"/*": {"origins": "*"}})

# Add blueprints here
# from routes.service import service
# server.register_blueprint(service, url_prefix='/service')


@server.route("/create_thread")
def create_thread():
    thread = client.beta.threads.create()
    return thread.id


@server.route("/messages/<string:thread_id>/send", methods=["POST"])
def send_message(thread_id):
    data = request.json
    if "message" in data:
        raw = base64.b64decode(message[data])
        out = io.StringIO(raw)

        out = preprocess(out)

        message = whisper_stt(out)

        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=data["message"]
        )
        return "message sent", 200
    else:
        return "no message provided", 405


@server.route("/messages/<string:thread_id>")
def get_messages(thread_id):
    thread = client.beta.threads.messages.list(thread_id)
    print(thread, file=sys.stderr)
    messages = [
        {"role": message.role, "content": message.content[0].text.value}
        for message in thread.data
    ]
    return messages, 200


if __name__ == "__main__":
    server.run(debug=True)
