# E-Paper Quote Display (german)
This project utilizes a 5.83-inch black and white E-Paper display from Waveshare, driven by a Raspberry Pi.
The display is designed to show a different quote every day, primarily in German. The project consists of generating the required bitmaps using the [generateBitMaps.py](./python/scripts/generateBitMap.py) script, and then displaying the quotes on the E-Paper. 

For that to you can compile a C programm found [here](./c/src/main.c) or use the Python script found [here](./python/scripts/showQuotes.py).

WARNING! The C programm doesn’t work currently, the display does not change.

## Installation

To set up the E-Paper display project, follow the steps below:
### Prerequisites

    Raspberry Pi with an operating system installed (e.g., Raspbian)
    Python 3.x installed on the Raspberry Pi
    Waveshare 5.83 inch E-Paper display
      https://www.waveshare.com/5.83inch-e-Paper.htm

    Optional (but recommended):
    E-Paper with a HAT to drive it, found

### Links:

  - [E-Paper](https://www.waveshare.com/5.83inch-e-Paper.htm)
  - [E-Paper with HAT](https://www.waveshare.com/5.83inch-e-paper-hat.htm)

### Hardware Setup

    Connect the Waveshare E-Paper display to the Raspberry Pi following the manufacturer's instructions. https://www.waveshare.com/wiki/5.83inch_e-Paper_HAT_Manual#C

## Usage

Clone or download the project repository to your Raspberry Pi

    git clone <repository_url>

Navigate to the project directory.

    cd <project_directory>

Install the required Python packages by navigating to the python directory and installing required dependecies:

    pip install setup.py

Generate the bitmaps required for displaying the quotes using the generateBitMaps.py script. This script will generate bitmap files for each entry in the [quotes json file](./wise.json).

    python generateBitMaps.py

All 365 bitmaps should be in the /bmp folder

Option 1: Compile the C program using the provided Makefile in the C directory.

    sudo make clean
    sudo make
    sudo ./epd

Option 2: Run the Python script directly.

    python showQuotes.py

## ToDo

  - enclosure for the photo frame, 3D printing

## Acknowledgments

The E-Paper display is manufactured by Waveshare. Visit their website for more information about the display and additional resources.
This project was inspired by the idea of displaying daily quotes and is meant for educational purposes.