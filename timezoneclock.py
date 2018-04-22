#!/usr/bin/pythoon3

from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment as sseg
from Adafruit_LED_Backpack import AlphaNum4 as alphanum
import os
import time
import asyncio
import RPi.GPIO as GPIO

# Init Timezone Variables
offset = 0

# Init GPIO for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Creates displays
ssegdisplay = sseg.SevenSegment(address=0x70)
alphadisplay = alphanum.AlphaNum4(address=0x71)

# Begin and reset display
ssegdisplay.begin()
ssegdisplay.clear()
ssegdisplay.write_display()

alphadisplay.begin()
alphadisplay.clear()
alphadisplay.write_display()

# Loop for starting displays
async def settime():
    # Sets Time
    utctime = datetime.utcnow()
    hour = utctime.hour + offset
    minute = utctime.minute
    second = utctime.second
    
    # Clear Display
    ssegdisplay.clear()
    
    ssegdisplay.set_colon(second % 2)
    
    ssegdisplay.write_display()
    
    await asyncio.sleep(0.25)

async def buttons():
    if GPIO.input(18) == False:
        print('Left button pressed')
        await asyncio.sleep(0.1)

while(True):
    asyncloop = asyncio.get_event_loop()
    tasks = [asyncloop.create_task(settime()), asyncloop.create_task(buttons())]
    wait_tasks = asyncio.wait(tasks)
    asyncloop.run_until_complete(wait_tasks)
