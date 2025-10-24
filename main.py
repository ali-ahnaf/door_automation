import utime
from lib.mfrc522 import MFRC522
from lib.buzzer import Buzzer
from lib.led import Led
from lib.motor import Motor
from lib.button import Button
import constants as c
from db import get_user

# Initialize components
rfid = MFRC522(spi_id=0, sck=c.PIN_RFID_SCK, miso=c.PIN_RFID_MISO, mosi=c.PIN_RFID_MOSI, cs=c.PIN_RFID_CS, rst=c.PIN_RFID_RST)
motor = Motor(c.PIN_MOTOR_IN1, c.PIN_MOTOR_IN2)
buzzer = Buzzer(c.PIN_BUZZER)
led = Led(c.PIN_LED)
button_forward = Button(c.PIN_BUTTON_FORWARD)
button_backward = Button(c.PIN_BUTTON_BACKWARD)

def main():
    print("Simple Door Lock System Starting...")
    
    # System state
    door_locked = True
    door_unlock_until = 0
    last_scan_time = 0
    scan_cooldown = 10  # 10 seconds cooldown between scans
    
    print("System ready! Bring RFID card close to reader.")
    buzzer.alert(c.BUZZER_SUCCESS)  # Startup beep
    led.turn_on()    # Ready indicator
    
    try:
        while True:
            current_time = utime.time()
            
            # Auto-lock door if time expired
            if not door_locked and current_time >= door_unlock_until:
                print("Auto-locking door...")

                motor.backward()
                utime.sleep(c.MOTOR_LOCK_TIME)
                motor.stop()

                door_locked = True
                buzzer.alert(c.BUZZER_ERROR)  # Lock beep
                led.turn_off()  # Turn off LED when locked
                led.stop_blinking()  # Stop any current blinking
                print("Door locked")

                utime.sleep(5)
            
            # Check if enough time has passed since last scan
            if current_time - last_scan_time >= scan_cooldown:
                # Try to read RFID card
                rfid.init()
                (stat, tag_type) = rfid.request(rfid.REQIDL)
                
                if stat == rfid.OK:
                    (stat, uid) = rfid.SelectTagSN()
                    
                    if stat == rfid.OK:
                        # Get card ID
                        card_id = int.from_bytes(bytes(uid), "little", False)
                        print(f"Card detected: {card_id}")
                        
                        # Update last scan time
                        last_scan_time = current_time
                        
                        # Check if user is authorized
                        user = get_user(card_id)
                        if user:
                            print(f"Access granted: {user['name']} (Flat: {user['flat']})")
                            
                            # Unlock door
                            if door_locked:
                                print("Unlocking door...")
                                led.blink(c.DOOR_OPEN_TIME)

                                motor.forward()
                                utime.sleep(c.MOTOR_UNLOCK_TIME)
                                motor.stop()

                                current_time = utime.time()
                                door_locked = False
                                door_unlock_until = current_time + c.DOOR_OPEN_TIME
                                buzzer.alert(c.BUZZER_SUCCESS)  # Success beep
                                print("Door unlocked")
                            else:
                                print("Door already unlocked")
                                buzzer.alert(c.BUZZER_SUCCESS)
                        else:
                            print(f"Access denied: Card {card_id} not authorized")
                            buzzer.alert(c.BUZZER_ERROR)  # Error beep
                            led.blink(2.0)  # Error blink for 2 seconds
                            utime.sleep(2)  # Wait for blink to complete
                            led.stop_blinking()  # Stop the error blink
                    
                    utime.sleep_ms(500)  # Prevent multiple reads
            
            # Check manual motor control buttons
            if button_forward.is_held():
                print("Manual forward button held - rotating motor forward")
                motor.forward()
                led.blink(2)
            elif button_backward.is_held():
                print("Manual backward button held - rotating motor backward")
                motor.backward()
                led.blink(2)
            else:
                # Stop motor if no buttons are pressed
                motor.stop()
                led.stop_blinking()
            
            utime.sleep_ms(100)  # Small delay
            
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
        motor.stop()
        led.turn_off()
    except Exception as e:
        print(f"System error: {str(e)}")
        motor.stop()
        led.turn_off()

if __name__ == "__main__":
    main()
