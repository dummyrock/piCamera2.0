import detectBallCam
import takePicture
from picamera2 import Picamera2

movement_detected=False

highSpeedCam = takePicture.highSpeedCamera()
img = highSpeedCam.takePhoto()

flag = True

liveCam = detectBallCam.liveCamera()

while flag:
    img = liveCam.lookForBall()
    #print(liveCam.getShape())
    movement_detected = liveCam.check_movement()
    if movement_detected:
        print("test found movement detected")
        movement_detected=False
    #flag = False

