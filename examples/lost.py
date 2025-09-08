import badger2040
import badger_os
import jpegdec


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


# State management
state = {
    "column": 0,
    "input": "text",  # text, number, punctuation, space
    "prefix": " Rm",  # Rm, @, :
    "char_1": "1",
    "char_2": "2",
    "char_3": "3",
    "char_4": "4",
    "char_5": "5",
    "char_6": "6",
    "char_7": "7",
    "char_8": "8",
    "char_9": "9",
    "char_10": "0",
    "char_11": "1",
    "char_12": "2",
    "char_13": "3",
    "char_14": "4",
    "char_15": "5",
    "char_16": "6",
    "char_17": "7",
    "char_18": "8",
    "char_19": "9",
}

badger_os.state_load("lost", state)

changed = True

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

TITLE_HEIGHT = 23
NAME_HEIGHT = 50
TEXT_HEIGHT = HEIGHT - (TITLE_HEIGHT + NAME_HEIGHT - 2)
TEXT_WIDTH = WIDTH - (IMAGE_WIDTH) - 1

TITLE_TEXT_SIZE = 0.64
NAME_TEXT_SIZE = 1.8
TEXT_SIZE = 2

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "This puppy is called..."
NAME = "hroar"
LABEL = "If lost, please return to"
IMAGE = "images/lost.jpg"

# ------------------------------
#      Utility functions
# ------------------------------


# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.set_pen(0)
    display.clear()

    # Draw badge image
    jpeg.open_file(IMAGE)
    jpeg.decode(WIDTH - IMAGE_WIDTH, 0)

    # Draw a white background behind the text
    display.set_pen(15)
    display.rectangle(1, TITLE_HEIGHT + NAME_HEIGHT, TEXT_WIDTH, HEIGHT - 1)

    # Line between title and name
    display.line(1, TITLE_HEIGHT, (WIDTH - IMAGE_WIDTH) + 26, TITLE_HEIGHT)

    # Draw the TITLE
    display.set_pen(15)
    display.set_font("sans")
    display.text(title, LEFT_PADDING - 1, (TITLE_HEIGHT // 2) + 1, WIDTH - IMAGE_WIDTH, TITLE_TEXT_SIZE)

    # Draw the NAME
    display.set_font("sans")
    display.text(NAME, NAME_PADDING + 1, TITLE_HEIGHT + (NAME_HEIGHT // 2) + 2, WIDTH - IMAGE_WIDTH, NAME_TEXT_SIZE)

    # Draw the main text
    display.set_pen(0)
    display.set_font("bitmap8")
    info = ""
    for x in range(1, len(state) - 3):
        info += state[f'char_{x}']
    text = f"{LABEL}{state['prefix']}{info}"
    display.text(text, LEFT_PADDING, TITLE_HEIGHT + NAME_HEIGHT + LEFT_PADDING - 1, wordwrap=((WIDTH - (IMAGE_WIDTH)) - (LEFT_PADDING * 2)), scale=TEXT_SIZE)

    display.update()


# ------------------------------
#        Buttons
# ------------------------------

def change():
    global changed
    display.set_update_speed(badger2040.UPDATE_TURBO)
    changed = True

def button_left():
    if int(state["column"]) in [0, "0"]:
        state["column"] = len(state) - 2
    else:
        state["column"] = str(int(state["column"]) - 1)

def button_right():
    if int(state["column"]) == len(state) - 3:
        state["column"] = "0"
    else:
        state["column"] = str(int(state["column"]) + 1)

def button_mid():
    if state["column"] not in [0, "0"]:
        col = state["column"]
        char = state[f"char_{str(col)}"]
        if state["input"] == "text":
            state["input"] = "number"
            char = "0"
        elif state["input"] == "number":
            state["input"] = "punctuation"
            char = "!"
        elif state["input"] == "punctuation":
            state["input"] = "space"
            char = " "
        elif state["input"] == "space":
            state["input"] = "text"
            char = "A"
        state[f"char_{str(col)}"] = char

def button_up():
    col = state["column"]
    # Change prefix
    if col in [0, "0"]:
        if state["prefix"] == " Rm":
            state["prefix"] = ": "
        elif state["prefix"] == ": ":
            state["prefix"] = " @"
        elif state["prefix"] == " @":
            state["prefix"] = " Rm"
    else:
        # Change column based on input type
        char = state[f"char_{col}"]
        if isinstance(char, int) or (char in digits):
            if char in [9, "9"]:
                char = "0"
            else:
                char = str(int(char) + 1)
        elif char in punctuation:
            if char == '~':
                char = "!"
            else:
                char = punctuation[punctuation.index(char) + 1]
        elif char in alphabet:
            if char == 'Z':
                char = "A"
            else:
                char = chr(ord(char) + 1)
        state[f"char_{col}"] = char

def button_down():
    col = state["column"]
    # Change prefix
    if col in [0, "0"]:
        if state["prefix"] == " Rm":
            state["prefix"] = " @"
        elif state["prefix"] == " @":
            state["prefix"] = ": "
        elif state["prefix"] == ": ":
            state["prefix"] = " Rm"
    else:
        # Change column based on input type
        char = state[f"char_{col}"]
        if isinstance(char, int) or (char in digits):
            if char in [0, "0"]:
                char = "9"
            else:
                char = str(int(char) - 1)
        elif char in punctuation:
            if char == '!':
                char = "~"
            else:
                char = punctuation[punctuation.index(char) - 1]
        elif char in alphabet:
            if char == 'A':
                char = "Z"
            else:
                char = chr(ord(char) - 1)
        state[f"char_{col}"] = char


# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

jpeg = jpegdec.JPEG(display.display)

# Truncate all of the text (except for the name as that is scaled)
title = truncatestring(TITLE, TITLE_TEXT_SIZE, TEXT_WIDTH)

# ------------------------------
#       Main program
# ------------------------------

while True:
    if display.pressed(badger2040.BUTTON_A):
        change()
        button_left()
    if display.pressed(badger2040.BUTTON_B):
        change()
        button_mid()
    if display.pressed(badger2040.BUTTON_C):
        change()
        button_right()
    if display.pressed(badger2040.BUTTON_UP):
        change()
        button_up()
    if display.pressed(badger2040.BUTTON_DOWN):
        change()
        button_down()

    if changed:
        draw_badge()
        badger_os.state_save("lost", state)
        changed = False
    # Sometimes a button press or hold will keep the system powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
