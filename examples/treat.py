import badger2040
import badger_os
import jpegdec
from math import ceil


# State management
state = {
    "name": "hroar",
    "food": "treats",
    "phrase": "(I promise I'm allowed chocolate)",
    "image": "treat1.jpg",
}
badger_os.state_load("treat", state)
changed = True

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 161

NAME_HEIGHT = 50
DETAILS_HEIGHT = HEIGHT - NAME_HEIGHT - 1
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

TITLE_TEXT_SIZE = 0.8
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 2
DETAIL_SPACING = 10

DETAIL = "Feed me "
IMAGE = "images/"

# ------------------------------
#      Utility functions
# ------------------------------

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
    jpeg.open_file(IMAGE + state["image"])
    jpeg.decode(WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Draw the NAME, scaling it based on the available width
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("sans")
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(state["name"], name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(state["name"], (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2), TEXT_WIDTH, name_size)
            break

    # Draw a white backgrounds behind the details
    display.set_pen(15)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the detail's title and text
    display.set_pen(0)
    display.set_font("sans")
    detail = DETAIL + state['food'] + "\n" + state['phrase']
    multiline_text(detail, LEFT_PADDING - 1, NAME_HEIGHT + 10, DETAILS_TEXT_SIZE, TEXT_WIDTH)

    display.update()


def button_switch():
    global changed
    if state.get("food") == "treats":
        state["food"] = "edibles"
        state["phrase"] = "(if I'm not gagged and still able to stand)"
        state["name"] = "hrrrr"
        state["image"] = "treat2.jpg"
    else:
        state["food"] = "treats"
        state["phrase"] = "(I promise I'm allowed chocolate)"
        state["name"] = "hroar"
        state["image"] = "treat1.jpg"
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

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    if display.pressed(badger2040.BUTTON_C):
        button_switch()

    if changed:
        draw_badge()
        badger_os.state_save("treat", state)
        changed = False

    # Sometimes a button press or hold will keep the system powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
