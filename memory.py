class Memory:
    
    def __init__(self):
        self.contents = []
        self.lastProgramUsed = 0
        self.writeLocationAddress = 0
        
    def clearOne(instruction):
        self.contents.remove(instruction)
    
    def clearAll(self):
        self.contents.clear()
    
    def loadInstruction(self, instruction):
        if self.contents.count(instruction) == 0:
            self.contents.append(instruction)
    
    def loadProgram(self, instructionList):
        self.clearAll()
        self.contents = instructionList
            
    def readAll(self):
        return self.contents
    
    def getWriteLocation(self):
        return self.writeLocationAddress
    
    def updateWriteLocation(self, newAdd):
        self.writeLocationAddress = newAdd