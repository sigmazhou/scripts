import random
import time
from datetime import datetime
from pydirectinput import (
    keyDown,
    keyUp,
    move,
    moveRel,
    moveTo,
    mouseDown,
    mouseUp,
    press,
    leftClick,
    rightClick,
)

def main():
    time.sleep(10)
    while True:
        random_click_delay = random.random()
        random_sleep_time = random.uniform(60*12, 60*13)
        keyDown("space")
        time.sleep(random_click_delay)
        keyUp("space")
        print(f"jumped at {datetime.now()}")
        time.sleep(random_sleep_time)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
