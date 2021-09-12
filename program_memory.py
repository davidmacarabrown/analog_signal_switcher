import machine
import uos
import json

class ProgramMemory:
    
    def __init__(self):
        pass
    
    def setDefaultPatch(self, bankNo, patchNo):
        if type(bankNo) == int and type(patchNo) == int:
            tempDict = {
                "patch": patchNo,
                "bank": bankNo
                    }
            with open("/program/default.json", "w") as file:
                json.dump(tempDict, file)
        else:
            print("Program Memory: INCORRECT TYPE FOR setDefaultPatch")
            print("patchNo: " + str(type(patchNo)) + "bankNo: " + str(type(bankNo)))
            
    def loadDefaultPatch(self):
        tempDict = {
            "patch": None,
            "bank": None
                }
        with open("/program/default.json", "r") as file:
            data = json.load(file)
            return data
        
        
    def loadPatch(self, bankNo, patchNo):
        if type(bankNo) == int and type(patchNo) == int:
            data = None
            bankNoParsed = str(bankNo)
            patchNoParsed = str(patchNo)
            with open("/program/bank" + bankNoParsed + ".json", "r") as file:
                data = json.load(file)
            patch = data[patchNoParsed]
            return patch
        else:
            print("Program Memory: INCORRECT TYPE FOR loadPatch")
       
    def writePatch(self, bankNo, patchNo, patchData):
        if type(bankNo) == int and type(patchNo) == int:
            bankNoParsed = str(bankNo)
            patchNoParsed = str(patchNo)
            
            data = None
            with open("/program/bank" + bankNoParsed + ".json", "r") as file:
                data = json.load(file)
            data[patchNoParsed] = patchData
            with open("/program/bank" + bankNoParsed + ".json", "w") as write:
                json.dump(data, write)
        else:
            print("Program Memory: INCORRECT TYPE FOR writePatch")
            print("patchNo: " + str(type(patchNo)) + "bankNo: " + str(type(bankNo)))
