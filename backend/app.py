from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room

MAX_PLAYERS_PER_LOBBY = 6
MIN_PLAYERS_PER_LOBBY = 3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    users_db = {}  # This will store user data as {username: password}
    lobbies = {}  # This will store lobbies with structure {lobby_id: [list_of_players]}

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db:
            return 'Username already taken!', 400
        else:
            users_db[username] = password
            return 'User registered successfully!'

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')
        if users_db.get(username) == password:
            session['username'] = username  # Save username in the session
            return 'Login successful!'
        else:
            return 'Invalid username or password!', 401

    @socketio.on('send_message')
    def handle_message(message):
        print('Received message:', message)
        emit('broadcast_message', message, broadcast=True)

    @app.route('/create_lobby', methods=['POST'])
    def create_lobby():
        lobby_id = len(lobbies) + 1
        lobbies[lobby_id] = [session['username']]
        print("Emitting lobby_update from create_lobby")
        socketio.emit('lobby_update', lobbies)
        return jsonify({"lobby_id": lobby_id, "players": lobbies[lobby_id]})

    @app.route('/join_lobby/<int:lobby_id>', methods=['POST'])
    def join_lobby(lobby_id):
        if lobby_id not in lobbies:
            return "Lobby not found!", 404

        # Check if the lobby is full
        if len(lobbies[lobby_id]) >= MAX_PLAYERS_PER_LOBBY:
            return "Lobby is full!", 403

        if session['username'] not in lobbies[lobby_id]:
            lobbies[lobby_id].append(session['username'])
            print("Emitting lobby_update from join_lobby")
            socketio.emit('lobby_update', lobbies) 
        return jsonify({"lobby_id": lobby_id, "players": lobbies[lobby_id]})


    @app.route('/lobbies', methods=['GET'])
    def get_lobbies():
        return jsonify(lobbies)

    return app

app = create_app()

if __name__ == '__main__':
    from flask_socketio import SocketIO
    socketio = SocketIO(app)
    socketio.run(app, debug=True)  # type: ignore
