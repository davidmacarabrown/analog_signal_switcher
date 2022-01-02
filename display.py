from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import framebuf

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)

class Display:
    
    def __init__(self):
        self.display = SSD1306_I2C(128, 64, i2c)
        self.large_font_framebuffer = {}
        
        self.items = [
            {
                "text": None,
                "line": 0,
                "margin": 0
            },
            {
                "text": None,
                "line": 16,
                "margin": 0
            },
            {
                "text": None,
                "line": 24,
                "margin": 0
             },
            {
                "text": None,
                "line": 32,
                "margin": 0
            }
            ]
        
        self.bank_patch = {
            "bank": None,
            "patch": None
            }
        
        for i in range(1, 6, 1):
            with open(f"/img/{i}.pbm", "rb") as image:
                image.readline()
                image.readline()
                image.readline()
                img = bytearray(image.read())
                self.large_font_framebuffer[i] = framebuf.FrameBuffer(img, 36, 48, framebuf.MONO_HLSB)
                
        with open("/img/dash.pbm", "rb") as dash:
            dash.readline()
            dash.readline()
            dash.readline()
            img = bytearray(dash.read())
            self.large_font_framebuffer["-"] = framebuf.FrameBuffer(img, 36, 48, framebuf.MONO_HLSB)
            
        with open("/img/colon.pbm", "rb") as colon:
            colon.readline()
            colon.readline()
            colon.readline()
            img = bytearray(colon.read())
            self.large_font_framebuffer[":"] = framebuf.FrameBuffer(img, 16, 48, framebuf.MONO_HLSB)
        
    def clear(self):
        self.items = [
            {
                "text": None,
                "line": 0,
                "margin": 0
            },
            {
                "text": None,
                "line": 16,
                "margin": 0
            },
            {
                "text": None,
                "line": 24,
                "margin": 0
             },
            {
                "text": None,
                "line": 32,
                "margin": 0
            }
            ]
        
        self.bank_patch = {
            "bank": None,
            "patch": None
            }
    
    def refresh(self):
        self.display.fill(0)
        for i in self.items:
            if i["text"]:
                self.display.text(i["text"], i["margin"], i["line"], 1)
                
        if self.bank_patch["bank"] and self.bank_patch["patch"]:
            self.display.blit(self.large_font_framebuffer[self.bank_patch["bank"]], 12, 16, 0)
            self.display.blit(self.large_font_framebuffer[":"], 56, 16, 0)
            self.display.blit(self.large_font_framebuffer[self.bank_patch["patch"]], 80, 16, 0)
                
        self.display.show()
        
    def update_line(self, text, line, indent = False):
        margin = 0
        if indent:
            margin = 8
            
        self.items[line]["text"] = text.upper()
        self.items[line]["margin"] = margin
        
    def update_bank(self, bank):
        self.bank_patch["bank"] = bank
        
    def update_patch(self, patch):
        self.bank_patch["patch"] = patch