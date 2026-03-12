import time

class Keypad:
    def __init__(self, i2c, addr=0x20):
        self.i2c = i2c
        self.addr = addr

        self.keys = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
        ]

    def write_pcf(self, data):
        self.i2c.writeto(self.addr, bytes([data]))

    def read_pcf(self):
        return self.i2c.readfrom(self.addr, 1)[0]

    def scan(self):
        for col in range(4):

            data = 0xFF
            data &= ~(1 << (col + 4))   # pull column LOW

            self.write_pcf(data)
            time.sleep_ms(1)

            val = self.read_pcf()

            for row in range(4):
                if not (val & (1 << row)):
                    return self.keys[col][row]

        return None