import time
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

MANUAL, PROGRAM, WRITE, MENU = "manual", "program", "write", "menu"

memory = Memory()
display = Display()
settings = Settings()

button_pad, write_pad = 0.1, 2

def write_enable(pin):

    switches["w"].irq(handler = None)
    time.sleep(button_pad)

    if pin.value() == 1:
        memory.change_mode(WRITE)
        display.clear()
        display.update_line(memory.get_mode(), 0)
        display.refresh()
        leds.reset_all()
        leds.toggle(6)
        switches["w"].irq(handler = write_handler)
    else:
        switches["w"].irq(handler = write_enable)

def write_handler(pin):

    switches["w"].irq(handler = None)
    time.sleep(write_pad)

    if pin.value():
        if memory.get_write_location():
            patch_add, bank_add, patch = memory.get_write_location(), memory.get_selected_bank(), memory.get_patch()

            _thread.start_new_thread(leds.rapid_blink, (6,))
            display.clear()
            display.update_line("Saving...", 1)
            display.update_line(f">> {memory.get_write_location()}", 2)
            display.refresh()
            disk.write_patch(bank_add, patch_add, patch)
            disk.set_default(bank_add, patch_add)
            memory.copy_write_location()
            memory.reset_write_location()
            memory.change_mode(PROGRAM)
            time.sleep(0.3)
            display.clear()
            switches["w"].irq(handler = write_enable)
            patch_handler()
        else:
            display.clear()
            display.update_line("Select Location", 1)
            display.update_line("Mode > Cancel", 2)
            display.refresh()
            time.sleep(1.5)
            switches["w"].irq(handler = write_handler)
            display.clear()
            display.update_header(memory.get_mode())
    else:
        switches["w"].irq(handler = write_handler)

    display.refresh()

def change_mode():
    display.clear()
    if memory.get_mode() == MANUAL:
        memory.change_mode(PROGRAM)
        switches["w"].irq(handler = None)
        memory.load_patch(memory.get_selected_patch())
        patch_handler()
    elif memory.get_mode() == PROGRAM:
        memory.change_mode(MANUAL)
        switches["w"].irq(handler = write_enable)
    else:
        memory.change_mode(MANUAL)
        leds.reset_all()
        switches["w"].irq(handler = write_enable)
        memory.reset_write_location()
        display.clear()
        display.update_line(memory.get_mode(), 0)
        display.refresh()
        patch_handler()
        return

    display.update_line(memory.get_mode(), 0)
    display.refresh()

def interrupt_mode(pin):

    switches["m"].irq(handler = None)
    time.sleep(button_pad)

    if pin.value():
        if switches["w"].value():
            if memory.get_mode() != MENU:
                memory.change_mode(MENU)
                show_menu()
                switches["m"].irq(handler = interrupt_mode)
                return
            else:
                close_menu()
                switches["m"].irq(handler = interrupt_mode)

        change_mode()

    switches["m"].irq(handler = interrupt_mode)

def show_menu():
    relays.reset()
    leds.reset_all()
    display.clear()
    display.update_line(MENU, 0)

    display.refresh()

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
    selected_bank = memory.get_selected_bank()

    memory.load_bank(disk.read_bank(selected_bank))
    display.update_bank(selected_bank)
    if selected_bank != memory.get_active_bank() and memory.get_selected_patch() == memory.get_active_patch():
        display.update_patch("-")
        display.refresh()
    else:
        memory.load_selected_patch()
        patch_handler()

def interrupt_handler(pin):

    disable_irq()
    time.sleep(0.1)

    if pin.value():
        stack = []

        for i in range(1, 6, 1):
            if switches[i].value():
                stack.append(i)

        if len(stack) ==2:
            if memory.get_mode() == PROGRAM:
                if 1 in stack:
                    memory.decrement_bank()
                    bank_change()

                elif 3 in stack:
                    memory.increment_bank()
                    bank_change()

        else:
            location = stack[0]

            if memory.get_mode() == MANUAL:
                manual_handler(location)

            elif memory.get_mode() == PROGRAM and memory.get_active_patch() != location:
                memory.set_selected_patch(location)
                memory.load_patch(location)
                patch_handler()
                disk.set_default(memory.get_selected_bank(), location)

            elif memory.get_mode() == WRITE:
                memory.set_write_location(location)
                display.update_line(f"Location: {location}", 1)
                display.refresh()
                leds.toggle(location)
                time.sleep(0.2)
                leds.toggle(location)

    enable_irq()

def manual_handler(single):
    memory.load_one(single)
    leds.toggle_one(single)
    relays.toggle_one(single)
    memory.set_active_bank()
    show_debug()

def patch_handler():
    for step in range(1, 6, 1):
        if step in memory.get_patch():
            relays.set_high(step)
            leds.set_high(step)
        else:
            relays.set_low(step)
            leds.set_low(step)

    selected_bank, selected_patch = memory.get_selected_bank(), memory.get_selected_patch()

    if memory.get_mode() == PROGRAM:
        display.clear()
        display.update_line(memory.get_mode(), 0)
        display.update_bank(selected_bank)
        display.update_patch(selected_patch)
        disk.set_default(selected_bank, selected_patch)
        display.refresh()

    memory.set_active_bank()
    show_debug()

def show_debug():
    if memory.debug:
        print("--------------------------------")
        print(f"Executing in {memory.mode} mode")
        print("--------------------------------")
        print(f"Bank Selected:  {memory.selected_bank}")
        print(f"Patch Selected: {memory.selected_patch}")
        print("--------------------------------")
        print(f"Memory Contents:  {memory.patch}")
        print(f"Bank Contents:    {memory.bank}")
        print(f"Default Patch: {disk.read_default()}")

def main():
    global debug
    if switches["w"].value():
        memory.enable_debug()
        time.sleep(1)

    leds.reset_all()
    relays.reset()
    display.clear()

    settings.set_params(disk.load_settings())

    print(settings.get_params())

    for opt in settings.get_params()["startup-mode"]["options"]:
        if opt["status"] == True:
            memory.change_mode(opt["option"])

    default_location = disk.read_default()

    memory.load_bank(disk.read_bank(default_location["bank"]))
    memory.set_selected_bank(default_location["bank"])
    memory.set_selected_patch(default_location["patch"])
    display.update_line(memory.get_mode(), 0)

    if memory.get_mode() == PROGRAM:
        memory.load_selected_patch()
        memory.set_active_bank()
        patch_handler()

    display.refresh()

    switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches["m"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)
    switches["w"].irq(trigger=machine.Pin.IRQ_RISING, handler=write_enable)

if __name__  == '__main__':
    main()
