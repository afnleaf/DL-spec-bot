# test.py
# test harness for the computer vision functions in vision.py
# images used for testing found in the test folder

import pyautogui
import os
import time
import numpy as np
import cv2
import pytesseract
import subprocess
# modules
import controls
import vision
import header

'''
there are a few main vision functions we must test
- game update
- spectating
- victory screen
- player death
- hero networths
'''
def run_tests():
    update_result = "✅" if test_game_update() else "❌"
    print(f"{update_result} game update")
    
    spec_result = "✅" if test_spectating() else "❌"
    print(f"{spec_result} spectating")

    victory_result = "✅" if test_victory() else "❌"
    print(f"{victory_result} victory")

    death_result = "✅" if test_death() else "❌"
    print(f"{death_result} player death")

    networth_result = "✅" if test_networth() else "❌"
    print(f"{networth_result} networth")
    


def test_game_update():
    update_template = np.array(cv2.imread("./templates/update.png"))
    filename = f'update (1).png'
    image = get_image(filename)

    return vision.check_game_update(image, update_template)


def test_spectating():
    spectating_template = np.array(cv2.imread("./templates/spectating.png"))
    
    #filename = f'spectating ({i}).png'
    filename = f'spectating (1).png'
    image = get_image(filename)

    return vision.check_spec(image, spectating_template) 


def test_victory():
    victory_template = np.array(cv2.imread("./templates/victory.png"))
    
    filename = f'victory (1).png'
    image = get_image(filename)

    return vision.check_game_end(image, victory_template)

def test_death():
    death_template = np.array(cv2.imread("./templates/0death.png"))
    
    filename = f'death (1).png'
    image = get_image(filename)

    return vision.check_hero_death(image, death_template)


def test_networth():
    
    # can reuse the other screenshots
    filename = f'spectating (1).png'
    image = get_image(filename)

    heroes = header.create_entities()
    heroes = vision.check_networth(image, heroes)
    print(heroes)

    nw = [
        {'name': 'a1', 'nw': 16, 'index': 0}, 
        {'name': 'a2', 'nw': 13, 'index': 1}, 
        {'name': 'a3', 'nw': 14, 'index': 2}, 
        {'name': 'a4', 'nw': 12, 'index': 3}, 
        {'name': 'a5', 'nw': 14, 'index': 4}, 
        {'name': 'a6', 'nw': 0, 'index': 5}, 
        {'name': 's1', 'nw': 0, 'index': 6}, 
        {'name': 's2', 'nw': 0, 'index': 7}, 
        {'name': 's3', 'nw': 14, 'index': 8}, 
        {'name': 's4', 'nw': 17, 'index': 9}, 
        {'name': 's5', 'nw': 7, 'index': 10}, 
        {'name': 's6', 'nw': 0, 'index': 11}
    ]

    return True if heroes == nw else False


    

# get image from given filename
# repeated a lot
def get_image(filename):
    cwd = os.getcwd() 
    image_path = os.path.join(cwd, 'test', filename)
    image = cv2.imread(image_path)
    return image

    



# default
def main():
    run_tests()
    

if __name__ == "__main__":
    main()

