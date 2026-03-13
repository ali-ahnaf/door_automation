from machine import Pin
import time

class Buzzer:
    def __init__(self, pin_num=28):
        self.buzzer = Pin(pin_num, Pin.OUT)
        self.buzzer.value(0)

    def beep(self, duration=0.05):
        self.buzzer.value(1)
        time.sleep(duration)
        self.buzzer.value(0)

    def success_alarm(self):
        # A quick triple beep
        for _ in range(3):
            self.beep(0.1)
            time.sleep(0.05)
            
    def reset(self):
        self.buzzer.value(0)

    def wrong_pin_alarm(self):
        # Long-short-long pattern
        self.beep(0.2)
        time.sleep(0.1)
        self.beep(0.05)
        time.sleep(0.1)
        self.beep(0.2)
