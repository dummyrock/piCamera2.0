import time
from flask import Flask, render_template, Response
import io
import detectBallCam
import takePicture

app = Flask(__name__)

movement_detected = False

def liveCam():
    global movement_detected
    liveCam = detectBallCam.liveCamera() 
    while True:
        img = liveCam.lookForBall()
        movement_detected = liveCam.check_movement()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

def highSpeedCam():
    global movement_detected
    highSpeedCam = takePicture.highSpeedCamera()
    print("im trying to run")
    while True:
        if movement_detected:
            movement_detected = False
            img = highSpeedCam.takePhoto()
            print("taking photo now")
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
       
@app.route('/')
def index():
    return render_template("golfServer.html")

@app.route('/liveCamera')
def liveCamera():
    return Response(liveCam(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/highSpeedPhoto')
def highSpeedPhoto():
    return Response(highSpeedCam(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
    app.run(host="0.0.0.0", port = 5000)
