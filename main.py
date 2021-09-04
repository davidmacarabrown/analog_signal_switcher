import time
import _thread
from machine import Pin
from memory import Memory
from indicator_leds import IndicatorLeds
from relay_output import RelayOutput
from instruction import Instruction
from program import ProgramMemory
from mode import Mode


#################################################### BUTTONS
switch1 = machine.Pin(20, machine.Pin.IN, Pin.PULL_DOWN)
switch2 = machine.Pin(19, machine.Pin.IN, Pin.PULL_DOWN)
switch3 = machine.Pin(18, machine.Pin.IN, Pin.PULL_DOWN)
switch4 = machine.Pin(17, machine.Pin.IN, Pin.PULL_DOWN)
switch5 = machine.Pin(16, machine.Pin.IN, Pin.PULL_DOWN)
writeSwitch = machine.Pin(22, machine.Pin.IN, Pin.PULL_DOWN)
modeSwitch = machine.Pin(21, machine.Pin.IN, Pin.PULL_DOWN)
#################################################### RELAY OUTPUTS
relays = RelayOutput()

relays.outputs[1] = machine.Pin(6, machine.Pin.OUT)
relays.outputs[2] = machine.Pin(7, machine.Pin.OUT)
relays.outputs[3] = machine.Pin(8, machine.Pin.OUT)
relays.outputs[4] = machine.Pin(9, machine.Pin.OUT)
relays.outputs[5] = machine.Pin(28, machine.Pin.OUT)

buttonPad = 0.1
writeEnableTime = 2.5
##################################################### INDICATOR LED
leds = IndicatorLeds()

leds.allLeds[1] = machine.Pin(4, machine.Pin.OUT)
leds.allLeds[2] = machine.Pin(3, machine.Pin.OUT)
leds.allLeds[3] = machine.Pin(2, machine.Pin.OUT)
leds.allLeds[4] = machine.Pin(1, machine.Pin.OUT)
leds.allLeds[5] = machine.Pin(0, machine.Pin.OUT)

leds.allLeds["write"] = machine.Pin(5, machine.Pin.OUT)

################################################# Registers

programMemory = ProgramMemory()
tempMemory = Memory()
instructionRegister = Instruction()

########################################### Starup

mode = Mode()

############################################
    
def interruptWrite(pin):
    writeSwitch.irq(handler = None)
    time.sleep(writeEnableTime)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual" or "Program":
            mode.changeMode("Write")
            print("++++ Executing in WRITE mode ++++")
            leds.resetAll()
            leds.toggleOne("write")
            time.sleep(0.5)
            writeSwitch.irq(handler = writeHandler)
            
            
def writeHandler(pin):
    writeSwitch.irq(handler = None)
    time.sleep(writeEnableTime)
    if pin.value() == 1:
        fl = 0
        while fl < 13:
            leds.toggleOne("write")
            time.sleep(0.3)
            leds.toggleOne("write")
            fl += 1
        
        print("---- Saving to Memory ----")
         
        location = tempMemory.getWriteLocation()
        programMemory.setDefaultProgram(location)
        patch = tempMemory.readAll()
        programMemory.writeToDisk(location, patch)
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
            toLoad = programMemory.loadLastProgramUsed()
            tempMemory.loadProgram(toLoad)
            instructionRegister.loadPatch(tempMemory.readAll())
            tempMemory.updateCurrentProgram(programMemory.getLastProgramUsed())
            instructionHandler()
            
            
        elif mode.returnValue() == "Program":
            mode.changeMode("Manual") ### Switching TO Manual mode
            print("Executing in Manual Mode")
            instructionRegister.loadPatch(tempMemory.contents)
            instructionHandler()
            
        elif mode.returnValue() == "Write":
            mode.changeMode("Manual")
            
    modeSwitch.irq(handler = interruptMode)

def interruptOne(pin):
    
    instructionValue = 1
    
    switch1.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        
        if mode.returnValue() == "Manual":
            tempMemory.loadInstruction(instructionValue)
            instructionRegister.loadInstruction(instructionValue)
            instructionHandler()
        
        elif mode.returnValue() == "Program":
            if tempMemory.currentProgram == str(instructionValue):
                pass
            else:
                programMemory.updateLastProgramUsed(instructionValue)
                tempMemory.updateCurrentProgram(instructionValue)
                tempMemory.loadProgram(programMemory.loadFromDisk(instructionValue))
                instructionRegister.loadPatch(tempMemory.contents)
                instructionHandler()
            
        elif mode.returnValue() == "Write":
                tempMemory.updateWriteLocation(instructionValue)
                leds.toggleOne(instructionValue)
                time.sleep(0.3)
                leds.toggleOne(instructionValue)
            
    switch1.irq(handler = interruptOne)
    

        
switch1.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptOne)
# switch2.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptTwo)
# switch3.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptThree)
# switch4.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFour)
# switch5.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFive)

modeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptMode)
writeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptWrite)

def instructionHandler():
    print("--------------------------------")
    print("Executing in ", mode.returnValue(), " mode")
    print("--------------------------------")
    print("Instruction Register: ", instructionRegister.contents)
    print("Memory Register:      ", tempMemory.readAll())
    
    if mode.returnValue() == "Program":
        leds.resetAll()
        relays.resetAll()
        currentProgram = tempMemory.getCurrentProgram()
    instructions = instructionRegister.read()
    
    leds.toggleMultiple(instructions)
    relays.latchPatch(instructions)
                
    instructionRegister.clearAll()
    print("--------------------------------")
    print("Instruction Register: ", instructionRegister.contents)
    print("Memory Register:      ", tempMemory.contents)
    
def startUp():
    leds.resetAll()
    relays.resetAll()
    print("           +++Restarted+++")
    print("--------------------------------")
    
    default = programMemory.readDefaultProgram()
    startupPatch = programMemory.loadFromDisk(default)
    tempMemory.loadProgram(startupPatch)
    tempMemory.updateCurrentProgram(default)
    
    print("--------------------------------")
    
    print(startupPatch, "last program used")
    initialState = tempMemory.readAll()
    print(initialState, "tempMemory contents")
    instructionRegister.loadPatch(initialState)
    print(instructionRegister.contents, "instruction register")
    instructionHandler()
    
startUp()