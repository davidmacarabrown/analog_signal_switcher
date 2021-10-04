class Instruction:
    
    def __init__(self):
        self.contents = []
        
    def loadInstruction(self, instr):
        self.contents.append(instr)
            
    def loadPatch(self, patch):
        self.contents.clear()
        for instruction in patch:
            self.contents.append(instruction)
            
    def clearAll(self):
        self.contents.clear()
        
    def read(self):
        return self.contents