from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin, freq=50, min_duty=1638, max_duty=8192):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.min_duty = min_duty
        self.max_duty = max_duty

    def set_angle(self, angle):
        duty = int(self.min_duty + (self.max_duty - self.min_duty) * angle / 180)
        self.pwm.duty_u16(duty)

    def move(self, angle, delay=0):
        self.set_angle(angle)
        if delay:
            time.sleep(delay)