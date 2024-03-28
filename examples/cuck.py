import badger2040
import jpegdec


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

TITLE_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

TITLE_TEXT_SIZE = 0.8
LINE_TEXT_SIZE = 0.55
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "cuckpuppy"
NAME = "hroar"
LINE_1 = "Let me watch"
LINE_2 = "Don't let me join"
LINE_3 = "I'll clean you up after"
DETAIL = "cuck.dog"
IMAGE = "images/cuck.jpg"

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

    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Draw the TITLE
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("sans")
    display.text(title, LEFT_PADDING + 25, (TITLE_HEIGHT // 2) + 1, WIDTH, TITLE_TEXT_SIZE)

    # Draw a white background behind the name
    display.set_pen(15)
    display.rectangle(1, TITLE_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT + DETAILS_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    display.set_font("serif_italic")
    name_size = 1.0  # A sensible starting scale
    name_length = display.measure_text(NAME, name_size)
    display.text(NAME, (TEXT_WIDTH - name_length) // 2, TITLE_HEIGHT + LEFT_PADDING + (DETAILS_HEIGHT) // 2, WIDTH, name_size)

    # Draw lines
    display.set_font("sans")
    line_no = 0
    for line in [LINE_1, LINE_2, LINE_3]:
        display.text(line, LEFT_PADDING + 2, TITLE_HEIGHT + 35 + line_no*(round((20*LINE_TEXT_SIZE)) + LEFT_PADDING), scale=LINE_TEXT_SIZE)
        line_no += 1

    # Draw a white backgrounds behind the details
    display.set_pen(15)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the detail's title and text
    display.set_pen(0)
    display.set_font("sans")
    detail_length = display.measure_text(detail, name_size)
    display.text(detail, (detail_length // 2),  (HEIGHT - (DETAILS_HEIGHT // 2)) - 1, WIDTH, DETAILS_TEXT_SIZE)

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
