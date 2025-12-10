import badger2040
import badger_os
import jpegdec
from math import ceil


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 0

TITLE_HEIGHT = 30
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

TITLE_TEXT_SIZE = 3

LEFT_PADDING = 5
NAME_PADDING = 20
LIST_TOP_PADDING = TITLE_HEIGHT + 15

TITLE = "hroar's hidden gear"

# State management
state = {
    'current': 0,
    'items': [
        # head
        "Gag",
        "Hypno",
        "Blindfold",
        "Collar",
        # body
        "Locks",
        "Clamps",
        "Mitts",
        "Rubber",
        # belt
        "Cage",
        "Padding",
        "Plug",
        # other
        "Other...",
    ],
    'checklist': [
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
        "[ ]",
    ],
}

badger_os.state_load("checklist", state)

changed = True

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
    display.set_pen(15)
    display.clear()

    # Draw a white background behind the name
    display.set_pen(0)
    display.rectangle(1, 1, TEXT_WIDTH, TITLE_HEIGHT)

    # Draw the TITLE
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("bitmap8")
    title_length = display.measure_text(title, TITLE_TEXT_SIZE)
    display.text(TITLE, (TEXT_WIDTH // 2) - ((title_length // 2) + LEFT_PADDING), LEFT_PADDING, WIDTH, TITLE_TEXT_SIZE)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    # display.set_font("bitmap14_outline")
    display.set_font("sans")

    n = 0
    x = LEFT_PADDING
    y = LIST_TOP_PADDING
    for index in range(len(state["items"])):
        display.text(f'{state["checklist"][index]}:{state["items"][index]}', x, y, WIDTH // 3, 0.57)
        n += 1
        y += NAME_HEIGHT // 4
        if n % 4 == 0:
            x += (WIDTH // 3) + 2
            y = LIST_TOP_PADDING

    display.update()


def button_switch():
    global changed
    display.set_update_speed(badger2040.UPDATE_NORMAL)
    i = state["current"]
    if state["checklist"][i] == "[ ]":
        state["checklist"][i] = "[X]"
    else:
        state["checklist"][i] = "[ ]"
    changed = True

def button_up():
    global changed
    display.set_update_speed(badger2040.UPDATE_TURBO)
    if state["current"] == 0:
        state["current"] = 11
    else:
        state["current"] -= 1
    changed = True

def button_down():
    global changed
    display.set_update_speed(badger2040.UPDATE_TURBO)
    if state["current"] == 11:
        state["current"] = 0
    else:
        state["current"] += 1
    changed = True

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
title = truncatestring(TITLE, TITLE_TEXT_SIZE, WIDTH)

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    if display.pressed(badger2040.BUTTON_C):
        button_switch()
    if display.pressed(badger2040.BUTTON_UP):
        button_up()
    if display.pressed(badger2040.BUTTON_DOWN):
        button_down()

    if changed:
        draw_badge()
        badger_os.state_save("checklist", state)
        changed = False
    # Sometimes a button press or hold will keep the system powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
