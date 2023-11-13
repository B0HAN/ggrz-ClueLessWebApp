from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from game import Game
from gameboard import Gameboard
from deck_control import Deck, Card

# Constants
MAX_PLAYERS_PER_LOBBY = 6
MIN_PLAYERS_PER_LOBBY = 3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, manage_session=False)

    # In-memory databases
    users_db = {}  # {username: password}
    players_in_lobby = []


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

    @app.route('/join', methods=['POST'])
    def join():
        if session['username'] not in players_in_lobby:
            if len(players_in_lobby) < MAX_PLAYERS_PER_LOBBY:
                players_in_lobby.append(session['username'])
                socketio.emit('players_update', players_in_lobby)
                return jsonify({"players": players_in_lobby})
            return "Lobby is full!", 403
        return "Already in the lobby!", 400

    @app.route('/get_players', methods=['GET'])
    def get_players():
        return jsonify({"players": players_in_lobby})
    
    @app.route('/start_game', methods=['POST'])
    def handle_start_game():
        # Ensure the user is logged in
        if 'username' not in session:
            return jsonify({"error": "User not logged in"}), 401

        # Check if the user trying to start the game is the first player in the lobby
        if players_in_lobby[0] != session['username']:
            return jsonify({"error": "You're not the first player in this lobby. Only the first player can start the game."}), 403

        # Check for minimum number of players before starting the game
        if len(players_in_lobby) < MIN_PLAYERS_PER_LOBBY:
            return jsonify({"error": f"At least {MIN_PLAYERS_PER_LOBBY} players are required to start the game."}), 403

        # If all checks passed, broadcast that the game has started
        emit('game_started', namespace='/', broadcast=True)
        #start game
        global curr_game
        curr_game = Game(players_in_lobby)
        #logs
        initial_game_state = curr_game.get_game_status()
        solution = curr_game.solution
        print("Initial Game State:\n ")
        print(initial_game_state)
        print("Solution: ")
        print(solution)
        return jsonify({"status": "Game started for lobby"})
    
    # -----------------
    # Socket Events
    # -----------------
    @socketio.on('move_player')
    def valid_move(move_data):
        username = move_data['username']
        destination = move_data['destination']
        player = curr_game.current_player()
        #print("Player: " + player.__str__() + "\n Destination: " + destination)
        if(player.__str__() == username):
            message = curr_game.move_player(player, destination)
            if "is not a valid" in message or 'You are' in message:
                emit('broadcast_message', message, broadcast=False)
            else:
                emit('broadcast_message', message, broadcast=True)
        else:
            emit('broadcast_message', 'IVALID MOVE: It is not your turn.', broadcast=False)

    @socketio.on('end_turn')
    def endTurn(user_data):
        username = user_data['username']
        player = curr_game.current_player()
        if(player.__str__() == username):
            curr_game.next_turn()
            new_player = curr_game.current_player()
            message = player.name + " has ended their turn\n It is now " + new_player.name + " turn.\n"
            emit('broadcast_message', message, broadcast=True)
        else:
            emit('broadcast_message', 'IVALID MOVE: It is not your turn.', broadcast=False)
        game_state = curr_game.get_game_status()
        print(" ========= CURRENT GAME STATE: \n")
        print(game_state)

    @socketio.on('make_suggestion')
    def makeSuggestion(suggestion_data):
        username = suggestion_data['username']
        suspect = suggestion_data['suspect']
        location = suggestion_data['location']
        weapon = suggestion_data['weapon']
        player = curr_game.current_player()
        if(player.__str__() == username):
            # These events need to happen sepeerately in the future, since after a suggestion is made
            # players will then choose to show a card through UI
            message = curr_game.player_makes_suggestion(player, suspect, weapon)
            fail = "You can only make a suggestion when you are in a room."
            if message != fail:
                emit('broadcast_message', suspect + " has been moved to " + location, broadcast=True)
            #This needs to be a separate event
            emit('broadcast_message', message, broadcast=False)
            colon_index = message.find(':')
            if colon_index != -1:
                # Remove characters after the colon
                global_message = message[:colon_index]
            emit('broadcast_message', global_message, broadcast=True, include_self=False)

        else:
            emit('broadcast_message', 'IVALID MOVE: It is not your turn.', broadcast=False)
        game_state = curr_game.get_game_status()
        print(" ========= CURRENT GAME STATE: \n")
        print(game_state)

    @socketio.on('make_accusation')
    def makeAccusation(accusation_data):
        username = accusation_data['username']
        suspect = accusation_data['suspect']
        location = accusation_data['location']
        weapon = accusation_data['weapon']
        player = curr_game.current_player()
        if(player.__str__() == username):
            # These events need to happen sepeerately in the future, since after a suggestion is made
            # players will then choose to show a card through UI
            message = curr_game.player_makes_accusation(player, suspect, weapon, location)
            emit('broadcast_message', username + " has made an accusation: ", broadcast=True)
            emit('broadcast_message', suspect +" in the " + location +  " with a " + weapon + "!", broadcast=True)
            #This needs to be a separate event

            emit('broadcast_message', message, broadcast=True)
        else:
            emit('broadcast_message', 'IVALID MOVE: It is not your turn.', broadcast=False)
        game_state = curr_game.get_game_status()
        print(" ========= CURRENT GAME STATE: \n")
        print(game_state)
        if curr_game.game_over == True:
            emit('broadcast_message', 'GAME OVER', broadcast=True)


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
