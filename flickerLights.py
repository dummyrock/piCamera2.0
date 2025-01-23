from smbus import SMBus
import time

class flickerLights:
    def __init__(self):
        self.addr = 0x8
        self.bus = SMBus(1)

    def turnOnStrobe(self):
        self.bus.write_byte(self.addr,0x1)
