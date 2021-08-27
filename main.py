import time
from machine import Pin
from memory import Memory
from instruction import Instruction
from modeStatus import printModeStatus
from program import ProgramMemory
from mode import Mode

led1 = machine.Pin(0, machine.Pin.OUT)
led2 = machine.Pin(1, machine.Pin.OUT)
led3 = machine.Pin(2, machine.Pin.OUT)
led4 = machine.Pin(3, machine.Pin.OUT)
led5 = machine.Pin(4, machine.Pin.OUT)

writeLed = machine.Pin(5, machine.Pin.OUT)

switch1 = machine.Pin(20, machine.Pin.IN, Pin.PULL_DOWN)
switch2 = machine.Pin(19, machine.Pin.IN, Pin.PULL_DOWN)
switch3 = machine.Pin(18, machine.Pin.IN, Pin.PULL_DOWN)
switch4 = machine.Pin(17, machine.Pin.IN, Pin.PULL_DOWN)
switch5 = machine.Pin(16, machine.Pin.IN, Pin.PULL_DOWN)

modeSwitch = machine.Pin(21, machine.Pin.IN, Pin.PULL_DOWN)
writeSwitch = machine.Pin(22, machine.Pin.IN, Pin.PULL_DOWN)

ledList = [led1, led2, led3, led4, led5, writeLed]

buttonPad = 0.1
writeEnableTime = 2.5

def resetOutputs():
    for leds in ledList:
        leds.value(0)

########################################## Registers

programMemory = ProgramMemory()
tempMemory = Memory()
instructionRegister = Instruction()

########################################### Starup

#startup
mode = Mode("Program")

############################################
    
def interruptWrite(pin):
    writeSwitch.irq(handler = None)
    
    time.sleep(writeEnableTime)
    
    if pin.value() == 1:
        writeLed.toggle()
        if mode.returnValue() != "Write":
            mode.changeMode("Write")
            print("Write Mode")
        
        if mode.returnValue() == "Write": #in write mode, holding the write button writes from the memory to the programMemory at the writeLocation in temporary Memory
            programMemory.writeToLocation(tempMemory.getWriteLocation, tempMemory.readAll())
            mode.changeMode("Program")
              
    writeSwitch.irq(handler = interruptWrite)
    
def interruptMode(pin):

    modeSwitch.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual": ### Switching TO program mode
            mode.changeMode("Program")
            instructionRegister.clear()
            tempMemory.loadInstruction(programMemory.readFromLocation(programMemory.getLastProgramUsed()))#load Last program to memory
            instructionRegister.loadPatch(tempMemory.readAll)
            
        elif mode.returnValue() == "Program":
            mode.changeMode("Manual")

            #switching TO manual
            instructionRegister.loadPatch(tempMemory.readAll)
            instructionHandler()
            
        elif mode.returnValue() == "Write":
            mode.changeMode("Manual")
            
    modeSwitch.irq(handler = interruptMode)

def interruptOne(pin):
    
    instructionValue = 1 #can later refactor to concat the bank ?
    
    switch1.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        
        if mode.returnValue() == "Program":
            programMemory.updateLastProgramUsed(instructionValue) #REFACTOR LATER TO INCLUDE BANK LETTER AS WELL AS PATCH NO
            memoryRegister.clear()
            tempMemory.loadProgram(programMemory.getLastProgramUsed) #refactor to loadToMemory
            loadMemoryToInstructionRegister() #refactor to: instructionRegister = memoryRegister
            
        else: #if mode == "Manual"
            instructionRegister.loadInstruction(instructionValue)
            if mode.returnValue() == "Write":
                tempMemory.updateWriteLocation(instructionValue)
            
        instructionHandler()
    switch1.irq(handler = interruptOne)
    

        
switch1.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptOne)
# switch2.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptTwo)
# switch3.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptThree)
# switch4.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFour)
# switch5.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFive)

modeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptMode)
writeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptWrite)

def instructionHandler():
    print("------------------------------------")
    print("Instruction Register: ", instructionRegister.read())
    print("------------------------------------")
    print("Memory Register:      ", tempMemory.readAll())
    
    if mode == "Program":
        resetOutputs()
            
    for instruction in instructionRegister.read():            
        
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
    
def startUp():
    tempMemory.clearAll()
    resetOutputs()
    time.sleep(1)
    print("+++Restarted+++")
    print("------------------------------------")
    
    defaultProgram = programMemory.readLastProgramUsed()
    startUpProgram = programMemory.readFromLocation(defaultProgram)
    tempMemory.loadProgram(startUpProgram)
    patch = tempMemory.readAll()
    instructionRegister.loadPatch(patch)
    
    print(instructionRegister.read())
    instructionHandler()
    print(mode.returnValue())
    
startUp()