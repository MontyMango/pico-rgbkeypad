# Cameron Harter - Added ConsumerControl features

import time
import usb_hid
from rgbkeypad import RGBKeypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode    # Used for media control
from random import randint


# Please refer to Layout.png for a better understand on what this does

CONSUMER_CONTROL_KEYS = {
    # First (Top) row
    (0,0): ConsumerControlCode.SCAN_PREVIOUS_TRACK,         # 0
    (1,0): ConsumerControlCode.PLAY_PAUSE,                  # 1
    (2,0): ConsumerControlCode.SCAN_NEXT_TRACK,             # 2
    (3,0): ConsumerControlCode.VOLUME_INCREMENT,            # 3

    # Second row
    (3,1): ConsumerControlCode.VOLUME_DECREMENT,            # 7

    # Third row
    (3,2): ConsumerControlCode.MUTE                         # B

}

KEYBOARD_SHORTCUTS = {
    # Second row
    (0,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FIVE,),  # 4
    (1,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SIX,),   # 5
    (2,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SEVEN,), # 6
    
    # Third row
    (0,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_NINE,),  # 8
    (1,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ZERO,),  # 9
    (2,2): (Keycode.LEFT_ALT, Keycode.KEYPAD_ONE,),       # A
    
    # Fourth (Bottom) row
    (0,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_THREE,),     # C
    (1,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FOUR,),      # D
    (2,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FIVE,),      # E
    (3,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_SIX,)        # F
}

# CLASS DECLARATIONS
keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)


# KEY BRIGHTNESS & COLORS
# If you want to turn off a block (If it's not being used)
# keypad.keys[0].color = (0,0,0)

DEFAULT_BRIGHTNESS = 0.1
IDLE_BRIGHTNESS = 0.05

def setBrightness(BRIGHTNESS):
    for key in keypad.keys:
        key.brightness = BRIGHTNESS


INVALID_KEY_COLOR = (255, 0, 0)

# Indicate the colors for the keys
# Color randomization (if needed)
# for key in keypad.keys:
#     key.color = (randint(0,255), randint(0,255), randint(0,255))

# MEDIA COLORS
keypad.keys[0].color = (102, 0, 204)        # Previous track
keypad.keys[1].color = (51, 51, 255)        # Play / Pause
keypad.keys[2].color = (204, 0, 255)        # Next track

# VOLUME COLORS
keypad.keys[3].color = (0, 102, 0)          # Volume up
keypad.keys[7].color = (102, 0, 0)          # Volume down
keypad.keys[11].color = (102, 102, 153)     # Mute volume

setBrightness(DEFAULT_BRIGHTNESS)


def whenKeyIsPressed(pressedKey):
    pressedKey.brightness = 1

    # If it's a keyboard shortcut, execute the keyboard shortcut
    if (key.x, key.y) in KEYBOARD_SHORTCUTS.keys():
        kbd.send(*KEYBOARD_SHORTCUTS[(key.x, key.y)]) 
    # If it's a consumer control shortcut, execute the key as a consumer control shortcut
    elif (key.x, key.y) in CONSUMER_CONTROL_KEYS.keys():
        cc.send(CONSUMER_CONTROL_KEYS[(key.x, key.y)])
        time.sleep(0.1)
    else:
        pressedKey.color = INVALID_KEY_COLOR



# MAIN PROGRAM
last_interaction_time = time.time()
isIdle = False

while True:
    for key in keypad.keys:
        if key.is_pressed():
            setBrightness(DEFAULT_BRIGHTNESS)
            whenKeyIsPressed(key)

            while key.is_pressed():
                pass

            last_interaction_time = time.time()
            isIdle = False

        else:
            # If the keypad idles for 5 second, dim the lights!
            if(isIdle is False):   
                if((time.time() - last_interaction_time) > 5 ):
                    setBrightness(IDLE_BRIGHTNESS)
                    isIdle = True