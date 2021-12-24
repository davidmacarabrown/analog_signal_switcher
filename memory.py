class Memory:
    
    def __init__(self):
        self.contents = []
        self.write_location_address = None
        self.current_bank = None
        self.current_patch = None
        
    def clear_all(self):
        self.contents.clear()
    
    def load_one(self, instruction):
        if self.contents.count(instruction) == 0:
            self.contents.append(instruction)
        elif self.contents.count(instruction) == 1:
            self.contents.remove(instruction)
    
    def load_patch(self, instructions):
        self.clear_all()
        for instruction in instructions:
            self.contents.append(instruction)

    def set_write_location(self, newAdd):
        self.write_location_address = newAdd
        
    def reset_write_location(self):
        self.write_location_address = None
    
    def set_current_patch(self, new):
        self.current_patch = new
    
    def set_current_bank(self, new):
        self.current_bank = new
