# MontyMango - Added ConsumerControl features

import time
import usb_hid
from rgbkeypad import RGBKeypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode    # Used for media control


#region Changable variables
# idleTime - When the keypad should dim it's lights
idleTime = 5            # Default is 5 seconds (5)
# sleepTime - When the keypad should turn off it's lights
sleepTime = 360         # Default is 5 minutes (360)

#endregion

# --- Below is system functionality, enter if you know what you're doing ---

#region Global Variables

# Selected Key Colors
INVALID_KEY_COLOR = (255, 0, 0)

# Brightness
DEFAULT_BRIGHTNESS = 0.1
IDLE_BRIGHTNESS = 0.04
#endregion


#region Needed Class Declarations
keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
#endregion


#region Key Functionality
# Please refer to Layout.png for the keys

CONSUMER_CONTROL_KEYS = {
    # First (Top) row
    (0,0): ConsumerControlCode.SCAN_PREVIOUS_TRACK,         # 0
    (1,0): ConsumerControlCode.PLAY_PAUSE,                  # 1
    (2,0): ConsumerControlCode.SCAN_NEXT_TRACK,             # 2
    #(3,0): ConsumerControlCode.,                           # 3
    
    # Second row
    (3,1): ConsumerControlCode.VOLUME_INCREMENT,            # 7

    # Third row
    (3,2): ConsumerControlCode.VOLUME_DECREMENT,            # B

    # Fourth row
    (3,3): ConsumerControlCode.MUTE                         # F
}

# Default Shortcuts (from Fork) (Commented out )
KEYBOARD_SHORTCUTS = {
    # First row
    #(0,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ONE),     # 0
    #(1,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_TWO),     # 1
    #(2,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_THREE),     # 2
    (3,0): (Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.ESCAPE),      # 3

    # Second row
    (0,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FIVE,),    # 4
    (1,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SIX,),     # 5
    (2,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SEVEN,),   # 6
    #(3,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_EIGHT),   # 7

    # Third row
    (0,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_NINE,),    # 8
    (1,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ZERO,),    # 9
    (2,2): (Keycode.LEFT_ALT, Keycode.KEYPAD_ONE,),         # A
    #(3,2): (Keycode.LEFT_ALT, Keycode.KEYPAD_TWO),         # B

    # Fourth (Bottom) row
    (0,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_THREE,),       # C
    (1,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FOUR,),        # D
    (2,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FIVE,),        # E
    #(3,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_SIX,)         # F
}
#endregion


#region KEY BRIGHTNESS & COLORS
# If you want to turn off a block (If it's not being used)
# keypad.keys[0].color = (0,0,0)


def setBrightness(BRIGHTNESS):
    for key in keypad.keys:
        key.brightness = BRIGHTNESS

# First row – Media (soft gray‑tinted pastel scheme)
keypad.keys[0].color = (40, 120, 255)       # Previous track
keypad.keys[1].color = (255, 150, 30)       # Play / Pause
keypad.keys[2].color = (30, 210, 220)       # Next track
# keypad.keys[3].color = (200, 200, 200)          # Switch modes (Reserved for a future update)

# Second Row
# Second row - Discord
keypad.keys[4].color = (150, 50, 220)       # Toggle Mute
keypad.keys[5].color = (90, 30, 170)         # Toggle Deafen
keypad.keys[6].color = (220, 50, 140)        # Toggle Camera
keypad.keys[7].color = (40, 220, 80)         # Volume up

# Third Row
# keypad.keys[8].color = (0, 0, 0)
# keypad.keys[9].color = (0, 0, 0)
# keypad.keys[10].color = (0, 0, 0)
keypad.keys[11].color = (220, 50, 40)        # Volume down

# Fourth Row
# keypad.keys[12].color = (0, 0, 0)
# keypad.keys[13].color = (0, 0, 0)
# keypad.keys[14].color = (0, 0, 0)
keypad.keys[15].color = (255, 80, 20)        # Mute volume

#endregion

#region Events / Functions
def whenKeyIsPressed(pressedKey):
    keyPressed = (pressedKey.x, pressedKey.y)

    # If it's a keyboard shortcut, execute the keyboard shortcut
    if keyPressed in KEYBOARD_SHORTCUTS.keys():
        kbd.send(*KEYBOARD_SHORTCUTS[(key.x, key.y)]) 
    # If it's a consumer control shortcut, execute the key as a consumer control shortcut
    elif keyPressed in CONSUMER_CONTROL_KEYS.keys():
        cc.send(CONSUMER_CONTROL_KEYS[(key.x, key.y)])
        time.sleep(0.1)
    else:
        pressedKey.color = INVALID_KEY_COLOR

# def flashSelectedKey(pressedKey, duration=1):
#     start_time = time.monotonic()
#     original_brightness = pressedKey.brightness

#     while time.monotonic() - start_time < duration:
#         pressedKey.brightness = 0
#         time.sleep(0.2)
#         pressedKey.brightness = original_brightness
#         time.sleep(0.2)

#     pressedKey.brightness = original_brightness

# def changePage():
    # Flash the buttons

    # Change the buttons page
#endregion





#region Main Program
last_key_pressed = 0
last_interaction_time = time.monotonic()
isIdle = False
isSleeping = False
setBrightness(DEFAULT_BRIGHTNESS)

while True:
    for key in keypad.keys:
        if key.is_pressed():
            setBrightness(DEFAULT_BRIGHTNESS)
            whenKeyIsPressed(key)

            # The animation blocks other actions from happening
            # Will work on making this a separate process in the future
            # flashSelectedKey(key)

            while key.is_pressed():
                key.brightness = 0.5
                pass

            last_interaction_time = time.monotonic()
            isIdle = False
            isSleeping = False
            last_key_pressed = key

        else:
            if(isIdle is False):   
                # Tried to implement key flashing, but it needs to be asynchronous :\
                # if((time.monotonic() - last_interaction_time) < 0.1 and last_key_pressed is not 0):
                    # flashSelectedKey(last_key_pressed)

                # If the keypad idles for 5 second, dim the lights!
                if((time.monotonic() - last_interaction_time) > idleTime ):
                    setBrightness(IDLE_BRIGHTNESS)
                    isIdle = True

            # Sleep if the keypad is idle for 5 minutes
            if(isSleeping is False):
                if((time.monotonic() - last_interaction_time) > sleepTime ):
                    setBrightness(0)
                    isSleeping = True
#endregion