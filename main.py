import time
from machine import Pin, I2C
from memory import Memory
from indicator_leds import IndicatorLeds
from relay_output import RelayOutput
from instruction import Instruction
from program_memory import ProgramMemory
from mode import Mode
from display import Display
from switches import Switches

#TODO:

    #[DOING] work on interrupt handling for other buttons
    # possibly rework instructionHandler to call the read operations in program mode, move them away from the interrupt "program" mode
    # make json files for as many banks as I think there will be, or figure out checks if the bank exists, and if not create new file?
    # add functionality to mode button to cycle through banks, or add other buttons for this... other buttons probably neater, plenty of i/o pins left - "bank select" as a mode?
    # [DOING] work on display functionality
    # basically debug anything that breaks which will probably be... everything???

# Object Setup

programMemory = ProgramMemory()
tempMemory = Memory()
instructionRegister = Instruction()
mode = Mode()
inputs = Switches()
relays = RelayOutput()
leds = IndicatorLeds()
display = Display()

# Time and button padding for de-bounce
buttonPad = 0.1
writeEnableTime = 2.5

# Interrupt Definitions
    
def interruptWrite(pin):
    inputs.switches["write"].irq(handler = None)
    time.sleep(writeEnableTime)
    
    if pin.value() == 1:
        if mode.returnValue() == "Manual" or "Program":
            mode.changeMode("Write")
            display.clear()
            display.update_mode(mode.returnValue())
            display.refresh()
            leds.resetAll()
            leds.toggleOne(6)
            time.sleep(0.5)
    inputs.switches["write"].irq(handler = writeHandler)
            
def writeHandler(pin):
        
    inputs.switches["write"].irq(handler = None)
    time.sleep(writeEnableTime)
            
    if pin.value() == 1:
        patchAddress = tempMemory.getWriteLocation()
        bankAddress = tempMemory.getCurrentBank()
        patch = tempMemory.readAll()
        
        programMemory.writePatch(bankAddress, patchAddress, patch)
        programMemory.setDefaultPatch(bankAddress, patchAddress)
        instructionRegister.loadPatch(patch)
        display.clear()
        display.update_line_one(">> Saving...")
        display.refresh()

        leds.rapidBlink(6)
        tempMemory.resetWriteLocation()
        mode.changeMode("Program")
        display.clear()
        time.sleep(0.1)
        instructionHandler()
        
        inputs.switches["write"].irq(handler = interruptWrite)
     
def interruptMode(pin):

    inputs.switches["mode"].irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        display.clear()
        
        #entering program mode
        if mode.returnValue() == "Manual":       ### Switching TO program mode
            
            mode.changeMode("Program")
            instructionRegister.clearAll()
            
            toLoad = programMemory.loadPatch(tempMemory.getCurrentBank(), tempMemory.getCurrentPatch())
            
            tempMemory.loadPatch(toLoad)
            instructionRegister.loadPatch(tempMemory.readAll())
            instructionHandler()
            
            display.update_bank(tempMemory.getCurrentBank())
        
        #entering manual mode
        elif mode.returnValue() == "Program":
            mode.changeMode("Manual")
        
        #exiting write mode
        elif mode.returnValue() == "Write":
            mode.changeMode("Manual")
            inputs.switches["write"].irq(handler = interruptWrite)
            leds.resetAll()
            tempMemory.resetWriteLocation()
            instructionRegister.loadPatch(tempMemory.readAll())
            instructionHandler()
            
    display.update_mode(mode.returnValue())
    display.refresh()
    inputs.switches["mode"].irq(handler = interruptMode)

def interruptHandler(instructionValue):
        
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
            display.update_patch(tempMemory.getCurrentPatch())
            instructionHandler()
            
    elif mode.returnValue() == "Write":
            tempMemory.updateWriteLocation(instructionValue)
            leds.toggleOne(instructionValue)
            time.sleep(0.3)
            leds.toggleOne(instructionValue)

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

# Interrupt triggers

inputs.switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=intOne)
inputs.switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=intTwo)
inputs.switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=intThree)
inputs.switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=intFour)
inputs.switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=intFive)
inputs.switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interruptMode)
inputs.switches["write"].irq(trigger=machine.Pin.IRQ_RISING, handler=interruptWrite)

debug = False

def instructionHandler():
    if debug:
        print("--------------------------------")
        print("Executing in ", mode.returnValue(), " mode")
        print("--------------------------------")
        print("Instruction Register: ", instructionRegister.contents)
        print("Memory Register:      ", tempMemory.readAll())
    
    if mode.returnValue() == "Program":
        leds.resetAll()
        relays.resetAll()
        display.clear()
        display.update_mode(mode.returnValue())
        display.update_bank(tempMemory.getCurrentBank())
        display.update_patch(tempMemory.getCurrentPatch())
        display.refresh()
        
    leds.toggleMultiple(instructionRegister.read())
    relays.latchPatch(instructionRegister.read())
                
    instructionRegister.clearAll()
    
    if debug:
        print("--------------------------------")
        print("Instruction Register: ", instructionRegister.contents)
        print("Memory Register:      ", tempMemory.contents)
        
def startUp():
    leds.resetAll()
    relays.resetAll()
    display.clear()
    display.update_line_one("Starting...")
    display.refresh()
    time.sleep(1)
    
    defaultData = programMemory.loadDefaultPatch()
    defaultBank = defaultData["bank"]
    defaultPatch = defaultData["patch"]
    
    startPatch = programMemory.loadPatch(defaultBank, defaultPatch)
    
    tempMemory.loadPatch(startPatch)
    tempMemory.updateCurrentPatch(defaultPatch)
    tempMemory.updateCurrentBank(defaultBank)

    instructionRegister.loadPatch(tempMemory.readAll())
    instructionHandler()

startUp()
