import machine
import uos
import json
    
def set_default(bankNo, patchNo):
    
    tempDict = {
        "patch": patchNo,
        "bank": bankNo
            }
    with open("/program/default.json", "w") as file:
        json.dump(tempDict, file)
        
def load_default():
    
    with open("/program/default.json", "r") as file:
        data = json.load(file)
        return data
    
def load_patch(bankNo, patchNo):
    
    bankNo, patchNo, data = str(bankNo), str(patchNo), None
    
    with open(f"/program/bank{bankNo}.json", "r") as file:
        data = json.load(file)
    patch = data[patchNo]
    
    return patch
   
def write_patch(bankNo, patchNo, patchData):
    
    bankNo, patchNo, data = str(bankNo), str(patchNo), None
    
    with open(f"/program/bank{bankNo}.json", "r") as file:
        data = json.load(file)
        
    data[patchNo] = patchData
    with open(f"/program/bank{bankNo}.json", "w") as write:
        json.dump(data, write)
