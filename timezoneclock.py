#!/usr/bin/python

from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment as 7seg
from Adafruit_LED_Backpack import AlphaNum4 as alphanum
import os
import time
import RPi.GPIO as GPIO

# Initializes Timezone Variables
offset = 0

# Creates displays
7segdisplay = 7seg.SevenSegment(address=0x70)
alphadisplay = alphanum.AlphaNum4(address=0x71)

# Begins displays
7segdisplay.begin()
alphadisplay.begin()

# Loop for starting displays
while(True):
    # Sets Time
    utctime = datetime.utcnow()
    hour = utctime.hour + offset
    minute = utctime.minute
    second = utctime.second

    # Clear Display
    7segdisplay.clear()

    7segdisplay.set_colon(second % 2)
