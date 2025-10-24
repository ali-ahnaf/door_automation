from machine import Pin

class Motor:
    def __init__(self, in1_pin, in2_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.stop()

    def forward(self):
        """Run motor forward (unlock direction)"""
        self.in1.value(1)
        self.in2.value(0)

    def backward(self):
        """Run motor backward (lock direction)"""
        self.in1.value(0)
        self.in2.value(1)

    def stop(self):
        """Stop the motor"""
        self.in1.value(0)
        self.in2.value(0)
