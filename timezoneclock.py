#!/usr/bin/python3

from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment as sseg
from Adafruit_LED_Backpack import AlphaNum4 as alphanum
import os
import time
import asyncio
import RPi.GPIO as GPIO

# Init Timezone Variables
offset = 0
timezones = [['UTC', 0], ['HST', -10], ['HDT', -9], ['AKST', -9], ['AKDT', -8], ['PST', -8], ['PDT', -7], ['MST', -7], ['MDT', -6], ['CST', -6], ['CDT', -5], ['EST', -5], ['EDT', -4], ['AST', -4], ['ADT', -3]]

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
alphadisplay.print_str('HELP')
alphadisplay.write_display()

# Loop for starting displays
async def settime():
    # Sets Time
    utctime = datetime.utcnow()
    hour = utctime.hour
    minute = utctime.minute
    second = utctime.second

    # Clear Displays
    ssegdisplay.clear()

    ## Sets Displays to current UTC + Offset
    ssegdisplay.set_digit(0, int((hour + timezones[offset][1]) / 10 / 24))
    ssegdisplay.set_digit(1, (hour + timezones[offset][1]) % 10 % 24)
    ssegdisplay.set_digit(2, int(minute / 10))
    ssegdisplay.set_digit(3, minute % 10)

    # Colon Blink
    ssegdisplay.set_colon(second % 2)
    
    # Write to display
    ssegdisplay.write_display()

    # Waits a quarter second
    await asyncio.sleep(0.25)

# Get Button State
async def buttons():
    if GPIO.input(18) == False:
        global offset
        print(offset)
        offset += 1

# Async Loop
while(True):
    asyncloop = asyncio.get_event_loop()
    tasks = [asyncloop.create_task(settime()), asyncloop.create_task(buttons())]
    wait_tasks = asyncio.wait(tasks)
    asyncloop.run_until_complete(wait_tasks)
