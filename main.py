import time
import _thread
from machine import Pin
from memory import Memory
from instruction import Instruction
from program import ProgramMemory
from mode import Mode
import sdcard


ledList = [led1, led2, led3, led4, led5, writeLed]

buttonPad = 0.1
writeEnableTime = 2.5

def resetLeds():
    for leds in ledList:
        leds.value(0)

########################################## Registers

programMemory = ProgramMemory()
tempMemory = Memory()
instructionRegister = Instruction()

########################################### Starup

#startup
mode = Mode()

############################################
    
def interruptWrite(pin):
    writeSwitch.irq(handler = None)
    time.sleep(writeEnableTime)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual" or "Program":
            mode.changeMode("Write")
            print("++++ Executing in WRITE mode ++++")
            resetLeds()
            writeLed.value(1)
            time.sleep(0.5)
            writeSwitch.irq(handler = writeHandler)
            
            
def writeHandler(pin):
    writeSwitch.irq(handler = None)
    time.sleep(writeEnableTime)
    if pin.value() == 1:
        writeLed.toggle()
        time.sleep(0.3)
        writeLed.toggle()
        time.sleep(0.3)
        writeLed.toggle()
        time.sleep(0.3)
        writeLed.toggle()
        time.sleep(0.3)
        writeLed.toggle()
        time.sleep(0.3)
        print("---- Saving to Memory ----")
         
        location = tempMemory.getWriteLocation()
        patch = tempMemory.readAll()
        programMemory.writeToLocation(location, patch)
        instructionRegister.loadPatch(patch)   
        writeSwitch.irq(handler = interruptWrite)
        mode.changeMode("Program")
        instructionHandler()
        
    writeSwitch.irq(handler = interruptWrite)
     
def interruptMode(pin):

    modeSwitch.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual": ### Switching TO program mode
            mode.changeMode("Program")
            instructionRegister.clearAll()
            lastProgram = programMemory.readLastProgramUsed()
            #print("P Debug: Last Program", lastProgram)
            tempMemory.loadProgram(lastProgram)#load Last program to memory
            #print("P Debug: Memory Contents: ", tempMemory.contents)
            instructionRegister.loadPatch(tempMemory.readAll())
            #print("P Debug: Instruction Register: ", instructionRegister.contents)
            tempMemory.updateCurrentProgram(programMemory.getLastProgramUsed())
            #print("P Debug: Memory/CurrentProgram: ", tempMemory.currentProgram)
            instructionHandler()
            
            
        elif mode.returnValue() == "Program":
            mode.changeMode("Manual") ### Switching TO Manual mode
            print("Executing in Manual Mode")
#             tempMemory.updateCurrentProgram("0")
#             instructionRegister.loadPatch(tempMemory.contents)
#             instructionHandler()
            
        elif mode.returnValue() == "Write":
            mode.changeMode("Manual")
            
    modeSwitch.irq(handler = interruptMode)

def interruptOne(pin):
    
    instructionValue = 1
    programLocation = "1"
    
    switch1.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        
        if mode.returnValue() == "Manual":
            tempMemory.loadInstruction(instructionValue)
            instructionRegister.loadInstruction(1)
            instructionHandler()
        
        elif mode.returnValue() == "Program":
            if tempMemory.currentProgram == programLocation:
                pass
            else:
                programMemory.updateLastProgramUsed(programLocation)
                tempMemory.updateCurrentProgram("1")
                tempMemory.loadProgram(programMemory.contents[programLocation])
                instructionRegister.loadPatch(tempMemory.contents)
                instructionHandler()
            
        elif mode.returnValue() == "Write":
                tempMemory.updateWriteLocation("1")
                led1.toggle()
                time.sleep(0.3)
                led1.toggle()
            
    switch1.irq(handler = interruptOne)
    

        
switch1.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptOne)
# switch2.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptTwo)
# switch3.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptThree)
# switch4.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFour)
# switch5.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFive)

modeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptMode)
writeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptWrite)

def instructionHandler():

    print("Executing in ", mode.returnValue(), " mode")

    print("Instruction Register: ", instructionRegister.contents)
    print("Memory Register:      ", tempMemory.readAll())
    
    if mode.returnValue() == "Program":
        resetLeds()
    instructions = instructionRegister.contents
    
    for instruction in instructions:            
        
        if instruction == 1:
            led1.toggle()
            
        elif instruction == 2:
            led2.toggle()
                
        elif instruction == 3:
            led3.toggle()
                
        elif instruction == 4:
            led4.toggle()           

        elif instruction == 5:
            led5.toggle()
                
    instructionRegister.clearAll()
    
    print("Instruction Register: ", instructionRegister.contents)
    print("Memory Register:      ", tempMemory.contents)
    
def startUp():
    resetLeds()
    print("           +++Restarted+++")
      
    lastProgramUsed = programMemory.readLastProgramUsed()
    lastLocationUsed = programMemory.getLastProgramUsed()
    tempMemory.updateCurrentProgram(lastLocationUsed)
    
    print(lastProgramUsed, "last program used")
    tempMemory.loadProgram(lastProgramUsed)
    initialState = tempMemory.readAll()
    print(initialState, "tempMemory contents")
    instructionRegister.loadPatch(initialState)
    print(instructionRegister.contents, "instruction register")
    instructionHandler()
    
startUp()