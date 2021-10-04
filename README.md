# Analog Signal Switcher Prototype Code
## Overview
This program is in development to allow the Rasperry Pi Pico (or other RP2040 based controller) to be used as a programmable loop switcher for guitar effects pedals. It facilitates similar functionality to some "name brand" offerings but with the charm of a Do-It-Yourself project. The codebase is written using MicroPython - a fork of Python 3 intended for microcontrollers. More information on MicroPython can be found at: https://micropython.org/  

## Features
The program allows two modes of operation: a fully manual mode which functions just like any true-bypass looper; and a program mode with banks of patch memory which are stored on the device. The code provides 5 switchable outputs as standard which can be expanded within the limits of the GPIO pins of the controller. Inputs are also mapped for changing mode and saving patches to the internal filesystem of the Pico. The patch banks are saved as JSON files with numerical keys representing patch number, and the values containing a numerical array representing the active outputs.

## Notes
Concerning data storage, there are libraries available for interfacing with SD Cards via the controllers data busses but their performance was just too unreliable and slow to be a viable option. The endurance of the Pi Pico flash memory is unknown to me, however I do not anticipate the writing of json.

## Planned Features
I plan to implement a display into the prototype and have already begun researching and testing some different displays. Adding a display will open up the possibility for menu functionality which can in turn open up many other additional possibilities including:

- MIDI functionality for controlling or being controlled by external units (would require large rework of the program memory to include MIDI data)
- Browsing and editing/deleting banks more quickly using buttons
- Enabling/Disabling features such as delay tails (would require summing amplifiers to be added to every loop and complicate the switching)

Both hardware and code are still in prototyping stage with the completed code, example build instructions and full documentation to follow.
