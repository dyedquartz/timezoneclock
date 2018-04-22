#!/usr/bin/python

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

# Begins display
ss7segdisplay.begin()
alphadisplay.begin()

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
    await asyncio.sleep(0.25)

async def buttons():
    async if GPIO.input(18) == False:
        print('Left button pressed')
        await asyncio.sleep(0.02)

asyncloop = asyncio.get_event_loop()
tasks = [asyncloop.create_task(settime()), asyncloop.create_task(buttons())]
wait_tasks = asyncio.wait(tasks)
asyncloop.run_forever()
