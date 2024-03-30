from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

server = Flask(__name__)
socketio = SocketIO(server, cors_allowed_origins='*')
server.config['CORS_HEADERS'] = 'Content-Type'
CORS(server, resources={r"/*": {"origins": "*"}})

# Add blueprints here
# from routes.service import service
# server.register_blueprint(service, url_prefix='/service')

if __name__ == "__main__":
    server.run()
