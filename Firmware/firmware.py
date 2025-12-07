import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.extensions.media_keys import MediaKeys


keyboard = KMKKeyboard()
keyboard.modules.append(MediaKeys())

# LED initialize
led = digitalio.DigitalInOut(board.SDA)
led.direction = digitalio.Direction.OUTPUT

# LED off by default
led.value = False
is_muted = False
PINS = [
    # Top row
    board.D1,   # 1 - GPIO01
    board.D2,   # 2 - GPIO02
    board.D3,   # 3 - GPIO03
    
    # Middle row
    board.D4,   # 4 - GPIO04
    board.D27,  # 5 - GPIO27
    board.D26,  # 6 - GPIO26
    
    # Bottom row
    board.D7,   # 7 - GPIO07
    board.D28,  # 8 - GPIO28
    board.D29,  # 9 - GPIO29
    
    # Extra key
    board.D0,   # 0 - GPIO00
]

# Default numpad mapping
NUMPAD_KEYS = [
    KC.KP_1,     # Key 1 - Top Left
    KC.KP_2,     # Key 2 - Top Middle  
    KC.KP_3,     # Key 3 - Top Right
    KC.KP_4,     # Key 4 - Middle Left
    KC.KP_5,     # Key 5 - Middle Middle
    KC.KP_6,     # Key 6 - Middle Right
    KC.KP_7,     # Key 7 - Bottom Left
    KC.KP_8,     # Key 8 - Bottom Middle
    KC.KP_9,     # Key 9 - Bottom Right
    KC.KP_0,     # Key 0 - Bottom Centered
]

# Media control mapping
MEDIA_KEYS = [
    KC.MPRV,     # Key 1 - Play/Pause
    KC.MNXT,     # Key 2 - Next Track
    KC.MPLY,     # Key 3 - Previous Track
    KC.VOLU,     # Key 4 - Volume Up
    KC.VOLD,     # Key 5 - Volume Down
    KC.MUTE,     # Key 6 - Mute
    KC.MRWD,  # Key 7 - Fast Forward
    KC.MFFD,  # Key 8 - Rewind
    KC.MYCM,  # Key 9 - File Manager
    KC.LWIN(KC.L),     # Key 0 - Lock Computer
]

# Function key mapping  
FUNCTION_KEYS = [
    KC.F1, KC.F2, KC.F3,
    KC.F4, KC.F5, KC.F6,
    KC.F7, KC.F8, KC.F9,
    KC.F10,
]


class MuteKey(KC):
    def __init__(self):
        super().__init__()
        self.is_muted = False
    
    def on_press(self, keyboard, *args, **kwargs):
        global is_muted
        is_muted = not is_muted
        led.value = is_muted 
        KC.MUTE.on_press(keyboard, *args, **kwargs)
        status = "MUTED" if is_muted else "UNMUTED"
        print(f"System {status} - LED {'ON' if is_muted else 'OFF'}")


SELECTED_KEYMAP = MEDIA_KEYS  


keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

keyboard.keymap = [SELECTED_KEYMAP]

if __name__ == '__main__':
    print("- " * 50)
    print("MACRO PAD FIRMWARE")
    print("- " * 50)
    print("LED Behavior:")
    print("  - Both LEDs OFF when system UNMUTED")
    print("  - Both LEDs ON (70%) when system MUTED")
    print()
    print("Key Layout (3x3 grid + bottom center):")
    print("[1][2][3]")
    print("[4][5][6]") 
    print("[7][8][9]")
    print("  [0]")
    print()
    print("Current keymap: Media") #change as needed
    print("- " * 50)
    
    # Start with LED OFF
    led.value = False
    
    keyboard.go()