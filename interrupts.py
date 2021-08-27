def interruptTwo(pin):
    
    instructionValue = 2
    
    switch2.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 2:
        global instructionRegister
        global lastProgramUsed
        
        if mode == "Program":
            lastProgramUsed = instructionValue
            memoryRegister.clear()
            loadProgramToMemory(instructionValue) #refactor to loadToMemory
            loadMemoryToInstructionRegister() #refactor to: instructionRegister = memoryRegister
            
        else: #if mode == "Manual"
            instructionRegister.append(instructionValue)
            if mode == "Write":
                writeLocationAddressRegister = instructionValue
            
        instructionHandler()
    switch2.irq(handler = interruptTwo)