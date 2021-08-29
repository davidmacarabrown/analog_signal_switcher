class ProgramMemory:
    
    def __init__(self):
        
        self.contents = {
                            "1" : [1,2,3,4,5],
                            "2" : [3, 4, 5],
                            "3" : [1, 5],
                            "4" : [],
                            "5" : []
                        }
        
        self.lastProgramUsed = "1"
        
    def writeToLocation(self, location, array):
        self.contents[location] = array
        
#     def deleteFromLocation(self, location):
#         self.contents.pop(location)
        
    def readFromLocation(self, location):
        return self.contents[location]
    
#     def deleteAll(self):
#         self.contents.clear()

    def getLastProgramUsed(self):
        return self.lastProgramUsed
        
    def readLastProgramUsed(self):
        last = self.lastProgramUsed
        return self.contents[last]
    
    def updateLastProgramUsed(self, newProgram):
        self.lastProgramUsed = newProgram