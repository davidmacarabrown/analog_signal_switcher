import time
from machine import Pin
from memory import Memory
from indicator_leds import IndicatorLeds
from relay_output import RelayOutput
from instruction import Instruction
from program_memory import ProgramMemory
from mode import Mode
#####################################################

#TODO:

    #[DOING] work on interrupt handling for other buttons
    # possibly rework instructionHandler to call the read operations in program mode, move them away from the interrupt "program" mode
    # make json files for as many banks as I think there will be, or figure out checks if the bank exists, and if not create new file?
    # add functionality to mode button to cycle through banks, or add other buttons for this... other buttons probably neater, plenty of i/o pins left - "bank select" as a mode?
    # work on display functionality
    # basically debug anything that breaks which will probably be... everything???


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

##################################################### INDICATOR LEDS
leds = IndicatorLeds()

leds.allLeds[1] = machine.Pin(4, machine.Pin.OUT)
leds.allLeds[2] = machine.Pin(3, machine.Pin.OUT)
leds.allLeds[3] = machine.Pin(2, machine.Pin.OUT)
leds.allLeds[4] = machine.Pin(1, machine.Pin.OUT)
leds.allLeds[5] = machine.Pin(0, machine.Pin.OUT)

leds.allLeds["write"] = machine.Pin(5, machine.Pin.OUT)

################################################# OBJECTS

programMemory = ProgramMemory()
tempMemory = Memory()
instructionRegister = Instruction()
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
        patchAddress = tempMemory.getWriteLocation()
        bankAddress = tempMemory.getCurrentBank()
        patch = tempMemory.readAll()
        
        programMemory.writePatch(bankAddress, patchAddress, patch)
        programMemory.setDefaultPatch(bankAddress, patchAddress)
        instructionRegister.loadPatch(patch)  
        fl = 0
        while fl < 4:
            leds.toggleOne("write")
            time.sleep(0.1)
            leds.toggleOne("write")
            time.sleep(0.1)
            
            fl += 1
        
        print("---- Saving to Memory ----")
         
        tempMemory.resetWriteLocation()
        mode.changeMode("Program")
        time.sleep(0.1)
        instructionHandler()
        
    writeSwitch.irq(handler = interruptWrite)
     
def interruptMode(pin):

    modeSwitch.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual":       ### Switching TO program mode
            
            mode.changeMode("Program")
            instructionRegister.clearAll()
            
            toLoad = programMemory.loadPatch(tempMemory.getCurrentBank(), tempMemory.getCurrentPatch())
            
            tempMemory.loadPatch(toLoad)
            instructionRegister.loadPatch(tempMemory.readAll())
            instructionHandler()
            
            
        elif mode.returnValue() == "Program":
            mode.changeMode("Manual")            ### Switching TO Manual mode
            print("Manual Mode")
            
        elif mode.returnValue() == "Write":
            mode.changeMode("Manual")
            
    modeSwitch.irq(handler = interruptMode)

def interruptHandler(instructionValue):
    
    print(type(instructionValue), instructionValue)
        
    if mode.returnValue() == "Manual":
        tempMemory.loadInstruction(instructionValue)
        instructionRegister.loadInstruction(instructionValue)
        instructionHandler()
        
    elif mode.returnValue() == "Program":
        if tempMemory.getCurrentPatch() == instructionValue:
            pass
        else:
            currentBank = tempMemory.getCurrentBank()
            programMemory.setDefaultPatch(currentBank, instructionValue)
            tempMemory.updateCurrentPatch(instructionValue)
            toLoad = programMemory.loadPatch(currentBank,instructionValue)
            tempMemory.loadPatch(toLoad)
            instructionRegister.loadPatch(tempMemory.contents)
            instructionHandler()
            
    elif mode.returnValue() == "Write":
            tempMemory.updateWriteLocation(instructionValue)
            leds.toggleOne(instructionValue)
            time.sleep(0.3)
            leds.toggleOne(instructionValue)
            print("Write location Bank: " + str(tempMemory.getCurrentBank()) + " Patch: " + str(tempMemory.getWriteLocation()) + " selected.") 

def intOne(pin):
    pinValue = 1
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interruptHandler(pinValue)
    pin.irq(handler = intOne)

def intTwo(pin):
    pinValue = 2
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interruptHandler(pinValue)
    pin.irq(handler = intTwo)

def intThree(pin):
    pinValue = 3
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interruptHandler(pinValue)
    pin.irq(handler = intThree)

def intFour(pin):
    pinValue = 4
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interruptHandler(pinValue)
    pin.irq(handler = intFour)

def intFive(pin):
    pinValue = 5
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interruptHandler(pinValue)
    pin.irq(handler = intFive)


switch1.irq(trigger=machine.Pin.IRQ_RISING, handler=intOne)
switch2.irq(trigger=machine.Pin.IRQ_RISING, handler=intTwo)
switch3.irq(trigger=machine.Pin.IRQ_RISING, handler=intThree)
switch4.irq(trigger=machine.Pin.IRQ_RISING, handler=intFour)
switch5.irq(trigger=machine.Pin.IRQ_RISING, handler=intFive)

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
    
    defaultData = programMemory.loadDefaultPatch()
    defaultBank = defaultData["bank"]
    defaultPatch = defaultData["patch"]
    
    startPatch = programMemory.loadPatch(defaultBank, defaultPatch)
    
    tempMemory.loadPatch(startPatch)
    tempMemory.updateCurrentPatch(defaultPatch)
    tempMemory.updateCurrentBank(defaultBank)
    
    print("--------------------------------")
    
    print(startPatch, "last program used")
    initialState = tempMemory.readAll()
    print(initialState, "tempMemory contents")
    instructionRegister.loadPatch(initialState)
    print(instructionRegister.contents, "instruction register")
    instructionHandler()
    
startUp()