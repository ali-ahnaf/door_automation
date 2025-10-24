# Pin assignments
PIN_RFID_SCK = 6
PIN_RFID_MISO = 4
PIN_RFID_MOSI = 7
PIN_RFID_CS = 5
PIN_RFID_RST = 22

PIN_MOTOR_IN1 = 18
PIN_MOTOR_IN2 = 16

PIN_BUZZER = 14

PIN_LED = 28

# Button pins
PIN_BUTTON_FORWARD = 20  # Button to rotate motor forward
PIN_BUTTON_BACKWARD = 21  # Button to rotate motor backward

# Timing settings
MOTOR_UNLOCK_TIME = 6.0  # seconds to unlock door
MOTOR_LOCK_TIME = 6.0    # seconds to lock door
DOOR_OPEN_TIME = 8      # seconds door stays open
ERROR_BLINK_TIME = 0.5   # seconds to blink error

# Buzzer types
BUZZER_SUCCESS = 1
BUZZER_ERROR = 2
BUZZER_PROCESSING = 3
