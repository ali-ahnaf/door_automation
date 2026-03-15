# Smart Door Lock System

A comprehensive RFID-based door lock system for Raspberry Pi Pico with motor control, user management, and security features.

## Uploading files to pico

```
pip install mpremote

# uploads everything at once from current dir to pico
mpremote cp -r . :/

# list files
mpremote ls

# remove file
mpremote rm my_old_file.py
```

## Features

- **RFID Authentication**: Secure access using MFRC522 RFID reader
- **Motor Control**: Automated door lock/unlock mechanism
- **User Management**: Hardcoded user database with names and flat numbers
- **Security Features**: Access attempt tracking, lockout protection, auto-lock
- **Audio/Visual Feedback**: Buzzer alerts and LED status indicators
- **Logging**: Comprehensive system logging for monitoring and debugging
- **Emergency Functions**: Emergency unlock capability

## Hardware Requirements

### Components
- Raspberry Pi Pico (or Pico W)
- MFRC522 RFID Reader Module
- DC Motor (for door lock mechanism)
- Motor Driver (L298N or similar)
- Buzzer (piezo buzzer)
- LED (status indicator)
- Jumper wires
- Breadboard (optional)

### Pin Connections

| Component | Pico Pin | Description |
|-----------|----------|-------------|
| RFID SCK (yellow) | GPIO 6 | SPI Clock |
| RFID MISO (red) | GPIO 4 | SPI MISO |
| RFID MOSI (orange) | GPIO 7 | SPI MOSI |
| RFID SDA (green) | GPIO 5 | SPI Chip Select |
| RFID RST (black) | GPIO 22 | RFID Reset |
| RFID GND (brown) | GPIO 38 | GND |
| RFID 3.3 (white) | GPIO 36 | POWER IN |
| Motor IN1 | GPIO 17 | Motor Control 1 |
| Motor IN2 | GPIO 18 | Motor Control 2 |
| Buzzer (green) | GPIO 14 | Audio Output |
| Status LED | GPIO 28 | Visual Status |

### 3. Configure Users
Edit `db.py` to add your users:

```python
users = {
    1234567890: {"name": "John Smith", "flat": "101", "access_level": "resident"},
    2345678901: {"name": "Sarah Johnson", "flat": "102", "access_level": "resident"},
    # Add more users as needed
}
```

Replace the example RFID IDs with your actual card IDs.

### Pin Assignments
Update pin assignments in `constants.py` if your hardware setup differs.



### NUKE (System Reset)
In case the pico runs into an infinite loop and cannot be exited:

1. Power off the board
2. Hold the BOOTSEL button and power the board
3. A USB mass storage mode will be activated
4. Drag and drop the `universal_flash_nuke.uf2` file in the directory
5. The board will automatically reset
6. Now configure interpreter and install MicroPython on the board

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for error messages
3. Verify hardware connections
4. Test individual components using the test function


```
import machine
import time
import utime as timex
from machine import I2C, Pin

from lib.lcd import LCD
from lib.keypad import Keypad
from lib.servo import Servo
from lib.buzzer import Buzzer
from db import get_user, USERS

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
    lcd.write("App crashed. Restarting")
    servo.move(0, 2)
    lcd.write(greeting)
    wrong_attempts = 0
    last_key = None

wrong_attempts = 0

while True:
    try:
        key = keypad.scan()

        if key and key != last_key:
            print("Pressed:", key)
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
                        servo.move(180, 2) # open locker by moving servo 180 degree
                        lcd.clear()
                        print(f"Access granted for {user['name']} in flat {user['flat']}.")
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
            elif key == 'C':   # Backspace   
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



```