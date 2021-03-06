from machine import Pin
import machine

switches ={
            1: machine.Pin(20, machine.Pin.IN, Pin.PULL_DOWN),
            2: machine.Pin(19, machine.Pin.IN, Pin.PULL_DOWN),
            3: machine.Pin(18, machine.Pin.IN, Pin.PULL_DOWN),
            4: machine.Pin(17, machine.Pin.IN, Pin.PULL_DOWN),
            5: machine.Pin(16, machine.Pin.IN, Pin.PULL_DOWN),
            "w": machine.Pin(22, machine.Pin.IN, Pin.PULL_DOWN),
            "m": machine.Pin(21, machine.Pin.IN, Pin.PULL_DOWN)
            }
