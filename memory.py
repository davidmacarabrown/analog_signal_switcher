class Memory:
    
    def __init__(self):
        self.contents = []
        self.writeLocationAddress = None
        self.currentBank = None
        self.currentPatch = None
        self.inputRegister = None
        
    def clearAll(self):
        self.contents.clear()
        
    def readInputRegister(self):
        return this.inputRegister
    
    def updateInputRegister(self, newInput):
        this.inputRegister = newInput
    
    def clearInputRegister(self):
        this.inputRegister = None
    
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
        self.writeLocationAddress = newAdd
        
    def resetWriteLocation(self):
        self.writeLocationAddress = None
    
    def updateCurrentPatch(self, newPatch):
        self.currentPatch = newPatch
        print("Updating current patch: " + str(newPatch))
        
    def getCurrentPatch(self):
        return self.currentPatch
    
    def updateCurrentBank(self, newBank):
        self.currentBank = newBank
    
    def getCurrentBank(self):
        return self.currentBank
