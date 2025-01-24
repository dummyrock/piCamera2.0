import uuid
import cv2
import detectBallCam
import takePicture
import flickerLights



movement_detected = False

liveCam = detectBallCam.liveCamera()
highSpeedCam = takePicture.highSpeedCamera()
strobeLight = flickerLights.flickerLights()

while True:
    
    img = liveCam.lookForBall()
    movement_detected = liveCam.check_movement()
    
    if movement_detected:
        strobeLight.turnOnStrobe()
        uid = str(uuid.uuid4().hex) 
        for i in range(5):
            img = highSpeedCam.takePhoto()
            highSpeedCam.savePhoto(img,uid + f"{i}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
