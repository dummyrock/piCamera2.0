import time
from flask import Flask, render_template, Presponse
import io
import detectBallCam
import takePicture

app = Flask(__name__)

def liveCamera():
    global movement_detected
    liveCam = detectBallCam.liveCamera()
    while True:
        img = liveCam.lookForBall()
        movement_detected = liveCam.checkMovement()
        if movement_detected:
            print("server found movement detected")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
        
def highSpeedPhoto():
    highSpeedCam = takePicture.highSpeedCamera()
    if movement_detected:
        img = highSpeedCam.takePhoto()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
    

@app.route('/')
def index():
    return render_template("golfServer.html")

@app.route('liveCamera')
def liveCamera():
    return Response(liveCamera,mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('highSpeedPhoto')
def highSpeedPhoto():
    return Response(highSpeedPhoto,mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(host="0.0.0.0", port = 5000)