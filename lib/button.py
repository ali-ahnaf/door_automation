from machine import Pin
import time

class Button:
    def __init__(self, pin_num, pull=Pin.PULL_UP, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, pull)
        self.debounce_ms = debounce_ms
        
        self._last_state = self.pin.value()
        self._last_time = time.ticks_ms()
        
        self._pressed = False
        self._released = False

    def update(self):
        current_state = self.pin.value()
        current_time = time.ticks_ms()

        # Debounce check
        if current_state != self._last_state:
            if time.ticks_diff(current_time, self._last_time) > self.debounce_ms:
                self._last_time = current_time
                
                if current_state == 0:  # pressed (for PULL_UP)
                    self._pressed = True
                else:                  # released
                    self._released = True
                
                self._last_state = current_state

    def is_pressed(self):
        return self.pin.value() == 0  # active LOW

    def was_pressed(self):
        if self._pressed:
            self._pressed = False
            return True
        return False

    def was_released(self):
        if self._released:
            self._released = False
            return True
        return False