import time
from machine import *
from " " import interrupts
import sys

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

lastProgramUsed = 1

programRegister = {
                    1 : [1, 3, 5],
                    2 : [1, 2, 3],
                    3 : [4, 5],
                    4 : [1, 2],
                    5 : []
                    }

memoryRegister = []
writeLocationAddressRegister = ""
instructionRegister = []

########################################### Starup

#startup
mode = "Program"

def printModeStatus():
    print("------------------------------------")
    print(mode + " Mode")

############################################

def loadParameterToMemory(switchNumber):
    if memoryRegister.count(switchNumber) == 0:
        memoryRegister.append(switchNumber)
    else:
        memoryRegister.remove(switchNumber)
        
def loadMemoryToInstructionRegister():
    for page in memoryRegister:
        instructionRegister.append(page)
        
        
def writeToProgramRegister(location):
    programRegister[location] = memoryRegister
    global lastProgramUsed
    lastProgramUsed = location

def loadProgramToMemory(patch):
    program = programRegister[patch]
    for parameter in program:
        memoryRegister.append(parameter)
    
def interruptWrite(pin):
    global mode
    writeSwitch.irq(handler = None)
    
    time.sleep(writeEnableTime)
    
    if pin.value() == 1:
        writeLed.toggle()
        if mode == "Program" or "Manual":
            mode = "Write"
            print(mode + " Mode")
        
        if mode == "Write":
            writeToProgramRegister(writeLocationAddressRegister)
            mode == "Program"
            
            
    writeSwitch.irq(handler = interruptWrite)
    
def interruptMode(pin):
    global mode
    global instructionRegister
    global programRegister
    
    modeSwitch.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        if mode == "Manual":
            mode = "Program"
            instructionRegister.clear()
            loadProgramToInstructionRegister(lastProgramUsed) #later change to last used program
            global memoryRegister
            memoryRegister = instructionRegister
            
        elif mode == "Program":
            mode = "Manual"

            loadProgramToMemory(lastProgramUsed) #later change to last used program
            global memoryRegister
            loadMemoryToInstructionRegister()
            instructionHandler()
            
        elif mode == "Manual":
            instructionRegister.clear()
        printModeStatus()
        instructionHandler()
    modeSwitch.irq(handler = interruptMode)

def interruptOne(pin):
    
    instructionValue = 1
    
    switch1.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
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
    print("Instruction Register: ", instructionRegister)
    print("------------------------------------")
    print("Memory Register:      ", memoryRegister)
    
    if mode == "Program":
        resetOutputs()
            
    for instruction in instructionRegister:            
        
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
                
    instructionRegister.clear()
    
def startUp():
    memoryRegister.clear()
    resetOutputs()
    time.sleep(1)
    print("+++Restarted+++")
    loadProgramToMemory(lastProgramUsed)
    loadMemoryToInstructionRegister()
    instructionHandler()
    printModeStatus()
    
startUp()