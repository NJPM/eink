import badger2040
import jpegdec
from math import ceil


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT


TITLE_HEIGHT = 30
DETAILS_HEIGHT = 43
QR_HEIGHT = 42
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH

TITLE_TEXT_SIZE = 1.3
DETAILS_TEXT_SIZE = 0.54

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "HROAR"
NAME = "FREE USE PUPPY \n WRECK MY TAIL PLZ"
DETAIL = "Sorry if I'm nonverbal, but I do consent and my zip is open"


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


def multiline_text(text: str, x_start: int, y_start: int, text_size: float, width: int):
    x = x_start
    y = y_start
    y_factor = 28
    for line in text.split('\n'):
        for word in line.split():
            if x + display.measure_text(word, text_size) >= width - 1:
                x = x_start
                y += ceil(y_factor * text_size)
            word += ' '
            display.text(word, x, y, width, text_size)
            x += display.measure_text(word, text_size)
        x = x_start
        y += ceil(y_factor * text_size) + 4


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.set_pen(0)
    display.clear()

    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH, 0, WIDTH, HEIGHT - 1)
    display.line(WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Draw a white background behind the name
    display.set_pen(15)
    display.rectangle(1, 1, TEXT_WIDTH, TITLE_HEIGHT)

    # Draw the TITLE
    display.set_pen(0)  # Change this to 0 if a white background is used
    display.set_font("sans")
    title_text_width = display.measure_text(TITLE, TITLE_TEXT_SIZE)
    display.text(title, ((TEXT_WIDTH - title_text_width) // 2) - LEFT_PADDING, (TITLE_HEIGHT // 2) + 2, WIDTH, TITLE_TEXT_SIZE)

    # Draw the name, scaling it based on the available width
    display.set_pen(15)
    # display.set_font("bitmap14_outline")
    display.set_font("sans")
    multiline_text(NAME, LEFT_PADDING * 5, TITLE_HEIGHT + 14, 0.8, WIDTH)

    # Draw a white backgrounds behind the details
    display.set_pen(15)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the detail's title and text
    display.set_pen(0)
    display.set_font("sans")
    multiline_text(DETAIL, LEFT_PADDING, (HEIGHT - DETAILS_HEIGHT) + 13, DETAILS_TEXT_SIZE, TEXT_WIDTH)


    display.update()


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

draw_badge()

while True:
    # Sometimes a button press or hold will keep the system powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
