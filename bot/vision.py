import cv2
import numpy as np
import pytesseract
import re
# modules
import header


# load tesseract-ocr model
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config_psm = "--oem 3 --psm 7 -c tessedit_char_whitelist=k.0123456789"


def check_game_update(image, template):
    print("check game update")

    # crop
    #x, y, w, h = 450, 770, 40, 40
    x, y, w, h = 15, 10, 315, 75
    image = image[y:y+h, x:x+w]
    # grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # bitwise not
    image = cv2.bitwise_not(image)
    # contrast / brightness control
    alpha = 1
    beta = 0
    # call convertScaleAbs function
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    #thresholding 
    _,image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    cv2.imwrite(f"./o/update.png", image)

    # ensure template is grayscale
    if len(template.shape) > 2:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)    
    
    # ensure both image and template are CV_8U
    image = image.astype(np.uint8)
    template = template.astype(np.uint8)
    
    # template match
    try:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        
        # define a threshold for matching
        match_threshold = 0.8
        
        if max_val >= match_threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            #cv2.imwrite(f"./o/result{i}.png", image)
            print(f"Game update Match found with confidence: {max_val}")
            return True
        else:
            #print(f"No match found. Best match confidence: {max_val}")
            return False
    except cv2.error as e:
        print(f"OpenCV Error: {str(e)}")
        return False


def check_game_end(image, template):
    print("check game end")

    # crop
    #x, y, w, h = 730, 500, 450, 135
    x, y, w, h = 610, 465, 690, 200

    image = image[y:y+h, x:x+w]
    # grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # bitwise not
    image = cv2.bitwise_not(image)
    # contrast / brightness control
    alpha = 1.6
    beta = 0
    # call convertScaleAbs function
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    # thresholding
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   
    cv2.imwrite(f"./o/victory.png", image)


    # ensure template is grayscale
    if len(template.shape) > 2:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)    
    
    # ensure both image and template are CV_8U
    image = image.astype(np.uint8)
    template = template.astype(np.uint8)
    
    # template match
    try:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        
        # define a threshold for matching
        match_threshold = 0.8
        
        if max_val >= match_threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            #cv2.imwrite(f"./o/result{i}.png", image)
            print(f"Game end Match found with confidence: {max_val}")
            return True
        else:
            #print(f"No match found. Best match confidence: {max_val}")
            return False
    except cv2.error as e:
        print(f"OpenCV Error: {str(e)}")
        return False


def check_spec(image, template):
    print("check spec")

    # crop
    x, y, w, h = 18, 21, 80, 18
    image = image[y:y+h, x:x+w]

    cv2.imwrite(f"./o/spec.png", image)

    # grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # bitwise not
    image = cv2.bitwise_not(image)
    
    # contrast / brightness control
    #alpha = 6
    #beta = 11
    alpha = 1.6
    beta = 0
    # call convertScaleAbs function
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    #thresholding
    _,image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite(f"./o/spec_after.png", image)

    # ensure template is grayscale
    if len(template.shape) > 2:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # ensure both image and template are CV_8U
    image = image.astype(np.uint8)
    template = template.astype(np.uint8)

    # template match
    try:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # define a threshold for matching
        match_threshold = 0.8

        if max_val >= match_threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            #cv2.imwrite(f"./o/result{i}.png", image)
            print(f"Spectating found with confidence: {max_val}")
            return True
        else:
            #print(f"No match found. Best match confidence: {max_val}")
            return False
    except cv2.error as e:
        print(f"OpenCV Error: {str(e)}")
        return False


def check_hero_death(image, template):
    print("check death")

    # crop
    #x, y, w, h = 450, 770, 40, 40
    x, y, w, h = 475, 750, 40, 40
    image = image[y:y+h, x:x+w]
    # grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # bitwise not
    image = cv2.bitwise_not(image)
    cv2.imwrite(f"./o/death.png", image)
    
    # contrast / brightness control
    #alpha = 6
    #beta = 11
    alpha = 1.6
    beta = 0
    # call convertScaleAbs function
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    #thresholding
    _,image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ensure emplate is grayscale
    if len(template.shape) > 2:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # ensure both image and template are CV_8U
    image = image.astype(np.uint8)
    template = template.astype(np.uint8)

    # template match
    try:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # define a threshold for matching
        match_threshold = 0.8

        if max_val >= match_threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            #cv2.imwrite(f"./o/result{i}.png", image)
            print(f"Death found with confidence: {max_val}")
            
            return True
        else:
            #print(f"No match found. Best match confidence: {max_val}")
            return False
    except cv2.error as e:
        print(f"OpenCV Error: {str(e)}")
        return False


def process_image(image):
    #print("process image")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, y = image.shape[::-1]
    # resize 2x
    image = cv2.resize(image, (0,0), fx=5, fy=5)
    # invert
    image = cv2.bitwise_not(image)
   
    # contrast / brightness control
    alpha = 2.2
    beta = 0 
    # call convertScaleAbs function
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    #thresholding 
    _,image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
    return image


def check_networth(image, heroes):
    print("check networth")

    # width, height and y pos are static
    # w/h are the size of the box around networth
    # y is where the first box starts on the y axis
    #w, h, y = 38, 20, 105
    w, h, y = 32, 18, 86
    
    for i, x in enumerate(header.xpos_heroes):
        net = image[y:y+h, x:x+w]
        net = process_image(net)
        cv2.imwrite(f"o/net{i+1}.png", net)
        text = pytesseract.image_to_string(net, config=config_psm)
        text = text.strip()
        text = text.replace(" ", "")
        #print(text)
        if bool(re.search(r'\d', text)):
            # multiple value by 1000 because of k
            value = 0
            k_index = text.find("k")
            if k_index != -1:
                sliced_text = text[:k_index] + text[k_index+1:]
                sliced_text = sliced_text.removesuffix(".")
                if sliced_text:
                    value = int(float(sliced_text) * 1000)
            else:
                text = text.removesuffix(".")
                value = int(float(text))
              
            heroes[i]["nw"] = value
            #text = process_code_mode1(net)
            #print(text)
    
    return heroes
