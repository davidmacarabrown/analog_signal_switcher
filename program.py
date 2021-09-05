import machine
import uos
import json

class ProgramMemory:
    
    def __init__(self):
        self.lastProgramUsed = 0
        self.lastBankUsed = 0
    
    def updateLastProgramUsed(self, newProgram):
        self.lastProgramUsed = newProgram
    
    def getLastProgramUsed(self):
        return self.lastProgramUsed
    
    def loadLastProgramUsed(self):
        data = None
        with open("/program/bank" + str(self.lastBankUsed) + ".json", "r") as file:
            data = json.load(file)
        patch = data[str(lastProgramUsed)]
        
    def loadFromDisk(self, bankNo, patchNo):
        data = None
        with open("/program/bank" + str(bankNo) + ".json", "r") as file:
            data = json.load(file)
        patch = data[str(patchNo)]
        return patch
       
    def writeToDisk(self, bankNo, patchNo, patchData):
        data = None
        with open("/program/bank" +str(bankNo) + ".json", "r") as file:
            data = json.load(file)
        data[str(patchNo)] = patchData
        with open("/program/bank" + str(bankNo) + ".json", "w") as write:
            json.dump(data, write)
        
    
    def setDefaultProgram(self, bankNo, patchNo):
        tempDict = {
        "patch": patchNo,
        "bank": bankNo
        }
        with open("/program/default.json", "w") as file:
            json.dump(tempDict, file)
            
    def readDefaultProgram(self):
        bank = ""
        patch = ""
        with open("/program/default.json", "r") as file:
            payload = json.load(file)
        
        return payload
    
pMem = ProgramMemory()

# pMem.setDefaultProgram(1, 6)
# 
# print(pMem.readDefaultProgram())

pMem.writeToDisk(1,1, [1])
print(pMem.loadFromDisk(1,1))
