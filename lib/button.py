from machine import Pin
import utime

class Button:
    def __init__(self, pin, pull_up=True):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP if pull_up else None)
        self.last_state = self.pin.value()
        self.last_press_time = 0
        self.debounce_time = 50  # milliseconds
        
    def is_pressed(self):
        current_state = self.pin.value()
        current_time = utime.ticks_ms()
        
        # Debounce logic
        if current_state != self.last_state:
            if utime.ticks_diff(current_time, self.last_press_time) > self.debounce_time:
                self.last_state = current_state
                self.last_press_time = current_time
                return not current_state  # Return True when button is pressed (LOW)
        
        return False
    
    def is_held(self):
        return not self.pin.value()  # Button pressed when pin is LOW
