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

    # [DOING] work on interrupt handling for other buttons
    # possibly rework instruction_handler to call the read operations in program mode, move them away from the interrupt "program" mode
    # make json files for as many banks as I think there will be, or figure out checks if the bank exists, and if not create new file?
    # add functionality to mode button to cycle through banks, or add other buttons for this... other buttons probably neater, plenty of i/o pins left - "bank select" as a mode?
    # [DOING] work on display functionality
    # basically debug anything that breaks which will probably be... everything???

# Object Setup

program_memory = ProgramMemory()
temp_memory = Memory()
instruction_register = Instruction()
mode = Mode()
inputs = Switches()
relays = RelayOutput()
leds = IndicatorLeds()
display = Display()

# Time and button padding for de-bounce
button_pad = 0.1
write_pad = 2

# Interrupt Definitions
def interrupt_write(pin):
    inputs.switches["write"].irq(handler = None)
    time.sleep(write_pad)
    
    if pin.value() == 1:
        if mode.return_value() == "Manual" or "Program":
            mode.change_mode("Write")
            display.clear()
            display.update_mode(mode.return_value())
            display.refresh()
            leds.reset_all()
            leds.toggle(6)
            time.sleep(0.5)
    inputs.switches["write"].irq(handler = write_handler)
            
def write_handler(pin):
        
    inputs.switches["write"].irq(handler = None)
    time.sleep(write_pad)
            
    if pin.value() == 1:
        if temp_memory.get_write_location():
            patch_address = temp_memory.get_write_location()
            bank_address = temp_memory.get_current_bank()
            patch = temp_memory.read_all()
            
            program_memory.write_patch(bank_address, patch_address, patch)
            program_memory.set_default(bank_address, patch_address)
            instruction_register.load_patch(patch)
            display.clear()
            display.update_line_one(">> Saving...")
            display.update_line_two("> " + str(patch_address))
            display.refresh()

            leds.rapid_blink(6)
            temp_memory.reset_write_location()
            mode.change_mode("Program")
            display.clear()
            time.sleep(0.1)
            instruction_handler()
            
            inputs.switches["write"].irq(handler = interrupt_write)
        else:
            display.clear()
            display.update_line_one("Select Location")
            display.update_line_two("Mode > Exit")
            display.refresh()
            time.sleep(1.5)
            
            inputs.switches["write"].irq(handler = write_handler)
            display.clear()
            display.update_mode(mode.return_value())
            display.refresh()
     
def interrupt_mode(pin):

    inputs.switches["mode"].irq(handler = None)
    time.sleep(button_pad)
    
    if pin.value() == 1:
        display.clear()
        
        #entering program mode
        if mode.return_value() == "Manual": 
            
            mode.change_mode("Program")
            instruction_register.clear()
            inputs.switches["write"].irq(handler = None)
            to_load = program_memory.load_patch(temp_memory.get_current_bank(), temp_memory.get_current_patch())
            
            temp_memory.load_patch(to_load)
            instruction_register.load_patch(temp_memory.read_all())
            instruction_handler()
            
            display.update_bank(temp_memory.get_current_bank())
        
        #entering manual mode
        elif mode.return_value() == "Program":
            mode.change_mode("Manual")
            inputs.switches["write"].irq(handler = interrupt_write)
        #exiting write mode
        elif mode.return_value() == "Write":
            mode.change_mode("Manual")
            inputs.switches["write"].irq(handler = interrupt_write)
            leds.reset_all()
            temp_memory.reset_write_location()
            instruction_register.load_patch(temp_memory.read_all())
            instruction_handler()
            
    display.update_mode(mode.return_value())
    display.refresh()
    inputs.switches["mode"].irq(handler = interrupt_mode)

def interrupt_handler(instruction_value):
        
    if mode.return_value() == "Manual":
        temp_memory.load_one(instruction_value)
        instruction_register.load_one(instruction_value)
        instruction_handler()
        
    elif mode.return_value() == "Program":
        if temp_memory.get_current_patch() == instruction_value:
            pass
        else:
            current_bank = temp_memory.get_current_bank()
            
            program_memory.set_default(current_bank, instruction_value)
            temp_memory.set_current_patch(instruction_value)
            to_load = program_memory.load_patch(current_bank,instruction_value)
            temp_memory.load_patch(to_load)
            instruction_register.load_patch(temp_memory.contents)
            display.update_patch(temp_memory.get_current_patch())
            instruction_handler()
            
    elif mode.return_value() == "Write":
            temp_memory.set_write_location(instruction_value)
            display.update_line_two("Location: " + str(instruction_value))
            display.refresh()
            leds.toggle(instruction_value)
            time.sleep(0.3)
            leds.toggle(instruction_value)

def int_one(pin):
    pin_value = 1
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interrupt_handler(pin_value)
    pin.irq(handler = int_one)

def int_two(pin):
    pin_value = 2
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interrupt_handler(pin_value)
    pin.irq(handler = int_two)

def int_three(pin):
    pin_value = 3
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interrupt_handler(pin_value)
    pin.irq(handler = int_three)

def int_four(pin):
    pin_value = 4
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interrupt_handler(pin_value)
    pin.irq(handler = int_four)

def int_five(pin):
    pin_value = 5
    pin.irq(handler = None)
    time.sleep(0.1)
    if pin.value() == 1:
        interrupt_handler(pin_value)
    pin.irq(handler = int_five)

# Interrupt triggers
inputs.switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=int_one)
inputs.switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=int_two)
inputs.switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=int_three)
inputs.switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=int_four)
inputs.switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=int_five)
inputs.switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)
# inputs.switches["write"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_write)

debug = False

def instruction_handler():
    if debug:
        print("--------------------------------")
        print("Executing in ", mode.return_value(), " mode")
        print("--------------------------------")
        print("Instruction Register: ", instruction_register.contents)
        print("Memory Register:      ", temp_memory.read_all())
    
    if mode.return_value() == "Program":
        leds.reset_all()
        relays.reset()
        display.clear()
        display.update_mode(mode.return_value())
        display.update_bank(temp_memory.get_current_bank())
        display.update_patch(temp_memory.get_current_patch())
        display.refresh()
        
    leds.toggle_multi(instruction_register.read())
    relays.latch_multi(instruction_register.read())
                
    instruction_register.clear()
    
    if debug:
        print("--------------------------------")
        print("Instruction Register: ", instruction_register.contents)
        print("Memory Register:      ", temp_memory.contents)
        
def start_up():
    leds.reset_all()
    relays.reset()
    display.clear()
    display.update_line_one("Starting...")
    display.refresh()
    time.sleep(1)
    
    default_data = program_memory.load_default()
    default_bank = default_data["bank"]
    default_patch = default_data["patch"]
    
    start_patch = program_memory.load_patch(default_bank, default_patch)
    
    temp_memory.load_patch(start_patch)
    temp_memory.set_current_patch(default_patch)
    temp_memory.set_current_bank(default_bank)

    instruction_register.load_patch(temp_memory.read_all())
    instruction_handler()

if __name__  == '__main__':
    start_up()