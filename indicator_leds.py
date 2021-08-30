from machine import Pin
import time

        
class IndicatorLeds:
    
    def __init__(self):
        self.allLeds = {}
    
    def toggleProgram(self, program):
        for step in program:
            self.allLeds[step].toggle()
            
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

# ledOne = machine.Pin(4, machine.Pin.OUT)
# ledTwo = machine.Pin(3, machine.Pin.OUT)
# ledThree = machine.Pin(2, machine.Pin.OUT)
# ledFour =

leds = IndicatorLeds()

leds.allLeds[1] = machine.Pin(4, machine.Pin.OUT)
leds.allLeds[2] = machine.Pin(3, machine.Pin.OUT)
leds.allLeds[3] = machine.Pin(2, machine.Pin.OUT)
leds.allLeds[4] = machine.Pin(1, machine.Pin.OUT)
leds.allLeds[5] = machine.Pin(0, machine.Pin.OUT)
leds.allLeds[6] = machine.Pin(5, machine.Pin.OUT)


scuffedDemoProgram = [1,2,3,4,5]

# leds.latchProgram(scuffedDemoProgram)

leds.singleBlink(6)

