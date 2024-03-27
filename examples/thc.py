import badger2040
import jpegdec


# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

TITLE_HEIGHT = 30
NAME_HEIGHT = HEIGHT - TITLE_HEIGHT - 2
TEXT_WIDTH = WIDTH - (IMAGE_WIDTH) - 1

TITLE_TEXT_SIZE = 0.9

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

TITLE = "hroar"
NAME = "WARNING. This puppy contains THC. This puppy has not been analyzed or approved by the FDA. There is limited information on the side effects of using this puppy, and there may be associated health risks. Marijuana use during pregnancy and breastfeeding may pose potential harms. It is against the law to drive or operate machinery when under the influence of this puppy. KEEP THIS PUPPY AWAY FROM CHILDREN."
IMAGE_THC = "images/thc.jpg"

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
    jpeg.open_file(IMAGE_THC)
    jpeg.decode(0, 0)

    # Draw a border around the images
    display.set_pen(0)
    # Left image
    display.line(0, 0, IMAGE_WIDTH + 1, 0)
    display.line(0, 0, 0, HEIGHT - 1)
    display.line(0, HEIGHT - 1, IMAGE_WIDTH + 1, HEIGHT - 1)
    display.line(IMAGE_WIDTH + 1, 0, IMAGE_WIDTH + 1, HEIGHT - 1)

    # Draw the TITLE
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("sans")
    display.text(title, IMAGE_WIDTH + LEFT_PADDING + 1, TITLE_HEIGHT // 2, WIDTH, TITLE_TEXT_SIZE)

    # Draw a white background behind the name
    display.set_pen(15)
    display.rectangle(IMAGE_WIDTH + 1, TITLE_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.set_pen(0)
    display.set_font("bitmap6")
    name_size = 0.4  # A sensible starting scale
    display.text(NAME, IMAGE_WIDTH + LEFT_PADDING, (TITLE_HEIGHT) + LEFT_PADDING, wordwrap=((WIDTH - (IMAGE_WIDTH)) - (LEFT_PADDING * 2)), scale=name_size)

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
