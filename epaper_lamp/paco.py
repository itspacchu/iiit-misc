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


# Settings

CONTRAST = 250
SLEEP_TIME = 300 #seconds


# Enable logging 
log = logging.getLogger(__name__)

"""
Point process constrast level on image
"""
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


"""
Wrapper for epd exec
blackimg= Image to show on black parts 
redimg= Image to show on red parts

Only Bitmap images of 1 bit color are supported
"""
def epd(blackimg:str="./images/null.bmp",redimg:str="./images/null.bmp"):
    subprocess.run(["epd", blackimg, redimg])

""" 
Render webpage
url : string input for url
"""
def render_webpage(url:str="https://smartcitylivinglab.iiit.ac.in/home/"):
    subprocess.run(['chromium','--headless','--disable-gpu','--screenshot','--window-size=480,800','--no-sandbox',url])
    webpage = Image.open("screenshot.png").convert("RGB").transpose(Image.ROTATE_90)
    webpage = change_contrast(webpage,CONTRAST)
    #r = webpage.split()[0]
    #r.point( lambda p: 255 - (10*p) if ((p >= 200) and (p < 240)) else 255 ).convert("1").save("screenshot_r.bmp")
    webpage.convert("1").save("screenshot_b.bmp")
    #epd("./images/null.bmp","./screenshot_b.bmp")
    epd(f"{os.getcwd()}/screenshot_b.bmp")
    os.remove(f"{os.getcwd()}/screenshot_b.bmp") # remove screenshots 

def start_save():
    os.system('bash -c "./camera_stream_saver.sh"')

def db_save():
    os.seteuid(1000)
    os.system('./db_save.sh')
"""
main event loop
"""
if(__name__ == "__main__"):
    log.debug("Starting Flask Server in a different process")
    cds = Process(target=app.run,args=("0.0.0.0","8000"))
    log.debug("Starting Camera Stream saver")
    csv = Process(target=start_save)

    # Handle multiple processes
    log.debug("\n\n-- Starting multiple processes to handle things --\n\n")
    csv.start()
    cds.start()
    
    # Event Loop
    log.debug("Starting epaper display connection")
    while(True):
        try:
            log.debug("Connecting to flask server")
            render_webpage("http://0.0.0.0:8000/")
            log.debug(f"Refreshing screen in {SLEEP_TIME} seconds")
            sleep(SLEEP_TIME)
            render_webpage("http://0.0.0.0:8000/w")
            sleep(SLEEP_TIME)
        except Exception as e:
            log.error(f"Exception {e} has occured \n Stopping Server process and epaper process")
            cds.join()
            csv.join()
            log.error("exitting")
