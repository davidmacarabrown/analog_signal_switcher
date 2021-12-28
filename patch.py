import machine
import uos
import json

path = "/program/patch.json"
default = "/program/default.json"
    
def set_default(bank_no, patch_no):
    
    temp = {
        "patch": patch_no,
        "bank": bank_no
            }
    with open(default, "w") as file:
        json.dump(temp, file)
        
def read_default():
    
    with open(default, "r") as file:
        data = json.load(file)
        return data
   
def write_patch(bank_no, patch_no, patch_data):
    
    bank_no, patch_no, data = str(bank_no), str(patch_no), None
    
    with open(path, "r") as file:
        data = json.load(file)
        
    data[bank_no][patch_no] = patch_data
    
    with open(path, "w") as write:
        json.dump(data, write)
    
def read_bank(bank):
    with open(path, "r") as file:
        data = json.load(file)
        return data[str(bank)]
