import time
from machine import *

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

mode = "Manual"
    
def resetOutputs():
    for leds in ledList:
        leds.value(0)

########################################## Registers

resetOutputs()

lastProgramUsed = "A"

programRegister = {
                    "A" : [1, 3, 5],
                    "B" : [1, 2, 3],
                    "C" : [4, 5],
                    "D" : [1, 2],
                    "E" : []
                    }

memoryRegister = []
writeLocationAddressRegister = ""
instructionRegister = []

###########################################

def loadParameterToMemory(switchNumber):
    if memoryRegister.count(switchNumber) == 0:
        memoryRegister.append(switchNumber)
    else:
        memoryRegister.remove(switchNumber)
        
def writeToProgramRegister(location):
    programRegster[location] = memoryRegister
    global lastProgramUsed
    lastProgramUsed = location

def loadProgramToInstructionRegister(patch):
    program = programRegister[patch]
    for parameter in program:
        instructionRegister.append(parameter)
    
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
    
            instructionRegister.clear()
            loadProgramToInstructionRegister(lastProgramUsed) #later change to last used program
            global memoryRegister
            memoryRegister = instructionRegister
            
        elif mode == "Manual":
            instructionRegister.clear()
        print(mode + " Mode")
        instructionHandler()
    modeSwitch.irq(handler = interruptMode)

def interruptOne(pin):
    
    writeLocationKey = "A"
    instructionValue = 1
    
    switch1.irq(handler = None)
    time.sleep(buttonPad)
    
    if pin.value() == 1:
        global instructionRegister
        
        if mode == "Program":
            loadProgramToInstructionRegister(writeLocationKey)
            global lastProgramUsed
            lastProgramUsed = writeLocationKey
            global memoryRegister
            memoryRegister = instructionRegister
            
        else:
            instructionRegister.append(instructionValue)
            loadParameterToMemory(instructionValue)
            if mode == "Write":
                writeLocationAddressRegister = writeLocationKey
            
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
    print("Queued Instructions: ", instructionRegister)
    print("Memory Register: ", memoryRegister)
    
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