from app import create_app, SocketIO

app = create_app()

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app, debug=True) # type: ignore
