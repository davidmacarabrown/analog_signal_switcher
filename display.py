from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)

class Display:
    
    def __init__(self):
        self.display = SSD1306_I2C(128, 32, i2c)
        self.line_one = None
        self.line_two = None
        self.bank= None
        self.patch= None
        
    def clear(self):
        self.mode = None
        self.line_one = None
        self.line_two = None
        self.bank= None
        self.patch= None
    
    def refresh(self):
        self.display.fill(0)
        
        if self.mode:
            self.display.text(self.mode, 0, 0)
        if self.line_one:
            self.display.text(self.line_one, 0, 0)
        if self.line_two:
            self.display.text(self.line_two, 0, 20)
        if self.bank:
            self.display.text(self.bank, 0, 10)
        if self.patch:
            self.display.text(self.patch, 54, 20)
        
        self.display.show()
    
    def update_mode(self, modeIn):
        self.mode = ">> " + str(modeIn).upper()
        
    def update_line_one(self, line):
        self.line_one = str(line)

    def update_line_two(self, line):
        self.line_two = str(line)

    def update_bank(self, bank):
        self.bank = "BANK:" + str(bank)

    def update_patch(self, patch):
        self.patch = "PATCH:" + str(patch)
        
    def save_message(self, location):
        self.clear()
        self.update_line_one(">> Saving...")
        self.update_line_two("> " + str(location))
        self.refresh()

    def write_warning(self):
        self.clear()
        self.line_one = "Select Location"
        self.line_two = "Mode > Exit"
        self.refresh()