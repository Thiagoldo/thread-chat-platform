from app import create_app
import eventlet
import eventlet.wsgi

app, socketio = create_app()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 3003
    print(f"Starting WebSocket server on {host}:{port}")
    eventlet.wsgi.server(eventlet.listen((host, port)), app)
