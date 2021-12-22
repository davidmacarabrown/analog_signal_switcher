import machine

class RelayOutput:
    
    def __init__(self):
        self.outputs = {
                        1: machine.Pin(6, machine.Pin.OUT),
                        2: machine.Pin(7, machine.Pin.OUT),
                        3: machine.Pin(8, machine.Pin.OUT),
                        4: machine.Pin(9, machine.Pin.OUT),
                        5: machine.Pin(28, machine.Pin.OUT)
                        }
        
    def latch_multi(self, patch):
        for step in patch:
            self.outputs[step].toggle()
    
    def reset(self):
        for output in self.outputs.values():
            output.value(0)