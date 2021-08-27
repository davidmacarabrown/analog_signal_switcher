class Memory:
    
    def __init__(self):
        self.contents = []
        
    def clearOne(instruction):
        self.contents.remove(instruction)
    
    def clearAll(self):
        self.contents.clear()
    
    def loadInstruction(self, instruction):
        if self.contents.count(instruction) == 0:
            self.contents.append(instruction)
    
    def loadProgram(self, instructionList):
        self.clearAll()
        for inst in instructionList:
            self.contents.append(inst)
        
        

