import json
import uos

exampleData = {
                '1': [1,2,3,4,5],
                '2': [1,2,5],
                '3': [3,4,5]
        }



with open("/program/test.json", "w") as file:
    json.dump(exampleData, file)
    
with open("/program/test.json", "r") as file:
    json = json.load(file)