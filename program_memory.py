import machine
import uos
import json

class ProgramMemory:
    
    def __init__(self):
        pass
    
    def setDefaultPatch(self, bankNo, patchNo):
        tempDict = {
            "patch": patchNo,
            "bank": bankNo
                }
        with open("/program/default.json", "w") as file:
            json.dump(tempDict, file)
            
    def loadDefaultPatch(self):
        tempDict = {
            "patch": None,
            "bank": None
                }
        with open("/program/default.json", "r") as file:
            data = json.load(file)
            return data
        
        
    def loadPatch(self, bankNo, patchNo):
        data = None
        with open("/program/bank" + str(bankNo) + ".json", "r") as file:
            data = json.load(file)
        patch = data[str(patchNo)]
        return patch
       
    def writePatch(self, bankNo, patchNo, patchData):
        data = None
        with open("/program/bank" +str(bankNo) + ".json", "r") as file:
            data = json.load(file)
        data[str(patchNo)] = patchData
        with open("/program/bank" + str(bankNo) + ".json", "w") as write:
            json.dump(data, write)