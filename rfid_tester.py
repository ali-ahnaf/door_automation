import utime
from lib.mfrc522 import MFRC522
import constants as c

# Initialize RFID reader only
rfid = MFRC522(spi_id=0, sck=c.PIN_RFID_SCK, miso=c.PIN_RFID_MISO, mosi=c.PIN_RFID_MOSI, cs=c.PIN_RFID_CS, rst=c.PIN_RFID_RST)

def main():
    print("RFID Card ID Tester Starting...")
    print("Bring RFID cards close to reader to see their IDs.")
    print("Press Ctrl+C to exit.\n")
    
    last_scan_time = 0
    scan_cooldown = 2  # 2 seconds cooldown between scans
    
    try:
        while True:
            current_time = utime.time()
            
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
                        print(f"Card ID: {card_id}")
                        
                        # Update last scan time
                        last_scan_time = current_time
                    
                    utime.sleep_ms(500)  # Prevent multiple reads
            
            utime.sleep_ms(100)  # Small delay
            
    except KeyboardInterrupt:
        print("\nRFID Tester stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

