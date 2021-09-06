class Memory:
    
    def __init__(self):
        self.contents = []
        self.writeLocationAddress = ""
        self.currentBank = 0
        self.currentPatch = 0
        
    def clearAll(self):
        self.contents.clear()
    
    def loadInstruction(self, instruction):
        if self.contents.count(instruction) == 0:
            self.contents.append(instruction)
        elif self.contents.count(instruction) == 1:
            self.contents.remove(instruction)
    
    def loadPatch(self, instructions):
        self.clearAll()
        for instruction in instructions:
            self.contents.append(instruction)
            
    def readAll(self):
        return self.contents
    
    def getWriteLocation(self):
        return self.writeLocationAddress
    
    def updateWriteLocation(self, newAdd):
        self.writeLocationAddress = str(newAdd)
        
    def resetWriteLocation(self):
        self.writeLocationAddress = ""
    
    def updateCurrentPatch(self, newPatch):
        self.currentPatch = newPatch
        print("Updating current patch: " + str(newPatch))
        
    def getCurrentPatch(self):
        return self.currentPatch
    
    def updateCurrentBank(self, newBank):
        self.currentBank = newBank
    
    def getCurrentBank(self):
        return self.currentBank