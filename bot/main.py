# main.py

import pyautogui
import os
import time
import win32gui
import win32com.client
import numpy as np
import cv2
#import pytesseract
import subprocess
# modules
import controls
import vision
import header

# get into state loop
# add failsafe to recursion depth
def find_deadlock_window(depth):
    if depth == header.depth:
        return
    depth += 1
    
    # look for windows
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    
    if hwnds:
        print("Found Deadlock window.")
        return hwnds[0]
    else:
        print("Deadlock window not found.")
        subprocess.run(header.open_deadlock_steam, shell=True)
        time.sleep(7)
        find_deadlock_window(depth)


# look for a window with the name "Deadlock" and find the hwnd????? 
def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if title == "Deadlock" and class_name == "SDL_app":
            hwnds.append(hwnd)
    return True




def control_state(hwnd):
    # create hero networth data 
    heroes = header.create_entities()

    # load some stuff
    cwd = os.getcwd() 
    victory_template = np.array(cv2.imread("./templates/victory.png"))
    spectating_template = np.array(cv2.imread("./templates/spectating.png"))
    death_template = np.array(cv2.imread("./templates/0death.png"))
    update_template = np.array(cv2.imread("./templates/update.png"))
    # set foreground window
    win32gui.SetForegroundWindow(hwnd)

    # take a screenshot of the game once to check if update is needed
    screenshot = np.array(pyautogui.screenshot(region=(0, 0, 1920, 1080)))
    if(vision.check_game_update(screenshot, update_template)):
        print("game update needed")
        return

    # enter back into a game
    #controls.click_watch_tab()
    controls.move_to_watch_zone()
    # flags
    loading = True
    tophero = {"name": "", "nw": 0, "index": -1}

    # main event loop
    i = 0
    while True:
        # take a screenshot of the game
        screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        # save the screenshot for debugging
        filename = f'screenshot{i}.png'
        filepath = os.path.join(cwd, 'output', filename)
        screenshot.save(filepath)
        screenshot = np.array(screenshot)

        # analyze the frame
        
        # looking for "spectating" top left
        if loading:
            if vision.check_spec(screenshot, spectating_template):
                controls.change_spec_mode()
                loading = False
        else:
            # looking for victory
            if vision.check_game_end(screenshot, victory_template):
                controls.click_watch_tab()
                break
            # looking for 0 hp
            if vision.check_hero_death(screenshot, death_template):
                pyautogui.click()
            # find value of every hero networth
            heroes = vision.check_networth(screenshot, heroes)
            koth = max(heroes, key=lambda x: x['nw'])
            if tophero["name"] != koth["name"]:
                tophero = koth
                controls.move_to_hero(tophero)
            if tophero["nw"] <= koth["nw"]:
                tophero["nw"] = koth["nw"] 
        
        # hit tab every so often
        if i % 20 == 0:
            controls.hit_tab()
        # increment counter    
        i += 1

    # recursive until ctrl-c
    control_state(hwnd)


# default
def main():
    hwnd = find_deadlock_window(0)
    if hwnd:
        control_state(hwnd)

if __name__ == "__main__":
    main()

