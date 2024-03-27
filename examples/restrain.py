import badger2040
import jpegdec


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 49

TITLE_TEXT_SIZE = 0.9
DETAIL_TEXT_SIZE = 0.6

TITLE_HEIGHT = round(30*TITLE_TEXT_SIZE)
TEXT_WIDTH = WIDTH - (IMAGE_WIDTH) - 1

LEFT_PADDING = 6
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "PATIENT, HROAR"
DETAIL_1 = "DR. SCHMITT"
DETAIL_2 = "DOB:   2024-04-06"
DETAIL_3 = "Hilton Sanitarium Rm #"
DETAIL_4 = "KEEP MUZZLED"
DETAIL_5 = "KEEP RESTRAINED"
IMAGE = "images/barcode.jpg"

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

    # Draw left badge image
    jpeg.open_file(IMAGE)
    jpeg.decode(0, 0)

    # Draw a white background
    display.set_pen(15)
    display.rectangle(IMAGE_WIDTH, 0, TEXT_WIDTH + 1, HEIGHT)

    # Draw the TITLE
    display.set_pen(0)
    display.set_thickness(3)
    display.set_font("sans")
    display.text(title, IMAGE_WIDTH + LEFT_PADDING + 1, TITLE_HEIGHT // 2, WIDTH, TITLE_TEXT_SIZE)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    display.set_thickness(2)
    display.set_font("sans")
    line = 0
    for detail in [DETAIL_1, DETAIL_2, DETAIL_3, DETAIL_4, DETAIL_5]:
        display.text(detail, IMAGE_WIDTH + LEFT_PADDING + 2, TITLE_HEIGHT + LEFT_PADDING + 2 + line*(round((22*DETAIL_TEXT_SIZE)) + LEFT_PADDING), scale=DETAIL_TEXT_SIZE)
        line += 1

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
