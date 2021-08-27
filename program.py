class ProgramMemory:
    
    def __init__(self):
        
        self.contents = {
                            1 : [1, 3, 5],
                            2 : [3, 4, 5],
                            3: [1, 5],
                            4: [],
                            5: []
                        }
        
        self.lastProgramUsed = 1
        
    def writeToLocation(self, location, array):
        self.contents[location] = array
        
    def deleteFromLocation(self, location):
        self.contents.pop(location)
        
    def readFromLocation(self, location):
        return self.contents.get(location)
    
    def deleteAll(self):
        self.contents.clear()
        
    def readLastProgramUsed(self):
        return self.lastProgramUsed
    
    def updateLastProgramUsed(self, newProgram):
        self.lastProgramUsed = newProgram