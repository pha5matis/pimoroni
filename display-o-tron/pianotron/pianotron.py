#!/usr/bin/env python
import fcntl
import socket
import struct
import time
import os
import sys
import psutil

from dothat import lcd
from dothat import backlight
import dothat.touch as nav

#Clears the LCD and sets contrast on Start
lcd.clear()
lcd.set_contrast(47)
backlight.graph_off()

#Global Variables
ButtonStatus = 'Off'
loopcount = 0

f=open('/root/.config/pianobar/scripts/out', 'r')

song = f.readline()
artist = f.readline()
station = f.readline()

if len(song) > 16:
    choppedsong = song[0:12] + "..."
else:
    choppedsong = song[0:(len(song)-1)]
    
if len(artist) > 16:
    choppedartist = artist[0:12] + "..."
else:
    choppedartist = artist[0:(len(artist)-1)]

if len(station) > 16:
    choppedstation = station[0:12] + "..."
else:
    choppedstation = station[0:(len(artist)-1)]

lcd.set_cursor_position(0,0)
lcd.write(choppedsong)
lcd.set_cursor_position(0,1)
lcd.write(choppedartist)
lcd.set_cursor_position(0,2)
lcd.write(choppedstation)

print choppedsong
print choppedartist
print choppedstation

f.close()
#lcd.close()
