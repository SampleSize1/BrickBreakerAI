import pyautogui
import mss
import numpy as np
import time
import keyboard

# Function to move the mouse to a specified position
def move_mouse(x, y):
    pyautogui.moveTo(x, y)

# Function to get the color of a pixel at a specified position using mss
def get_pixel_color(img, x, y):
    return img[y, x]

# Function to find the ball's x position (assumes ball is red)
def find_ball_x(img):
    # Extract RGB channels
    r, g, b, _ = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
    
    # Condition to detect red color
    mask = (r > 200) & (g < 50) & (b < 50)
    
    # Find the x coordinates of the red pixels
    red_pixels = np.where(mask)
    
    if red_pixels[0].size > 0:
        # Return the x coordinate of the first red pixel found
        return red_pixels[1][0]
    return None

# Variable to keep track of whether the program is running
running = False

# Function to toggle the running state
def toggle_running():
    global running
    running = not running
    if running:
        print("Program started")
    else:
        print("Program stopped")

# Bind the 't' key to toggle the running state
keyboard.add_hotkey('t', toggle_running)

if __name__ == "__main__":
    screen_width, screen_height = pyautogui.size()
    
    print("Press 't' to start/stop the program")

    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
        
        while True:
            if running:
                # Capture screen
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)

                # Find the ball's x position
                ball_x = find_ball_x(screen_width, screen_height, img)
                if ball_x is not None:
                    print("True")
                    move_mouse(ball_x, screen_height - 300)  # Move paddle to the ball's x position
                else:
                    print("False")
                
            time.sleep(0.01)  # Adjust as necessary to control the speed