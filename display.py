from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)

class Display:
    
    def __init__(self):
        self.display = SSD1306_I2C(128, 64, i2c)
        self.header = None
        self.line_one = None
        self.line_two = None
        self.line_three = None
        
    def clear(self):
        self.header = None
        self.line_one = None
        self.line_two = None
        self.line_three = None
    
    def refresh(self):
        self.display.fill(0)
        
        if self.header:
            self.display.text(self.header, 0, 0)
        if self.line_one:
            self.display.text(self.line_one, 0, 16)
        if self.line_two:
            self.display.text(self.line_two, 0, 24)
        
        self.display.show()
    
    def update_mode(self, mode):
        self.header = mode.upper()
        
    def update_line_one(self, line):
        self.line_one = str(line)

    def update_line_two(self, line):
        self.line_two = str(line)

    def update_bank(self, bank):
        self.line_one = f"BANK: {str(bank)}"

    def update_patch(self, patch):
        self.line_two = f"PATCH: {str(patch)}"
        
    def save_message(self, location):
        self.clear()
        self.line_one =">> Saving..."
        self.line_two = f"> {str(location)}"
        self.refresh()

    def write_warning(self):
        self.clear()
        self.line_one = "Select Location"
        self.line_two = "Mode > Exit"
        self.refresh()