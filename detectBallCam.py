import cv2
import numpy as np
import time

class liveCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Error: Could not open video capture device.")
        self.can_play_beep = True
        self.prev_ball_xy = [0,0]
        self.movement_threshold = 50
        self.ball_movement_detected = False
        
    # Function to play a beep sound
    def play_beep(self):
        """
        frequency = 1000  # Frequency of the beep in Hertz
        duration = 300    # Duration of the beep in milliseconds
        winsound.Beep(frequency, duration)
        """
        #if you have a speaker or are on windows you can play sound, I however do not have a speaker connected
        print("playing sound of ball is detected")
        
    def check_movement(self):
        return self.ball_movement_detected
    
    def ball_movement(self):
        print("ball is moving!!")
        self.ball_movement_detected = True
    
    def getShape(self,frame):

        # Get the shape of the frame

        h, w, __ = frame.shape

        return frame.shape
    
    def destroyCap(self):
        self.cap.release()


    def lookForBall(self):
        ret, frame = self.cap.read()

        h, w, __ = self.getShape(frame)
              
        cropped_h = h-h//4
        cropped_w = w-w//4
        
        cropped_img = frame[cropped_h:, cropped_w:]
        
        gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        
        blurred_image = cv2.medianBlur(gray_image, 5)
        
        circles = cv2.HoughCircles(
            blurred_image,
            cv2.HOUGH_GRADIENT,
            dp=1.2,  # Inverse ratio of resolution
            minDist=30,  # Minimum distance between detected centers
            param1=350,  # Upper threshold for the Canny edge detector
            param2=20,  # Accumulator threshold for circle detection
            minRadius=5,  # Minimum radius of detected circles
            maxRadius=50,  # Maximum radius of detected circles
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))  # Convert circle parameters to integers
            for (x, y, r) in circles[0, :]:
                # Draw the circle
                cv2.circle(frame, (x + cropped_w, y + cropped_h), r, (0, 255, 0), 2)
                # Draw the center
                cv2.circle(frame, (x+cropped_w, y+cropped_h), 5, (0, 0, 255), -1)
                # Add text
                cv2.putText(frame, "Golf Ball", ((x + cropped_w)- 40, (y + cropped_h) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                x_rounded = int(x) - int(self.prev_ball_xy[0])
                y_rounded = int(y) - int(self.prev_ball_xy[1])
                
                if self.prev_ball_xy != [0,0]:
                    if abs(x_rounded) > self.movement_threshold or abs(y_rounded) > self.movement_threshold:
                        self.ball_movement()
                    else:
                        self.ball_movement_detected = False
                
                self.prev_ball_xy = [x,y]
                
                if self.can_play_beep:
                    self.play_beep()
                    self.can_play_beep = False
                    
        else:
            if self.prev_ball_xy != [0,0]:
                print("Ball missing, possible fast movement!")
                self.ball_movement()
                self.prev_ball_xy = [0,0]
                self.can_play_beep = True
            else:
                self.ball_movement_detected = False
       
        __, img_encoded = cv2.imencode('.jpeg', frame)
        data = img_encoded.tobytes()
        return data
        
