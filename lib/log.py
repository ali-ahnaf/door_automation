import utime
import uio

class Logger:
    def __init__(self, log_file_name="app_log.txt"):
        self.log_file_name = log_file_name
        self.log_file = uio.open(log_file_name, "a")
    
    def log(self, message):
        timestamp = utime.time()
        log_entry = f"[{utime.localtime(timestamp)}] {message}\n"
        
        print(log_entry, end="")
        
        # Write to the log file
        self.log_file.write(log_entry)
        self.log_file.flush()
    
    def close(self):
        self.log_file.close()
