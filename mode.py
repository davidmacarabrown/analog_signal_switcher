class Mode:
    
    def __init__(self, initialMode):
        self.value = initialMode
    
    def changeMode(self, newMode):
        self.value = newMode
        
    def returnValue(self):
        return self.value