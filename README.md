# Smart Door Lock System

A comprehensive RFID-based door lock system for Raspberry Pi Pico with motor control, user management, and security features.

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
| RFID SCK | GPIO 6 | SPI Clock |
| RFID MISO | GPIO 4 | SPI MISO |
| RFID MOSI | GPIO 7 | SPI MOSI |
| RFID CS | GPIO 5 | SPI Chip Select |
| RFID RST | GPIO 22 | RFID Reset |
| Motor IN1 | GPIO 17 | Motor Control 1 |
| Motor IN2 | GPIO 16 | Motor Control 2 |
| Buzzer | GPIO 14 | Audio Output |
| Status LED | GPIO 15 | Visual Status |

## Software Setup

### 1. Install MicroPython
- Flash MicroPython firmware to your Raspberry Pi Pico
- Use Thonny IDE or similar for code upload

### 2. Upload Code
Upload all Python files from the `src/` directory to your Pico:
- `main.py` - Main system entry point
- `system_controller.py` - System integration and control
- `door_controller.py` - Motor control for door lock
- `rfid_manager.py` - RFID card reading and authentication
- `db.py` - User database and system state
- `constants.py` - System configuration constants
- `buzzer.py` - Audio feedback control
- `led.py` - LED status control
- `log.py` - System logging
- `mfrc522.py` - RFID reader driver

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

## Usage

### Starting the System
1. Power on the Raspberry Pi Pico
2. The system will automatically start and initialize
3. Green LED indicates system is ready
4. Bring an authorized RFID card close to the reader

### System Behavior
- **Valid Card**: Door unlocks, green LED, success beep, auto-locks after 10 seconds
- **Invalid Card**: Access denied, red LED blink, error beep, failed attempt recorded
- **Too Many Failed Attempts**: System lockout for 30 seconds, red LED fast blink
- **Emergency**: Use emergency unlock function if needed

### Testing Components
To test individual components, modify `main.py`:

```python
if __name__ == "__main__":
    test_components()  # Uncomment this line
    # main()  # Comment out this line
```

## Configuration

### Timing Settings (constants.py)
- `MOTOR_UNLOCK_TIME`: Time to run motor for unlock (default: 2.0s)
- `MOTOR_LOCK_TIME`: Time to run motor for lock (default: 2.0s)
- `ACCESS_GRACE_PERIOD`: How long door stays unlocked (default: 10s)
- `MAX_FAILED_ATTEMPTS`: Failed attempts before lockout (default: 3)
- `LOCKOUT_DURATION`: Lockout duration in seconds (default: 30s)

### Pin Assignments
Update pin assignments in `constants.py` if your hardware setup differs.

## Security Features

1. **Access Control**: Only registered RFID cards can unlock the door
2. **Attempt Tracking**: Failed access attempts are logged and counted
3. **Lockout Protection**: System locks out after too many failed attempts
4. **Auto-Lock**: Door automatically locks after grace period
5. **Audit Trail**: All access attempts are logged with timestamps

## Troubleshooting

### Common Issues

1. **RFID Not Reading Cards**
   - Check wiring connections
   - Ensure card is close enough to reader
   - Verify RFID card IDs in database

2. **Motor Not Moving**
   - Check motor driver connections
   - Verify power supply to motor
   - Test motor with manual commands

3. **System Not Starting**
   - Check all file uploads completed
   - Verify MicroPython installation
   - Check serial output for error messages

### Debug Mode
Enable debug logging by modifying the Logger class in `log.py` or check log files:
- `main.log` - System startup and main events
- `system_controller.log` - System control events
- `door_controller.log` - Motor control events
- `rfid_manager.log` - RFID reading events

## File Structure

```
src/
├── main.py                 # Main entry point
├── system_controller.py    # System integration
├── door_controller.py      # Motor control
├── rfid_manager.py         # RFID handling
├── db.py                   # User database
├── constants.py            # Configuration
├── buzzer.py              # Audio feedback
├── led.py                 # LED control
├── log.py                 # Logging system
└── mfrc522.py             # RFID driver
```

## Emergency Recovery

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