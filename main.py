import pyautogui
import time


# Function to detect if the game is in inverted mode (white background)
def is_inverted_mode(background_sample_region, threshold=250):
    screenshot = pyautogui.screenshot(region=background_sample_region)
    grayscale = screenshot.convert("L")

    # Calculate the average brightness in the background region
    avg_brightness = sum(
        grayscale.getpixel((x, y)) for x in range(grayscale.width) for y in range(grayscale.height)) / (
                                 grayscale.width * grayscale.height)

    return avg_brightness > threshold


# Function to detect obstacles based on mode (bright vs dark pixels)
def detect_obstacle(region, inverted_mode=False):
    screenshot = pyautogui.screenshot(region=region)
    grayscale = screenshot.convert("L")

    # Set detection threshold based on mode
    threshold = 100 if inverted_mode else 150
    pixel_count = 0
    required_pixel_count = 43  # Adjust for sensitivity

    # Count pixels meeting threshold criteria
    for x in range(grayscale.width):
        for y in range(grayscale.height):
            if grayscale.getpixel((x, y)) < threshold if inverted_mode else grayscale.getpixel((x, y)) > threshold:
                pixel_count += 1

    return pixel_count > required_pixel_count


def jump():
    pyautogui.press("space")


def duck():
    pyautogui.keyDown("down")
    time.sleep(0.3)
    pyautogui.keyUp("down")


# Define regions for ground and flying obstacles, and background sampling
ground_region = (235, 280, 130, 30)
flying_region = (235, 240, 130, 30)
background_region = (50, 280, 50, 30)

print("Starting in 3 seconds...")
time.sleep(3)

while True:
    # Check if the game is in inverted mode by sampling the background color
    inverted_mode = is_inverted_mode(background_region)

    # Detect ground or flying obstacles based on current mode
    if detect_obstacle(ground_region, inverted_mode=inverted_mode):
        jump()
        time.sleep(0.02)  # Small delay to prevent multiple jumps per obstacle
    elif detect_obstacle(flying_region, inverted_mode=inverted_mode):
        duck()
        time.sleep(0.02)  # Small delay to avoid multiple ducks per obstacle

    # Frequency for checking obstacles based on game speed
    time.sleep(0.01)
