from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit

# Constants
MAX_PLAYERS_PER_LOBBY = 6
MIN_PLAYERS_PER_LOBBY = 3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, manage_session=False)

    # In-memory databases
    users_db = {}  # {username: password}
    lobbies = {}   # {lobby_id: [list_of_players]}

    # -----------------
    # Web Routes
    # -----------------

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db:
            return 'Username already taken!', 400
        users_db[username] = password
        return 'User registered successfully!'

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')
        if users_db.get(username) == password:
            session['username'] = username
            return 'Login successful!'
        return 'Invalid username or password!', 401

    @app.route('/create_lobby', methods=['POST'])
    def create_lobby():
        lobby_id = len(lobbies) + 1
        lobbies[lobby_id] = [session['username']]
        socketio.emit('lobby_update', lobbies)
        return jsonify({"lobby_id": lobby_id, "players": lobbies[lobby_id]})

    @app.route('/join_lobby/<int:lobby_id>', methods=['POST'])
    def join_lobby(lobby_id):
        if lobby_id not in lobbies:
            return "Lobby not found!", 404

        if len(lobbies[lobby_id]) >= MAX_PLAYERS_PER_LOBBY:
            return "Lobby is full!", 403

        if session['username'] not in lobbies[lobby_id]:
            lobbies[lobby_id].append(session['username'])
            socketio.emit('lobby_update', lobbies) 

        return jsonify({"lobby_id": lobby_id, "players": lobbies[lobby_id]})

    @app.route('/lobbies', methods=['GET'])
    def get_lobbies():
        return jsonify(lobbies)

    # -----------------
    # Socket Events
    # -----------------

    @socketio.on('send_message')
    def handle_message(data):
        username = data.get('username', 'Anonymous')
        message = data['message']
        formatted_message = f"{username}: {message}"
        emit('broadcast_message', formatted_message, broadcast=True)

    return app

app = create_app()

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app, debug=True) # type: ignore
