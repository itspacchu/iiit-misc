#!/usr/bin/python3
import os,subprocess
from PIL import Image,ImageEnhance
from time import sleep

SLEEP_TIME = 30

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


def epd(blackimg:str="./images/null.bmp",redimg:str="./images/null.bmp"):
    subprocess.run(["sudo","./epd", blackimg, redimg])

def render_webpage(url:str="https://smartcitylivinglab.iiit.ac.in/home/"):
    #chrome --headless --disable-gpu --screenshot --window-size=1280,1696 https://www.chromestatus.com/
    subprocess.run(['chromium','--headless','--disable-gpu','--screenshot','--window-size=480,800',url])
    webpage = Image.open("screenshot.png").convert("RGB").transpose(Image.ROTATE_90)
    webpage = change_contrast(webpage,100)
    #r = webpage.split()[0]
    #r.point( lambda p: 255 - (10*p) if ((p >= 200) and (p < 240)) else 255 ).convert("1").save("screenshot_r.bmp")
    webpage.convert("1").save("screenshot_b.bmp")
    epd("./screenshot_b.bmp")

if(__name__ == "__main__"):
    while(True):
        render_webpage("http://0.0.0.0:8000/")
        print(f"Refreshing screen in {SLEEP_TIME} seconds")
        sleep(SLEEP_TIME)
