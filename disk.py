import machine
import uos
import json

patch = "/program/patch.json"
default = "/program/default.json"
settings = "/data/settings.json"

def set_default(bank_no, patch_no):
    temp = {
        "patch": patch_no,
        "bank": bank_no
            }
    with open(default, "w") as file:
        json.dump(temp, file)

    print("default Patch/Bank Updated")

def read_default():
    with open(default, "r") as file:
        data = json.load(file)
        return data

def write_patch(bank_no, patch_no, patch_data):

    bank_no, patch_no, data = str(bank_no), str(patch_no), None

    with open(patch, "r") as file:
        data = json.load(file)

    data[bank_no][patch_no] = patch_data

    with open(patch, "w") as file:
        json.dump(data, file)

def read_bank(bank):
    with open(patch, "r") as file:
        data = json.load(file)
        return data[str(bank)]

def load_settings():
    with open(settings, "r") as file:
        data = json.load(file)
        return data

def save_settings(params):
    with open(settings, "w") as file:
        data = json.dump(params, file)
