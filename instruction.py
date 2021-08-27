class Instruction:
    
    def __init__(self):
        self.contents = []
        
    def loadInstruction(self, inst):
        if self.contents.count(inst) == 0:
            self.contents.append(inst)
            
    def loadPatch(self, patch):
        self.contents = patch
            
    def clearAll(self):
        self.contents.clear()
        
    def read(self):
        return self.contents