# Analog Signal Switcher Prototype Code
## Overview
This program is in development to allow the Rasperry Pi Pico (or other RP2040 based controller) to be used as a programmable loop switcher for guitar effects pedals. It facilitates similar functionality to some "name brand" offerings but with the charm of a Do-It-Yourself project. The codebase is written using MicroPython - a fork of Python 3 intended for microcontrollers. More information on MicroPython can be found at: https://micropython.org/  

## Working Features
- Manual Mode: one input toggles one set of relays, on or off - standard true-bypass looper functionality
- Manual Mode: carries over from Program Mode, so active loops are maintained when switching from Program to Manual
- Program Mode: loads banks from disk
- Program Mode: select patch with switch
- Program Mode: loads the last used program upon startup
- Program Mode: can change banks by using a combination of input buttons to move up or down
- Program Mode: program waits for an input selection when changing banks
- Write Mode: enter write mode by holding "Write" button
- Write Mode: write patch to disk
- Write Mode: select write location while in write mode
- Write Mode: exit write mode by pressing the "Mode" button
- OLED Display: shows mode, bank, patch and write information

## Notes
Concerning data storage, there are libraries available for interfacing with SD Cards via the controllers data busses but their performance was just too unreliable and slow to be a viable option. The endurance of the Pi Pico flash memory is unknown to me, however I do not anticipate the writing of small json files to have any major impact on the lifespan of the storage.

## Planned Features
- MIDI functionality for controlling or being controlled by external units (would require large rework of the program memory to include MIDI data)
- Browsing and editing/deleting banks more quickly using buttons
- Enabling/Disabling features such as delay tails (would require summing amplifiers to be added to every loop and complicate the switching)
- Switchable buffer circuitry
- Built-in Tuner functionality
- Amp Switching Output TS or TRS

Both hardware and code are still in prototyping stage with the completed code, example build instructions and full documentation to follow.
