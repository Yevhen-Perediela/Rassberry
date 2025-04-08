from flask import Flask, request, jsonify, Response, send_from_directory
# from motor import Ordinary_Car
from picamera2 import Picamera2
import cv2
import os

app = Flask(__name__)

# --- Inicjalizacja kamery ---
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"
picam2.configure("preview")
picam2.start()

# --- Inicjalizacja samochodu ---
car = ''

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')

    if direction == "forward":
        car.set_motor_model(1000, 1000, 1000, 1000)
    elif direction == "backward":
        car.set_motor_model(-1000, -1000, -1000, -1000)
    elif direction == "left":
        car.set_motor_model(-1500, -1500, 1500, 1500)
    elif direction == "right":
        car.set_motor_model(1500, 1500, -1500, -1500)
    elif direction == "stop":
        car.set_motor_model(0, 0, 0, 0)
    else:
        return jsonify({"error": "Invalid direction"}), 400

    return jsonify({"status": "ok", "direction": direction})

@app.route('/video_feed')
def video_feed():
    def gen_frames():
        while True:
            frame = picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return """
    <h1>Samochodzik z API</h1>
    <p>Użyj POST /move z JSON body: {"direction": "forward"}</p>
    <p><a href="/video_feed">Podgląd kamery</a></p>
    """


@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('static', path)
# --- Uruchom serwer ---
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        car.set_motor_model(0, 0, 0, 0)
