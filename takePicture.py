from picamera2 import Picamera2
import time
import io
import uuid

class highSpeedCamera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.picam2.set_controls({"ExposureTime":2000, "AnalogueGain": 8.0, "Brightness": 0.2})
        self.picam2.start()
        time.sleep(2)
        
    def takePhoto(self):
        data = io.BytesIO()
        self.picam2.capture_file(data,format="jpeg")
        
        return data.getvalue()
    
    def savePhoto(self,data,uid): 
        output_file = f"images/photo_{uid}.jpg"
        with open(output_file,"wb") as f:
            f.write(data)
