import time
import gc
import _thread
from machine import Pin, I2C

from memory import Memory
from display import Display
from settings import Settings

import disk as disk
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
settings = Settings()

button_pad, write_pad = 0.1, 2

def write_enable(pin):
    
    switches["write"].irq(handler = None)
    time.sleep(button_pad)
    
    if pin.value() == 1:
        if t_mem.mode == "manual" or "program":
            t_mem.change_mode("write")
            display.clear()
            display.update_line(t_mem.mode, 0)
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
            patch_add, bank_add, patch = t_mem.write_location, t_mem.selected_bank, t_mem.patch
            
            _thread.start_new_thread(leds.rapid_blink, (6,))
            display.clear()
            display.update_line("Saving...", 1)
            display.update_line(f">> {t_mem.write_location}", 2)
            display.refresh()
            disk.write_patch(bank_add, patch_add, patch)
            disk.set_default(bank_add, patch_add)            
            t_mem.copy_write_location()
            t_mem.reset_write_location()
            t_mem.change_mode("program")
            time.sleep(0.3)
            display.clear()
            switches["write"].irq(handler = write_enable)
            instruction_handler()
        else:
            display.clear()
            display.update_line("Select Location", 1)
            display.update_line("Mode > Cancel", 2)
            display.refresh()
            time.sleep(1.5)    
            switches["write"].irq(handler = write_handler)
            display.clear()
            display.update_header(t_mem.mode)
    else:
        switches["write"].irq(handler = write_handler)
            
    display.refresh()
    
def change_mode():
    display.clear()
    if t_mem.mode == "manual": 
        t_mem.change_mode("program")
        switches["write"].irq(handler = None)
        t_mem.load_patch(t_mem.selected_patch)
        instruction_handler()
    elif t_mem.mode == "program":
        t_mem.change_mode("manual")
        switches["write"].irq(handler = write_enable)
    else:
        t_mem.change_mode("manual")
        leds.reset_all()
        switches["write"].irq(handler = write_enable)
        t_mem.reset_write_location()
        instruction_handler()
            
    display.update_line(t_mem.mode, 0)
    display.refresh()
     
def interrupt_mode(pin):

    switches["mode"].irq(handler = None)
    time.sleep(button_pad)
    
    if pin.value():
        if switches["write"].value():
            if t_mem.mode != "menu":
                t_mem.mode = "menu"
                show_menu()
                switches["mode"].irq(handler = interrupt_mode)
                return
            else:
                close_menu()
                switches["mode"].irq(handler = interrupt_mode)

        change_mode()
            
    switches["mode"].irq(handler = interrupt_mode)
    
def show_menu():
    relays.reset()
    leds.reset_all()
    display.clear()
    display.update_line("menu", 0)
    
    display.refresh()

def reset_irq():
    switches[1].irq(handler=interrupt_handler)
    switches[2].irq(handler=interrupt_handler)
    switches[3].irq(handler=interrupt_handler)
    switches[4].irq(handler=interrupt_handler)
    switches[5].irq(handler=interrupt_handler)
    return
    
def disable_patch_irq():
    switches[1].irq(handler=None)
    switches[2].irq(handler=None)
    switches[3].irq(handler=None)
    switches[4].irq(handler=None)
    switches[5].irq(handler=None)
    return

def bank_change():
    t_mem.load_bank(disk.read_bank(t_mem.selected_bank))
    display.update_bank(t_mem.selected_bank)
    if t_mem.selected_bank != t_mem.active_bank and t_mem.selected_patch == t_mem.active_patch:
        display.update_patch("-")
        display.refresh()
    else:
        t_mem.load_selected_patch()
        instruction_handler()

def interrupt_handler(pin):
    
    _thread.start_new_thread(disable_patch_irq, ())
    time.sleep(0.1)

    if pin.value():
        if switches[2].value():
            if switches[1].value():
                _thread.start_new_thread(reset_irq, ())
                t_mem.decrement_bank()
                bank_change()
                return
            
            elif switches[3].value():
                _thread.start_new_thread(reset_irq, ())
                t_mem.increment_bank()
                bank_change()
                return

        for i in range(1, 6, 1):
            if switches[i].value():  
                if t_mem.mode == "manual":
                    instruction_handler(i) 
                elif t_mem.mode == "program":
                    disk.set_default(t_mem.selected_bank, i)
                    t_mem.set_selected_patch(i)
                    t_mem.load_patch(i)
                    instruction_handler()    
                else:
                    t_mem.set_write_location(i)
                    display.update_line(f"Location: {i}", 1)
                    display.refresh()
                    leds.toggle(i)
                    time.sleep(0.2)
                    leds.toggle(i)  
                break
                
    reset_irq()

debug = False
def instruction_handler(single= None):
    
    if single:
        t_mem.load_one(single)
        leds.toggle_one(single)
        relays.toggle_one(single)
        t_mem.set_active()
        return
        
    else:
        for step in range(1, 6, 1):
            if step in t_mem.patch:
                relays.set_high(step)
                leds.set_high(step)
            else:
                relays.set_low(step)
                leds.set_low(step)
                
        display.clear()
        if t_mem.mode == "program":
            display.update_line(t_mem.mode, 0)
            display.update_bank(t_mem.selected_bank)
            display.update_patch(t_mem.selected_patch)
            disk.set_default(t_mem.selected_bank, t_mem.selected_patch)
        display.refresh()
        
    t_mem.set_active()
    
    if debug:
        print("--------------------------------")
        print(f"Executing in {t_mem.mode} mode")
        print("--------------------------------")
        print(f"Patch Selected: {t_mem.selected_patch} Memory Contents:       {t_mem.patch}")
        print(f"Bank Selected: {t_mem.selected_bank} Bank Contents:        {t_mem.bank}")
        
def main():
    global debug
    if switches["write"].value():
        debug = True
        time.sleep(1)
    
    leds.reset_all()
    relays.reset()
    display.clear()
    
    settings.load_settings()
    
    for p in settings.params:
        if p["parameter"] == "startup-mode":
            for opt in p["options"]:
                if opt["status"] == True:
                    t_mem.change_mode(opt["name"])
                
    default_location = disk.read_default()
    
    t_mem.load_bank(disk.read_bank(default_location["bank"]))
    t_mem.set_selected_bank(default_location["bank"])
    t_mem.set_selected_patch(default_location["patch"])
    
    if t_mem.mode == "program":
        t_mem.load_selected_patch()
        
    display.update_line(t_mem.mode, 0)
    display.refresh()
    instruction_handler()
    
    switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)
    switches["write"].irq(trigger=machine.Pin.IRQ_RISING, handler=write_enable)
    
if __name__  == '__main__':
    gc.enable()
    main()
    
    