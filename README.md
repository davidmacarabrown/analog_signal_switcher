# Analog Signal Switcher Prototype Code
## Overview
This program is in development to allow the Rasperry Pi Pico (or other RP2040 based controller) to be used as a programmable loop switcher for guitar effects pedals. It facilitates similar functionality to some "name brand" offerings but with the charm of a Do-It-Yourself project. The codebase is written using MicroPython - a fork of Python 3 intended for microcontrollers. More information on MicroPython can be found at: https://micropython.org/  

## Features
The program allows two modes of operation: a fully manual mode which functions just like any true-bypass looper; and a program mode with banks of patch memory which are stored on the device. The code provides 5 switchable outputs as standard which can be expanded within the limits of the GPIO pins of the controller. Inputs are also mapped for changing mode and saving patches to memory. The program memory saves to the internal filesystem of the Pico. There are libraries available for interfacing with SD Cards via the controllers data busses but their performance was just too unreliable and slow to be a viable option.

Both hardware and code are still in prototyping stage with the completed code and build instructions to follow.
