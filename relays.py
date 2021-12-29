import machine

outputs = {
            1: machine.Pin(11, machine.Pin.OUT),
            2: machine.Pin(12, machine.Pin.OUT),
            3: machine.Pin(13, machine.Pin.OUT),
            4: machine.Pin(14, machine.Pin.OUT),
            5: machine.Pin(15, machine.Pin.OUT)
            }
        
def toggle_multi(patch):
    for step in patch:
        outputs[step].toggle()
        
def toggle_one(s):
    outputs[s].toggle()
        
def set_high(relay):
    outputs[relay].value(1)
    
def set_low(relay):
    outputs[relay].value(0)
        
def reset():
    for output in outputs.values():
        output.value(0)
