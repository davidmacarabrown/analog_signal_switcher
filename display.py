from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

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
        self.display.fill(0)
        
    def refresh(self):
        self.display.fill(0)
        
        if self.mode:
            self.display.text(self.mode, 0, 4)
        if self.line_one:
            self.display.text(self.line_one, 0, 4)
        if self.line_two:
            self.display.text(self.line_two, 0, 20)
        if self.bank:
            self.display.text(self.bank, 0, 20)
        if self.patch:
            self.display.text(self.patch, 54, 20)
        
        self.display.show()
    
    def update_mode(self, modeIn):
        self.mode = ">> " + str(modeIn)
        
    def update_line_one(self, line):
        self.line_one = str(line)

    def update_line_two(self, line):
        self.line_two = str(line)

    def update_bank(self, bank):
        self.bank = "Bank:" + str(bank)

    def update_patch(self, patch):
        self.patch = "Patch:" + str(patch)


    

