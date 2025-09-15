# controls.py
# functions to execute pyautogui "macros"

import pyautogui
import time
# modules
import header


# pyautogui config
pyautogui.FAILSAFE = False

def move_to_watch_zone():
    print("moving to watch zone")
    # click past main menu
    pyautogui.click()
    time.sleep(1)
    #for _ in range(5):
    #    pyautogui.press("esc")
    #    time.sleep(0.1)
    # walk right
    pyautogui.keyDown('d')
    time.sleep(2)
    pyautogui.keyUp('d')
    # walk backwards
    pyautogui.keyDown('s')
    time.sleep(2)
    pyautogui.keyUp('s')
    # press e
    pyautogui.press('e')
    time.sleep(0.5)
    # enter game
    pyautogui.moveTo(200, 390)
    pyautogui.click()

def click_watch_tab():
    time.sleep(0.5)
    for _ in range(5):
        pyautogui.press("esc")
        time.sleep(0.1)
    pyautogui.moveTo(200, 390)
    pyautogui.click()
    time.sleep(2)
    pyautogui.click()


def change_spec_mode():
    #pyautogui.press("c")
    pyautogui.moveTo(1920, 540)


def back_to_main():
    time.sleep(0.5)
    pyautogui.press("esc")
    time.sleep(0.5)
    pyautogui.moveTo(200, 390)
    pyautogui.click()


def move_to_hero(koth):
    print(f"KOTH: {koth['name']}: {koth['nw']}") 
    pyautogui.keyDown("tab")
    pyautogui.moveTo(header.xpos_heroes[int(koth["index"])], 50)
    pyautogui.click()
    pyautogui.keyUp("tab")
    pyautogui.moveTo(1920, 540)
            

def hit_tab():
    pyautogui.keyDown("tab")
    time.sleep(1.5)
    pyautogui.keyUp("tab")
