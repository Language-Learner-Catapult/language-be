from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

from util.assistant import client

load_dotenv()

server = Flask(__name__)
server.config['CORS_HEADERS'] = 'Content-Type'
CORS(server, resources={r"/*": {"origins": "*"}})

# Add blueprints here
# from routes.service import service
# server.register_blueprint(service, url_prefix='/service')


@server.route("/create_thread")
def create_thread():
    thread = client.beta.threads.create()
    return thread.id


@server.route("/messages/<string:thread_id>/send")
def send_message(thread_id):
    data = request.json()
    if "message" in data:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=data["message"]
        )
        return "", 200
    else:
        return "", 405


@server.route("/messages/<string:thread_id>")
def get_messages(thread_id):
    messages = client.beta.threads.messages.list(thread_id)
    return messages


if __name__ == "__main__":
    server.run()
