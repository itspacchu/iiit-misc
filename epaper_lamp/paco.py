#!/usr/bin/python3
# The MIT License (MIT)

# Copyright (c) 2015 Prashant Nandipati (prashantn@riseup.net)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os,subprocess
from PIL import Image,ImageEnhance
from time import sleep
from multiprocessing  import Process
import os
from server import *
import requests
import logging


CONTRAST = 100

log = logging.getLogger(__name__)

SLEEP_TIME = 30


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


def epd(blackimg:str="./images/null.bmp",redimg:str="./images/null.bmp"):
    subprocess.run(["epd", blackimg, redimg])

def render_webpage(url:str="https://smartcitylivinglab.iiit.ac.in/home/"):
    #chrome --headless --disable-gpu --screenshot --window-size=1280,1696 https://www.chromestatus.com/
    subprocess.run(['chromium','--headless','--disable-gpu','--screenshot','--window-size=480,800','--no-sandbox',url])
    webpage = Image.open("screenshot.png").convert("RGB").transpose(Image.ROTATE_90)
    webpage = change_contrast(webpage,CONTRAST)
    #r = webpage.split()[0]
    #r.point( lambda p: 255 - (10*p) if ((p >= 200) and (p < 240)) else 255 ).convert("1").save("screenshot_r.bmp")
    webpage.convert("1").save("screenshot_b.bmp")
    epd("./screenshot_b.bmp")

if(__name__ == "__main__"):
    log.debug("Starting Flask Server in a different process")
    cds = Process(target=app.run,args=("0.0.0.0","8000"))
    cds.start()
    log.debug("Starting epaper display connection")
    while(True):
        try:
            log.debug("Connecting to flask server")
            render_webpage("http://0.0.0.0:8000/")
            log.debug(f"Refreshing screen in {SLEEP_TIME} seconds")
            sleep(SLEEP_TIME)
        except Exception as e:
            log.error(f"Exception {e} has occured \n Stopping Server process and epaper process")
            cds.join()
            log.error("exitting")
