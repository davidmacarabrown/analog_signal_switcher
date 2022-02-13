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

memory = Memory()
display = Display()
settings = Settings()

manual, program, write, menu = 1,2,3,4
button_pad, write_pad = 0.1, 2

def write_enable(pin):

    switches["write"].irq(handler = None)
    time.sleep(button_pad)

    if pin.value() == 1:
        if memory.mode == manual or program:
            memory.change_mode(write)
            display.clear()
            display.update_line(memory.mode, 0)
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
        if memory.write_location:
            patch_add, bank_add, patch = memory.write_location, memory.selected_bank, memory.patch

            _thread.start_new_thread(leds.rapid_blink, (6,))
            display.clear()
            display.update_line("Saving...", 1)
            display.update_line(f">> {memory.write_location}", 2)
            display.refresh()
            disk.write_patch(bank_add, patch_add, patch)
            disk.set_default(bank_add, patch_add)
            memory.copy_write_location()
            memory.reset_write_location()
            memory.change_mode(program)
            time.sleep(0.3)
            display.clear()
            switches["write"].irq(handler = write_enable)
            program_handler()
        else:
            display.clear()
            display.update_line("Select Location", 1)
            display.update_line("Mode > Cancel", 2)
            display.refresh()
            time.sleep(1.5)
            switches["write"].irq(handler = write_handler)
            display.clear()
            display.update_header(memory.mode)
    else:
        switches["write"].irq(handler = write_handler)

    display.refresh()

def change_mode():
    display.clear()
    if memory.mode == manual:
        memory.change_mode(program)
        switches["write"].irq(handler = None)
        memory.load_patch(memory.selected_patch)
        program_handler()
    elif memory.mode == program:
        memory.change_mode(manual)
        switches["write"].irq(handler = write_enable)
    else:
        memory.change_mode(manual)
        leds.reset_all()
        switches["write"].irq(handler = write_enable)
        memory.reset_write_location()
        program_handler()

    display.update_line(memory.mode, 0)
    display.refresh()

def interrupt_mode(pin):

    switches["mode"].irq(handler = None)
    time.sleep(button_pad)

    if pin.value():
        if switches["write"].value():
            if memory.mode != menu:
                memory.mode = menu
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
    memory.load_bank(disk.read_bank(memory.selected_bank))
    display.update_bank(memory.selected_bank)
    if memory.selected_bank != memory.active_bank and memory.selected_patch == memory.active_patch:
        display.update_patch("-")
        display.refresh()
    else:
        memory.load_selected_patch()
        program_handler()

def interrupt_handler(pin):

    disable_irq()
    time.sleep(0.1)

    if pin.value():
        stack = []

        for i in range(1, 6, 1):
            if switches[i].value():
                stack.append[i]

        if memory.mode == program:
            if len(stack) == 2:
                if 1 in stack:
                    memory.decrement_bank()
                    bank_change()

                elif 3 in stack:
                    memory.increment_bank()
                    bank_change()

            else:
                memory.set_selected_patch(stack[0])
                memory.load_patch(i)
                program_handler()
                disk.set_default(memory.selected_bank, i)

        elif memory.mode == manual:
            manual_handler(stack[0])

        else:
            memory.set_write_location(stack[0])
            display.update_line(f"Location: {i}", 1)
            display.refresh()
            leds.toggle(i)
            time.sleep(0.2)
            leds.toggle(i)

    enable_irq()

def manual_handler(single):
    memory.load_one(single)
    leds.toggle_one(single)
    relays.toggle_one(single)
    memory.set_active()
    show_debug()

def program_handler():
        for step in range(1, 6, 1):
            if step in memory.patch:
                relays.set_high(step)
                leds.set_high(step)
            else:
                relays.set_low(step)
                leds.set_low(step)

        display.clear()
        if memory.mode == program:
            display.update_line(memory.mode, 0)
            display.update_bank(memory.selected_bank)
            display.update_patch(memory.selected_patch)
            disk.set_default(memory.selected_bank, memory.selected_patch)
        display.refresh()

    memory.set_active()
    show_debug()

def show_debug:
    if memory.debug:
        print("--------------------------------")
        print(f"Executing in {memory.mode} mode")
        print("--------------------------------")
        print(f"Patch Selected: {memory.selected_patch} Memory Contents:       {memory.patch}")
        print(f"Bank Selected: {memory.selected_bank} Bank Contents:        {memory.bank}")

def main():
    global debug
    if switches["write"].value():
        memory.enable_debug()
        time.sleep(1)

    leds.reset_all()
    relays.reset()
    display.clear()

    settings.load_settings()

    for opt in settings.params["startup-mode"]["options"]:
        if opt["status"] == true:
            memory.change_mode(opt["option"])

    default_location = disk.read_default()

    memory.load_bank(disk.read_bank(default_location["bank"]))
    memory.set_selected_bank(default_location["bank"])
    memory.set_selected_patch(default_location["patch"])
    display.update_line(memory.mode, 0)

    if memory.mode == program:
        memory.load_selected_patch()
        program_handler()

    display.refresh()

    switches[1].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[2].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[3].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[4].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches[5].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_handler)
    switches["mode"].irq(trigger=machine.Pin.IRQ_RISING, handler=interrupt_mode)
    switches["write"].irq(trigger=machine.Pin.IRQ_RISING, handler=write_enable)

if __name__  == '__main__':
    main()
