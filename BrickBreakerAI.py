import pyautogui
from PIL import ImageGrab
import time
import keyboard

# Function to move the mouse to a specified position
def move_mouse(x, y):
    pyautogui.moveTo(x, y)

# Function to get the color of a pixel at a specified position
def get_pixel_color(x, y):
    screenshot = ImageGrab.grab()
    return screenshot.getpixel((x, y))

# Function to find the ball's x position t(assumes ball is red)
def find_ball_x(screen_width, screen_height):
    screenshot = ImageGrab.grab()
    for y in range(screen_height-1,screen_height//5,-2):
        for x in range(screen_width):
            r, g, b = screenshot.getpixel((x, y))
            # if r == 224 and g == 226 and b == 226: #background color
            #     return x
            # if r == 87 and g == 78 and b == 101: #ball dark color
            #     return x
            if r == 96 and g == 87 and b == 110: #ball and power up color
                return x

    return None

running = False
def toggle_running():
    global running
    running = not running
    if running:
        print("Program started")
    else:
        print("Program stopped")
keyboard.add_hotkey('t', toggle_running)

if __name__ == "__main__":
    screen_width, screen_height = pyautogui.size()
    
    print("Press 't' to start/stop the program")

    while True:
        if running:
            ball_x = find_ball_x(screen_width, screen_height)
            if ball_x is not None:
                print("True")
                move_mouse(ball_x, screen_height - 300)  # Move paddle to the ball's x position
            else:
                print("False")
        #time.sleep(0.001)  # Adjust as necessary to control the speedttt