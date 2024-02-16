import badger2040
import jpegdec


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 0

TITLE_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

TITLE_TEXT_SIZE = 4
DETAILS_TEXT_SIZE = 2

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "HELLO"
NAME = "hroar"
DETAIL = "MY NAME IS"

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

    # Draw the TITLE
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("bitmap8")
    title_length = display.measure_text(title, TITLE_TEXT_SIZE)
    display.text(title, (WIDTH - title_length) // 2, (TITLE_HEIGHT // 10) + 1, WIDTH, TITLE_TEXT_SIZE)

    # Draw a white backgrounds behind the details
    # display.set_pen(15)
    # display.rectangle(1, TITLE_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    # display.set_pen(0)
    detail_length = display.measure_text(detail, DETAILS_TEXT_SIZE)
    display.text(detail, (WIDTH - detail_length) // 2, TITLE_HEIGHT + (DETAILS_HEIGHT // 5), WIDTH, DETAILS_TEXT_SIZE)

    # Draw a white background behind the name
    display.set_pen(15)
    display.rectangle(1, TITLE_HEIGHT + DETAILS_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT + DETAILS_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    display.set_font("sans")
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(NAME, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(NAME, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + TITLE_HEIGHT + DETAILS_HEIGHT + (DETAILS_HEIGHT) // 2, WIDTH, name_size)
            break

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

detail = truncatestring(DETAIL, DETAILS_TEXT_SIZE, TEXT_WIDTH)

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    # Sometimes a button press or hold will keep the system powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()