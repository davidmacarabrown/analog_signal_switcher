from machine import Pin
from relay_output import RelayOutput

relays = RelayOutput()

relays.outputs[1] = machine.Pin(6, machine.Pin.OUT)
relays.outputs[2] = machine.Pin(7, machine.Pin.OUT)
relays.outputs[3] = machine.Pin(8, machine.Pin.OUT)
relays.outputs[4] = machine.Pin(9, machine.Pin.OUT)
relays.outputs[5] = machine.Pin(28, machine.Pin.OUT)

testPatch = [1,2,3,4,5]

relays.latchPatch(testPatch)



