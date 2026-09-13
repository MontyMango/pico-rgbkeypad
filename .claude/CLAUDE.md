# Pico RGB Keypad Project Context

## Overview
This repository is a CircuitPython project for a Raspberry Pi Pico running a Pimoroni RGB keypad board as a custom OBS/streaming control deck.

The project is based on the original Pico RGB Keypad work by Martin O'Hanlon, with custom key mappings and media-control behavior added for a personal setup.

## Purpose
- Turn a Raspberry Pi Pico + RGB keypad into a USB HID device.
- Map physical keys to media controls and keyboard shortcuts.
- Use the keypad as a lightweight streaming/desktop control surface, especially with OBS Studio.
- Keep the logic in a single `main.py` file while using a local `lib/` folder for CircuitPython dependencies.

## High-level architecture
- `main.py`: the actual runtime program executed on the Pico.
- `lib/rgbkeypad.py`: custom driver for the Pimoroni keypad board; handles GPIO/I2C/SPI communication and key state/color updates.
- `lib/adafruit_hid/`: Adafruit HID support library for keyboard and consumer-control events.
- `firmware/`: CircuitPython UF2 firmware images intended for flashing the Pico.

## Current implementation details
`main.py` sets up:
- `RGBKeypad()` for the matrix keypad
- `Keyboard(usb_hid.devices)` for hotkey-style keyboard combos
- `ConsumerControl(usb_hid.devices)` for media shortcuts

The project currently uses:
- `CONSUMER_CONTROL_KEYS` for media controls such as previous, play/pause, next, volume up/down, and mute.
- `KEYBOARD_SHORTCUTS` for custom keyboard combos, mostly modifier + keypad keys.
- brightness and idle/sleep behavior to dim or power off the keypad after inactivity.

## Important runtime behavior
- This is not a normal desktop Python app; it is intended to run directly on a CircuitPython-enabled Pico.
- The code uses `usb_hid` and Adafruit HID APIs, so it must be copied to the device filesystem alongside `lib/`.
- Key mappings are configured directly in `main.py` and are designed around the keypad’s physical layout.
- The device is polled in a loop; any key press triggers a shortcut and then holds the selected brightness while pressed.

## Key files
- [main.py](../main.py): main program, key mapping, colors, event handling, and loop logic.
- [lib/rgbkeypad.py](../lib/rgbkeypad.py): hardware driver and key abstraction for the keypad.
- [README.md](../README.md): setup instructions and mapping description.

## Hardware/firmware notes
- The board is meant to run CircuitPython.
- The included firmware is in `firmware/` and can be flashed to the Pico in bootloader mode.
- The repo expects `lib/adafruit_hid` and `lib/rgbkeypad.py` to be present on the Pico alongside `main.py`.

## Working assumptions for future changes
- Preserve CircuitPython compatibility; do not add standard PC Python dependencies.
- Any new keys or actions should be added in `main.py` through the existing mapping dictionaries.
- Avoid breaking the device polling loop and keypad LED update behavior.
- If you change physical mappings, keep the keyboard and consumer-control semantics consistent with the OBS hotkey workflow described in the README.

## Repo status
- No automated tests are present in this repo.
- This project is hardware-oriented and script-driven rather than application-framework-based.
- Most debugging will happen by flashing code to the Pico and testing the live HID behavior.

## Suggested future task directions
- Add a second page/mode for different key layouts.
- Add visual feedback on pressed keys with non-blocking animation.
- Expand the custom shortcut mapping to support more OBS functions or app-specific hotkeys.
- Clean up the current logic to separate key mapping, colors, and device behavior more clearly.
