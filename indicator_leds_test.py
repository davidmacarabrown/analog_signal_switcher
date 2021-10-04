from indicator_leds import IndicatorLeds

leds = IndicatorLeds()

leds.allLeds[1] = machine.Pin(4, machine.Pin.OUT)
leds.allLeds[2] = machine.Pin(3, machine.Pin.OUT)
leds.allLeds[3] = machine.Pin(2, machine.Pin.OUT)
leds.allLeds[4] = machine.Pin(1, machine.Pin.OUT)
leds.allLeds[5] = machine.Pin(0, machine.Pin.OUT)

leds.allLeds["write"] = machine.Pin(5, machine.Pin.OUT)

indicator = machine.Pin(25, machine.Pin.OUT)
indicator.value(0)