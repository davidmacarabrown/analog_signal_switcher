class Memory:
    
    def __init__(self):
        self.contents = []
        self.writeLocationAddress = 0
        self.currentProgram = 0
        
    def clearAll(self):
        self.contents.clear()
    
    def loadInstruction(self, instruction):
        if self.contents.count(instruction) == 0:
            self.contents.append(instruction)
        elif self.contents.count(instruction) == 1:
            self.contents.remove(instruction)
    
    def loadProgram(self, program):
        self.clearAll()
        for instruction in program:
            self.contents.append(instruction)
            
    def readAll(self):
        return self.contents
    
    def getWriteLocation(self):
        return self.writeLocationAddress
    
    def updateWriteLocation(self, newAdd):
        self.writeLocationAddress = newAdd
    
    def updateCurrentProgram(self, newProgram):
        self.currentProgram = newProgram