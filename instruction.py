class Instruction:
    
    def __init__(self):
        self.contents = []
        
    def load_one(self, instr):
        self.contents.append(instr)
            
    def load_patch(self, patch):
        self.contents.clear()
        for instruction in patch:
            self.contents.append(instruction)
            
    def clear(self):
        self.contents.clear()