import time
import machine
        
class IndicatorLeds:
    
    def __init__(self):
        self.indicators = {
                        1: machine.Pin(0, machine.Pin.OUT),
                        2: machine.Pin(1, machine.Pin.OUT),
                        3: machine.Pin(2, machine.Pin.OUT),
                        4: machine.Pin(3, machine.Pin.OUT),
                        5: machine.Pin(4, machine.Pin.OUT),
                        6: machine.Pin(5, machine.Pin.OUT)
                        }
        
    def toggle(self, led):
        self.indicators[led].toggle()
        
    def set_high(self, led):
        self.indicators[led].value(1)
        
    def set_low(self, led):
        self.indicators[led].value(0)
    
    def toggle_multi(self, program):
        for step in program:
            self.indicators[step].toggle()
            
    def toggle_all(self):
        for led in self.indicators.values():
            led.toggle()
            
    def rapid_blink(self, led):
        self.indicators[led].value(0)
        time.sleep(0.05)
        i = 0
        while i < 14:
            self.indicators[led].toggle()
            time.sleep(0.05)
            i += 1
    
    def single_blink(self, led):
        self.indicators[led].value(0)
        self.indicators[led].toggle()
        time.sleep(0.5)
        self.indicators[led].toggle()
        
    def reset_all(self):
        for led in self.indicators.values():
            led.value(0)
            
    def reset_one(self, led):
        self.indicators[led].value(0)
