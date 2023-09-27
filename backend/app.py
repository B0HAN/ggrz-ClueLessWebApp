print("Starting app.py")
from flask import Flask

def create_app():
    print("Inside create_app function")
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
print("Finished app.py")
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(message):
    print('Received message:', message)
    emit('broadcast_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
