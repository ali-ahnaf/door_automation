from machine import Pin
import time

class Motor:
    def __init__(self, in1_pin, in2_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.stop()

    def forward(self, duration):
        """Run motor forward (unlock direction)"""
        self.in1.value(1)
        self.in2.value(0)
        time.sleep(duration)
        self.stop()

    def backward(self, duration):
        """Run motor backward (lock direction)"""
        self.in1.value(0)
        self.in2.value(1)
        time.sleep(duration)
        self.stop()

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
