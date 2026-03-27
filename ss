import machine
import time
import utime as timex
from machine import I2C, Pin

from lib.lcd import LCD
from lib.keypad import Keypad
from lib.servo import Servo
from lib.buzzer import Buzzer
from lib.button import Button
from db import get_user, USERS

# button
servo_btn = Button(6)

# buzzer
buzzer = Buzzer()

# initialize i2c bus
i2c = machine.I2C(1, scl=Pin(27), sda=Pin(26), freq=100000)

# keypad
keypad = Keypad(i2c)
last_key = None
pin = ""

# lcd
lcd=LCD(i2c)
lcd.clear()
greeting='Enter PIN'
lcd.write(greeting)

# servo
servo = Servo(0)
servo.move(0, 1) # start at angle 0

wrong_pin_delay = 2000

def reset():
    global pin, wrong_attempts, last_key
    buzzer.reset()
    pin = ""
    lcd.clear()
    lcd.write("Restarting")
    servo.move(0, 2)
    lcd.clear()
    lcd.write(greeting)
    wrong_attempts = 0
    last_key = None

wrong_attempts = 0
door_open = False
door_open_time = 0

def open_door():
    servo.move(180, 2) # open locker by moving servo 180 degree
    lcd.clear()
    lcd.write("Door open. Push")

while True:
    try:
        key = keypad.scan()
        btn.update()

        # Open door (trigger once)
        if btn.was_pressed() and not door_open:
            open_door()
            door_open = True
            door_open_time = time.ticks_ms()

        # Handle timeout (5 seconds)
        if door_open and time.ticks_diff(time.ticks_ms(), door_open_time) > 5000:
            lcd.clear()
            pin = ""
            lcd.write(greeting)
            wrong_attempts = 0
            door_open = False
            servo.move(0, 2) # close locker by moving servo 180 degree
            wrong_attempts = 0

        if key and key != last_key:
            #print("Pressed:", key)
            buzzer.beep()
            last_key = key

            # If D is pressed → submit
            if key == 'D':
                print("Submit pin :", pin)
                lcd.clear()
                if pin:
                    user = get_user(pin)
                    if user:
                        lcd.write("Access granted: " + user['name'])
                        open_door()
                        door_open = True
                        door_open_time = time.ticks_ms()
                        print(f"Access granted for {user['name']} in flat {user['flat']}.")
                        time.sleep_ms(10000) # wait for 10s then lock the door
                        servo.move(0, 2) # close locker by moving servo 180 degree
                        wrong_attempts = 0
                    else:
                        lcd.write("Invalid PIN. Wait 2s")
                        time.sleep_ms(2000)
                        wrong_attempts += 1
                        print("Invalid PIN. Access denied.")                        
                
                if wrong_attempts > 2:
                    lcd.clear()
                    lcd.write("Locked for 5m")
                    time.sleep_ms(5*1000*60)
                    wrong_attempts = 0

                lcd.clear()
                pin = ""   # reset
                lcd.write(greeting)
                wrong_attempts = 0
            elif key == 'C': # Backspace   
                pin = ""             
                lcd.clear()
                lcd.write(greeting)
            # If it is a keypad character → add to pin
            elif key in ['0','1','2','3','4','5','6','7','8','9','A','B']:
                pin += key
                # show pin on LCD
                lcd.clear()
                # lcd.write(pin)
                # hide pin
                lcd.write("*" * len(pin))

        if not key:
            last_key = None

        time.sleep_ms(50)

    except Exception as e:
        print("Error:", e)
        reset()
