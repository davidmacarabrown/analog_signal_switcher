import time
from machine import *

led1 = machine.Pin(0, machine.Pin.OUT)
led2 = machine.Pin(1, machine.Pin.OUT)
led3 = machine.Pin(2, machine.Pin.OUT)
led4 = machine.Pin(3, machine.Pin.OUT)
led5 = machine.Pin(4, machine.Pin.OUT)

switch1 = machine.Pin(20, machine.Pin.IN, Pin.PULL_DOWN)
switch2 = machine.Pin(19, machine.Pin.IN, Pin.PULL_DOWN)
switch3 = machine.Pin(18, machine.Pin.IN, Pin.PULL_DOWN)
switch4 = machine.Pin(17, machine.Pin.IN, Pin.PULL_DOWN)
switch5 = machine.Pin(16, machine.Pin.IN, Pin.PULL_DOWN)

modeSwitch = machine.Pin(21, machine.Pin.IN, Pin.PULL_DOWN)

ledList = [led1, led2, led3, led4, led5]

mode = False
    
def resetLeds():
    for leds in ledList:
        leds.value(0)

resetLeds()


programRegister = [1, 3, 5] #placeholder program
instructionRegister = []

def loadProgramToInstructionRegister():
    for parameter in programRegister:
        instructionRegister.append(parameter)

def interruptMode(pin):
    global mode
    global instructionRegister
    global programRegister
    
    modeSwitch.irq(handler = None)
    time.sleep(0.06)
    modeSwitch.irq(handler = interruptMode) #disabling interrupts needs refactored?
    
    if pin.value() == 1:
        print(pin)
        if mode == False:
            mode = not mode
        elif mode == True:
            mode = not mode
        modeStatus = ""
        if mode == True:
            modeStatus = "Program"
            loadProgramToInstructionRegister()
        elif mode == False:
            modeStatus = "Manual"
        print("Mode: " + modeStatus)
        instructionHandler()

def interruptOne(pin):
    switch1.irq(handler = None)
    time.sleep(0.06)
    switch1.irq(handler = interruptOne)
    
    if pin.value() == 1:
        interruptPin = pin
        print(pin)
        global instructionRegister
        instructionRegister.append(1)
        instructionHandler()
        print("Input 1")
    
def interruptTwo(pin):
    switch2.irq(handler = None)
    time.sleep(0.06)
    switch2.irq(handler = interruptTwo)
    
    if pin.value() == 1:
        global instructionRegister
        instructionRegister.append(2)
        instructionHandler()
        print("Input 2")
    
def interruptThree(pin):
    switch3.irq(handler = None)
    time.sleep(0.06)
    switch3.irq(handler = interruptThree)
    
    if pin.value() == 1:
        global instructionRegister
        instructionRegister.append(3)
        instructionHandler()
        print("Input 3")
    
def interruptFour(pin):
    switch4.irq(handler = None)
    time.sleep(0.06)
    switch4.irq(handler = interruptFour)
    
    if pin.value() == 1:
        global instructionRegister
        instructionRegister.append(4)
        instructionHandler()
        print("Input 4")
    
def interruptFive(pin):
    switch5.irq(handler = None)
    time.sleep(0.06)
    switch5.irq(handler = interruptFive)
    
    if pin.value() == 1:
        global instructionRegister
        instructionRegister.append(5)
        instructionHandler()
        print("Input 5")
    
switch1.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptOne)
switch2.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptTwo)
switch3.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptThree)
switch4.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFour)
switch5.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptFive)

modeSwitch.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptMode)

def instructionHandler():
    
    for instruction in instructionRegister:
                
        if instruction == 1:
            if mode == True:
                led1.toggle()
                time.sleep(0.1)
                led1.toggle()
            else:
                led1.toggle()
            
        if instruction == 2:
            if mode == True:
                led2.toggle()
                time.sleep(0.1)
                led2.toggle()
            else:
                led2.toggle()
        
        if instruction == 3:
            if mode == True:
                led3.toggle()
                time.sleep(0.1)
                led3.toggle()
            else:
                led3.toggle()
        
        if instruction == 4:
            if mode == True:
                led4.toggle()
                time.sleep(0.1)
                led4.toggle()
            else:
                led4.toggle()

        if instruction == 5:
            if mode == True:
                led5.toggle()
                time.sleep(0.1)
                led5.toggle()
            else:
                led5.toggle()
            
    instructionRegister.clear()
            

            