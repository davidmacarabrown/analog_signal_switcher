import time
import gc
import _thread
from machine import Pin, I2C

from memory import Memory
from display import Display

import patch as p_mem
import indicators as leds
from switches import switches
import relays

#TODO:

    # [DOING] work on interrupt handling for other buttons
    # possibly rework instruction_handler to call the read operations in program mode, move them away from the interrupt "program" mode
    # make json files for as many banks as I think there will be, or figure out checks if the bank exists, and if not create new file?
    # add functionality to mode button to cycle through banks, or add other buttons for this... other buttons probably neater, plenty of i/o pins left - "bank select" as a mode?
    # [DOING] work on display functionality
    # basically debug anything that breaks which will probably be... everything???

t_mem = Memory()
display = Display()

button_pad, write_pad = 0.1, 2

def interrupt_write(pin):
    
    switches["write"].irq(handler = None)
    time.sleep(button_pad)
    
    if pin.value() == 1:
        if t_mem.mode == "manual" or "program":
            t_mem.change_mode("write")
            display.clear()
            display.update_mode(t_mem.mode)
            display.refresh()
            leds.reset_all()
            leds.toggle(6)
            time.sleep(0.5)
            switches["write"].irq(handler = write_handler) 
    else:
        switches["write"].irq(handler = interrupt_write)
            
def write_handler(pin):
        
    switches["write"].irq(handler = None)
    time.sleep(write_pad)
            
    if pin.value() == 1:
        if t_mem.write_location:
            patch_add, bank_add, = t_mem.write_location, t_mem.current_bank
            patch = t_mem.contents
            
            p_mem.write_patch(bank_add, patch_add, patch)
            p_mem.set_default(bank_add, patch_add)
            
            _thread.start_new_thread(leds.rapid_blink, (6,))
            
            display.save_message(t_mem.write_location)
            time.sleep(0.5)
            
            t_mem.copy_write_location()
            t_mem.reset_write_location()
            t_mem.change_mode("program")
            display.clear()
            time.sleep(0.1)
            switches["write"].irq(handler = interrupt_write)
            instruction_handler()
        else:
            display.write_warning()
            time.sleep(1.5)    
            switches["write"].irq(handler = write_handler)
            display.clear()
            display.update_mode(t_mem.mode)
    else:
        switches["write"].irq(handler = write_handler)
            
    display.refresh()
     
def interrupt_mode(pin):

    switches["mode"].irq(handler = None)
    time.sleep(button_pad)
    
    if pin.value() == 1:
        display.clear()
        
        if t_mem.mode == "manual": 
            t_mem.change_mode("program")
            switches["write"].irq(handler = None)
            to_load = p_mem.load_patch(t_mem.current_bank, t_mem.current_patch)
            t_mem.load_patch(to_load)
            instruction_handler()
        
        elif t_mem.mode == "program":
            t_mem.change_mode("manual")
            switches["write"].irq(handler = interrupt_write)
            
        else:
            t_mem.change_mode("manual")
            print("hello mate")
            switches["write"].irq(handler = interrupt_write)
            t_mem.reset_write_location()
            instruction_handler()
            
    display.update_mode(t_mem.mode)
    display.refresh()
    switches["mode"].irq(handler = interrupt_mode)

def interrupt_handler(pin):
    
    pin.irq(handler = None)
    time.sleep(0.1)
    
    if pin.value() == 1:
        for i in range(1, 6, 1):
            if switches[i].value() == 1:  
                if t_mem.mode == "manual":
                    instruction_handler(i) 
                elif t_mem.mode == "program":
                    if t_mem.current_patch == i:
                        pass
                    else:
                        p_mem.set_default(t_mem.current_bank, i)
                        t_mem.set_current_patch(i)
                        to_load = p_mem.load_patch(t_mem.current_bank,i)
                        t_mem.load_patch(to_load)
                        instruction_handler()    
                else:
                    t_mem.set_write_location(i)
                    display.update_line_two("Location: " + str(i))
                    display.refresh()
                    leds.toggle(i)
                    time.sleep(0.3)
                    leds.toggle(i)  
                break
                
    pin.irq(handler = interrupt_handler)

switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)

debug = False

def instruction_handler(single= None):
    
    if debug:
        print("--------------------------------")
        print("Executing in ", t_mem.mode, " mode")
        print("--------------------------------")
        print("Instruction Register: ", i_reg.contents)
        print("Memory Register:      ", t_mem.contents)
    
    
    if single:
        t_mem.load_one(single)
        leds.toggle_one(single)
        relays.toggle_one(single)
        
    else:
        display.clear()
        display.update_mode(t_mem.mode)
        
        if t_mem.mode == "program":
            display.update_bank(t_mem.current_bank)
            display.update_patch(t_mem.current_patch)
        display.refresh()
        
        for step in range(1, 6, 1):
            if step in t_mem.contents:
                relays.set_high(step)
                leds.set_high(step)
            else:
                relays.set_low(step)
                leds.set_low(step)
    
    if debug:
        print("--------------------------------")
        print("Instruction Register: ", i_reg.contents)
        print("Memory Register:      ", t_mem.contents)
        
def start_up():
    
    leds.reset_all()
    relays.reset()
    display.clear()
    display.update_line_one("Starting...")
    display.refresh()
    time.sleep(1)
    
    default_data = p_mem.load_default()
    default_bank = default_data["bank"]
    default_patch = default_data["patch"]
    start_patch = p_mem.load_patch(default_bank, default_patch)
    
    t_mem.load_patch(start_patch)
    t_mem.set_current_patch(default_patch)
    t_mem.set_current_bank(default_bank)
    instruction_handler()

if __name__  == '__main__':
    gc.enable()
    start_up()
    
    