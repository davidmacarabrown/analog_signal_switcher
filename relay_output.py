from machine import Pin

class RelayOutput:
    
    def __init__(self):
        self.outputs = {}
        
    def latchSingle(self, relay):
        self.outputs[relay].value(1)
        
    def latchPatch(self, patch):
        self.resetAll()
        for step in patch:
            self.outputs[step].value(1)
    
    def resetAll(self):
        for output in self.outputs.values():
            output.value(0)