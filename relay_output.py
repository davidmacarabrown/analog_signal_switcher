import machine

class RelayOutput:
    
    def __init__(self):
        self.outputs = {
                        1: machine.Pin(10, machine.Pin.OUT),
                        2: machine.Pin(11, machine.Pin.OUT),
                        3: machine.Pin(12, machine.Pin.OUT),
                        4: machine.Pin(13, machine.Pin.OUT),
                        5: machine.Pin(14, machine.Pin.OUT)
                        }
        
    
    def toggle_multi(self, patch):
        for step in patch:
            self.outputs[step].toggle()
            
    def set_high(self, relay):
        self.outputs[relay].value(1)
        
    def set_low(self, relay):
        self.outputs[relay].value(0)
            
    def reset(self):
        for output in self.outputs.values():
            output.value(0)