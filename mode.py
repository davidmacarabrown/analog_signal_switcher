class Mode:
    
    def __init__(self):
        self.value = "Program"
    
    def change_mode(self, newMode):
        self.value = newMode
        
    def return_value(self):
        return self.value