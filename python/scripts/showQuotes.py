#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

# /home/justus/quotes/lib
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# 
dir = os.path.dirname(os.path.realpath(__file__))
print(dir)

# import the rest of the modules
import logging
from datetime import date
from waveshare_epd import epd5in83
from PIL import Image
logging.basicConfig(level=logging.DEBUG)

def main():
    try:
        global epd; epd = epd5in83.EPD()           #get the display
        logging.info("init and clear")         
        epd.init()                                 #init the display
        epd.Clear()

        #getting todays day of the year
        dayOfYear = date.today().strftime('%j')

        #drawing the quote and author to the screen
        writeScreen(dayOfYear)

        #exiting into sleep
        logging.info("Goto Sleep...")
        epd.sleep()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd5in83.epdconfig.module_exit()
        exit()

def writeScreen(number_day: int):
    #initiate the drawing of the black frame
    image = Image.new('1', (epd.width, epd.height), 255)
    image = Image.open(os.path.join("/home/justus/quotes/bmp/", str(number_day)+".bmp"))

    #output to the display
    logging.info("drawing to screen")
    epd.display(epd.getbuffer(image))

if __name__ == '__main__':
    main()