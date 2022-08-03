#!/usr/bin/python3
import os,subprocess
from PIL import Image
from time import sleep

SLEEP_TIME = 30

def epd(blackimg:str="./images/null.bmp",redimg:str="./images/null.bmp"):
    subprocess.run(["sudo","./epd", blackimg, redimg])

def render_webpage(url:str="https://smartcitylivinglab.iiit.ac.in/home/"):
    #chrome --headless --disable-gpu --screenshot --window-size=1280,1696 https://www.chromestatus.com/
    subprocess.run(['chromium','--headless','--disable-gpu','--screenshot','--window-size=480,800',url])
    webpage = Image.open("screenshot.png").convert("RGB").transpose(Image.ROTATE_90)
    r = webpage.split()[0]
    r.point( lambda p: 255 - p if ((p > 100) and (p < 240)) else 255 ).convert("1").save("screenshot_r.bmp")
    webpage.convert("1").save("screenshot_b.bmp")
    epd("./screenshot_b.bmp","./screenshot_r.bmp")

if(__name__ == "__main__"):
    while(True):
        render_webpage("http://0.0.0.0:8000/")
        print(f"Refreshing screen in {SLEEP_TIME} seconds")
        sleep(SLEEP_TIME)
