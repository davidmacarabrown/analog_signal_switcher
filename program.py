import machine
import uos

class ProgramMemory:
    
    def __init__(self):
        self.lastProgramUsed = 0
    
    def updateLastProgramUsed(self, newProgram):
        self.lastProgramUsed = newProgram
    
    def getLastProgramUsed(self):
        return self.lastProgramUsed
    
    def loadLastProgramUsed(self):
        with open("/patch/default.txt", "r") as file:
            lastProgram = file.read()
            parsed = int(lastProgram)
            self.lastProgramUsed = parsed
        print("Loading last program used from disk: " + lastProgram)
        return parsed
        
    def loadFromDisk(self, patchNo):
        with open("/patch/" + str(patchNo) + ".txt", "r") as file:
            bank = file.read()
            array = []
            for i in bank:
                array.append(int(i))
            print("Loading  from disk: " +str(array))
            return array
        
    def writeToDisk(self, patchNo, patchData):
        parsed = ""
        for c in patchData:
            parsed += str(c)
        print("Writing " + parsed + " to location: " + str(patchNo))
        with open("/patch/" + str(patchNo) + ".txt", "w") as file:
            file.write(parsed)
    
    def setDefaultProgram(self, default):
        parsed = str(default)
        with open("/patch/default.txt", "w") as file:
            print("Setting default program: " + default)
            file.write(default)
            
    def readDefaultProgram(self):
        with open("/patch/default.txt", "r") as file:
            default = file.read()
            print("Reading default program: " + default)
            parsed = int(default)
            return parsed