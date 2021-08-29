class Mode:
    
    def __init__(self):
        self.value = "Program"
    
    def changeMode(self, newMode):
        self.value = newMode
        
    def returnValue(self):
        return self.value