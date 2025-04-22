import badger2040
import jpegdec
from math import ceil


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

TITLE_HEIGHT = 30
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

TITLE_TEXT_SIZE = 0.8

LEFT_PADDING = 5
NAME_PADDING = 20

TITLE = "hroar"
NAME = "ASK TO PET"
IMAGE = "images/pet.jpg"

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
    for line in text.split('\n'):
        for word in line.split():
            if x + display.measure_text(word, text_size) >= width - 1:
                x = x_start
                y += ceil(30 * text_size)
            word += ' '
            display.text(word, x, y, width, text_size)
            x += display.measure_text(word, text_size)
        x = x_start
        y += ceil(30 * text_size) + 4


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

    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Draw a white background behind the name
    display.set_pen(15)
    display.rectangle(1, 1, TEXT_WIDTH, TITLE_HEIGHT)

    # Draw the TITLE
    display.set_pen(0)  # Change this to 0 if a white background is used
    display.set_font("sans")
    display.text(title, LEFT_PADDING + 56, (TITLE_HEIGHT // 2), WIDTH, TITLE_TEXT_SIZE)

    # Draw the name, scaling it based on the available width
    display.set_pen(15)
    # display.set_font("bitmap14_outline")
    display.set_font("sans")
    text = "   ASK TO PET \nI'M WORKING"
    multiline_text(text, LEFT_PADDING, TITLE_HEIGHT*2, 0.95, WIDTH)
    # name_size = 5.0  # A sensible starting scale
    # while True:
    #     name_length = display.measure_text(NAME, name_size)
    #     if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
    #         name_size -= 0.01
    #     else:
    #         display.text(NAME, (TEXT_WIDTH - name_length) // 2, TITLE_HEIGHT * 2, WIDTH, name_size, spacing=0)
    #         break

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
