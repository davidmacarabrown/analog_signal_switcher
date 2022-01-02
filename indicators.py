import time
import machine
import _thread


indicators = {
                1: machine.Pin(0, machine.Pin.OUT),
                2: machine.Pin(1, machine.Pin.OUT),
                3: machine.Pin(2, machine.Pin.OUT),
                4: machine.Pin(3, machine.Pin.OUT),
                5: machine.Pin(4, machine.Pin.OUT),
                6: machine.Pin(5, machine.Pin.OUT)
                    }
    
def toggle(led):
    indicators[led].toggle()
    
def set_high(led):
    indicators[led].value(1)
    
def set_low(led):
    indicators[led].value(0)

def toggle_multi(program):
    for step in program:
        indicators[step].toggle()
        
def toggle_all():
    for led in indicators.values():
        led.toggle()
        
def toggle_one(led):
    indicators[led].toggle()
        
def rapid_blink(led):
    time.sleep(0.05)
    i = 0
    while i < 15:
        indicators[led].toggle()
        time.sleep(0.05)
        i += 1
    return

def single_blink(led):
    indicators[led].value(0)
    indicators[led].toggle()
    time.sleep(0.5)
    indicators[led].toggle()
    
def reset_all():
    for led in indicators.values():
        led.value(0)
        