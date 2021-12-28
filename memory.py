class Memory:
    
    def __init__(self):
        self.mode = "program"
        self.patch = []
        self.bank = {}
        self.write_location = None
        self.current_bank = None
        self.current_patch = None
        
    def change_mode(self, newMode):
        self.mode = newMode
        
    def clear_all(self):
        self.patch.clear()
    
    def load_one(self, instruction):
        if self.patch.count(instruction) == 0:
            self.patch.append(instruction)
        elif self.patch.count(instruction) == 1:
            self.patch.remove(instruction)
            
    def load_patch(self, patch_address):
        self.patch = self.bank[str(patch_address)]
        
    def load_current_patch(self):
        self.patch = self.bank[str(self.current_patch)]
    
    def load_bank(self, bank):
        self.bank = bank

    def set_write_location(self, newAdd):
        self.write_location = newAdd
        
    def copy_write_location(self):
        self.current_patch = self.write_location
        
    def reset_write_location(self):
        self.write_location = None
    
    def set_current_patch(self, new):
        self.current_patch = new
    
    def set_current_bank(self, new):
        self.current_bank = new
        
    def increment_bank(self):
        if self.current_bank < 5:
            self.current_bank += 1
            self.current_patch = 1
        
    def decrement_bank(self):
        if self.current_bank > 1:
            self.current_bank -= 1
            self.current_patch = 1