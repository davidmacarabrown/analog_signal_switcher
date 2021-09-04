from machine import Pin
import time

        
class IndicatorLeds:
    
    def __init__(self):
        self.allLeds = {}
        
    def toggleOne(self, led):
        self.allLeds[led].toggle()
    
    def toggleMultiple(self, program):
        for step in program:
            self.allLeds[step].toggle()
            
    def toggleAll(self):
        for led in self.allLeds.values():
            led.toggle()
            
    def rapidBlink(self, led):
        self.allLeds[led].value(0)
        time.sleep(0.05)
        i = 0
        while i < 14:
            self.allLeds[led].toggle()
            time.sleep(0.05)
            i += 1
    
    def singleBlink(self, led):
        self.allLeds[led].value(0)
        self.allLeds[led].toggle()
        time.sleep(0.5)
        self.allLeds[led].toggle()
        
    def resetAll(self):
        for led in self.allLeds.values():
            led.value(0)
            
    def resetOne(self, led):
        self.allLeds[led].value(0)
