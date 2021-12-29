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



"""

INFO:
    + top segment of display is 16px
    + bottom segment is 48px

TODO:

    + basically debug anything that breaks which will probably be... everything???
    
"""

t_mem = Memory()
display = Display()

button_pad, write_pad = 0.1, 2

def write_enable(pin):
    
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
            switches["write"].irq(handler = write_handler) 
    else:
        switches["write"].irq(handler = write_enable)
            
def write_handler(pin):
        
    switches["write"].irq(handler = None)
    time.sleep(write_pad)
            
    if pin.value():
        if t_mem.write_location:
            patch_add, bank_add, patch = t_mem.write_location, t_mem.current_bank, t_mem.patch
            
            _thread.start_new_thread(leds.rapid_blink, (6,))
            display.save_message(t_mem.write_location)
            p_mem.write_patch(bank_add, patch_add, patch)
            p_mem.set_default(bank_add, patch_add)            
            t_mem.copy_write_location()
            t_mem.reset_write_location()
            t_mem.change_mode("program")
            display.clear()
            switches["write"].irq(handler = write_enable)
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
            t_mem.load_patch(t_mem.current_patch)
            instruction_handler()
        elif t_mem.mode == "program":
            t_mem.change_mode("manual")
            switches["write"].irq(handler = write_enable)
        else:
            t_mem.change_mode("manual")
            print("hello mate")
            switches["write"].irq(handler = write_enable)
            t_mem.reset_write_location()
            instruction_handler()
            
    display.update_mode(t_mem.mode)
    display.refresh()
    switches["mode"].irq(handler = interrupt_mode)
    
def enable_irq():
    switches[1].irq(handler=interrupt_handler)
    switches[2].irq(handler=interrupt_handler)
    switches[3].irq(handler=interrupt_handler)
    switches[4].irq(handler=interrupt_handler)
    switches[5].irq(handler=interrupt_handler)
    return
    
def disable_irq():
    switches[1].irq(handler=None)
    switches[2].irq(handler=None)
    switches[3].irq(handler=None)
    switches[4].irq(handler=None)
    switches[5].irq(handler=None)
    return

def bank_change():
    t_mem.load_bank(p_mem.read_bank(t_mem.current_bank))
    display.update_bank(t_mem.current_bank)
    if t_mem.current_bank != t_mem.active_bank and t_mem.current_patch == t_mem.active_patch:
        display.update_patch("-")
        display.refresh()
    else:
        t_mem.load_current_patch()
        instruction_handler()

def interrupt_handler(pin):
    
    _thread.start_new_thread(disable_irq, ())
    time.sleep(0.1)

    if pin.value():
        if switches[2].value():
            if switches[1].value():
                _thread.start_new_thread(enable_irq, ())
                t_mem.decrement_bank()
                bank_change()
                return
            
            elif switches[3].value():
                _thread.start_new_thread(enable_irq, ())
                t_mem.increment_bank()
                bank_change()
                return

        for i in range(1, 6, 1):
            if switches[i].value():  
                if t_mem.mode == "manual":
                    instruction_handler(i) 
                elif t_mem.mode == "program":
                    p_mem.set_default(t_mem.current_bank, i)
                    t_mem.set_current_patch(i)
                    t_mem.load_patch(i)
                    instruction_handler()    
                else:
                    t_mem.set_write_location(i)
                    display.update_line_two(f"Location: {str(i)}")
                    display.refresh()
                    leds.toggle(i)
                    time.sleep(0.2)
                    leds.toggle(i)  
                break
                
    enable_irq()

debug = False
def instruction_handler(single= None):
    
    if debug:
        print("--------------------------------")
        print(f"Executing in {t_mem.mode} mode")
        print("--------------------------------")
        print(f"Patch {t_mem.current_patch} Contents:       {t_mem.patch}")
        print(f"Bank {t_mem.current_bank} Contents:        {t_mem.bank}")
    
    if single:
        t_mem.load_one(single)
        leds.toggle_one(single)
        relays.toggle_one(single)
    else:
        for step in range(1, 6, 1):
            if step in t_mem.patch:
                relays.set_high(step)
                leds.set_high(step)
            else:
                relays.set_low(step)
                leds.set_low(step)
                
        display.clear()
        display.update_mode(t_mem.mode)
        display.update_bank(t_mem.current_bank)
        display.update_patch(t_mem.current_patch)
        display.refresh()
        p_mem.set_default(t_mem.current_bank, t_mem.current_patch)
        t_mem.set_active()
        
def main():
    global debug
    if switches["write"].value():
        debug = True
        time.sleep(1)
    
    leds.reset_all()
    relays.reset()
    display.clear()
    display.refresh()
    default_location = p_mem.read_default()
    t_mem.load_bank(p_mem.read_bank(default_location["bank"]))
    t_mem.set_current_bank(default_location["bank"])
    t_mem.set_current_patch(default_location["patch"])
    t_mem.load_current_patch()

    instruction_handler()
    
    switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)
    
if __name__  == '__main__':
    gc.enable()
    main()
    
    