#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

# __file__ is: /home/justus/quotes/src/quotes.py
# /home/justus/quotes/fonts
fontsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
# /home/justus/quotes/lib
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# import the rest of the modules
import logging
from PIL import Image,ImageDraw,ImageFont
import textwrap
import json
from string import ascii_letters
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # get quote, calculate placment and generate bitmap for all days of the year
        for i in range(1, 366):
            # padd zeros from the right
            padded_i = str(i).zfill(3)

            # get corresponding quote and author from json
            quote, author = get_quote(i)
            
            # calculate quote size, so that the quote has a height of approx. 300px            
            quote_wrapped, quote_font, author_font = calculate_font_size(quote)
    
            # drawing the quote and author to the screen
            generate_bit_map(padded_i, quote_wrapped, author, quote_font, author_font)

    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        exit()

def get_quote(index: int) ->  tuple[str, str]:
    logging.info("getting quote for day "+str(index))
    
    # open the json with quotes
    file = open("../../wise.json")
    data = json.load(file)

    quote = data[str(index)][0]
    author = data[str(index)][1]
    logging.debug("Quote: "+quote+" from: "+author)
    return quote, author

###########
# width = 600 pixel
# height = 448 pixel
# lower 270 pixels are reserved for authors
def calculate_font_size(quote: str) -> tuple[str, ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]: 
    # default values
    quote_fontsize = 70
    author_fontsize = 26
    
    quote_font = ImageFont.truetype(os.path.join(fontsdir, "LyonsSerif.ttf"), quote_fontsize)
    author_font = ImageFont.truetype(os.path.join(fontsdir, "LyonsSerif.ttf"), author_fontsize)


    # for char in ascii_letters:
    #     char_bbox = quote_font.getbbox(char)
    #     char_width = char_bbox[2] - char_bbox[0]
    #     char_height = char_bbox[3]
    #     print("width: "+ str(char_width)+" height: "+str(char_height))
    #     print("width: "+ str(quote_font.getsize(char)[0])+" height: "+str(quote_font.getsize(char)[1])+"\n")
    
    # Calculate the average length and  maximal height of a single character of our font.
    # Note: this takes into account the specific font and font size.
    while True:
        # default values
        sum_char_width = 0
        max_char_height = 0

        # loop through all letters in lower and capital cases
        for char in ascii_letters:
            char_bbox = quote_font.getbbox(char)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3]
            
            sum_char_width = sum_char_width + char_width
            # for the height use max value, for better results
            if char_height > max_char_height:
                max_char_height = char_height

        # calculate average char length to later calulate wraps
        avg_char_width = sum_char_width/ len(ascii_letters)

        # Translate this average length into a character count epd.width=600
        max_char_per_line = int(600 / avg_char_width)

        # preprocess text tp wrap around
        quote_wrapped = textwrap.fill(quote, width=max_char_per_line)
        
        # check if quote height is greater than 270px
        number_of_lines = quote_wrapped.count("\n")
        if (number_of_lines * max_char_height) < 270:
            return quote_wrapped, quote_font, author_font
        
        # if the quote height is too big ,decrement font size
        logging.debug("decrementing size by 2, current height is "+str(number_of_lines * max_char_height)+" and current font size is "+str(quote_fontsize))
        quote_fontsize = quote_fontsize - 2
        quote_font = ImageFont.truetype(os.path.join(fontsdir, "LyonsSerif.ttf"), quote_fontsize) 

def generate_bit_map(n: int, quote: str, author: str, quote_font: ImageFont.FreeTypeFont, author_font: ImageFont.FreeTypeFont):
    # initiate the drawing of the black frame
    image = Image.new('1', (600, 448), 255)
    draw = ImageDraw.Draw(image)

    logging.debug("drawing...")
    # Writing quote text
    draw.multiline_text((40,40), "\""+quote+"\"", font = quote_font, fill = 0, align = "left")
    
    # Writing author
    draw.multiline_text((40,350), author, font = author_font, fill = 0, align ="left")

    # saving to directory
    image.save("../../bmp/"+str(n)+".bmp")

if __name__ == '__main__':
    main()