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

#Function to get CPU Temp
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#Function to get CPU Usage
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

#The Button press turns the backlight on and off.
@nav.on(nav.BUTTON)
def handle_button(ch, evt):
#def handle_button(pin):
    global ButtonStatus
    global loopcount
    if ButtonStatus == 'On':
	backlight.off()
	ButtonStatus = 'Off'
    else:
       backlight.rgb(229,255,0)
	   display_hostname()
	   display_NIC()
	   display_WNIC()
       ButtonStatus = 'On'
       loopcount = 0

#The down joystick shuts the pi down
@nav.on(nav.DOWN)
def handle_down(ch, evt):
#def handle_down(pin):
    global loopcount
    loopcount=0
    lcd.clear()
    backlight.rgb(255, 0, 0)
    lcd.write("Shutting Down!")
    time.sleep(1)
    os.system('systemctl poweroff') 
    sys.exit()
    time.sleep(2)

#Function to get interface IP's
def get_addr(ifname):
   try:
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       return socket.inet_ntoa(fcntl.ioctl(
          s.fileno(),
          0x8915,  # SIOCGIFADDR
          struct.pack('256s', ifname[:15].encode('utf-8'))
       )[20:24])
   except IOError:
      return 'Disconnected'

#Function to get hostname in uppercase
def get_HostName():
	hostname = (socket.gethostname()).upper()
	return hostname

#Print the hostname as a function on the first line centered.
def display_hostname():
	hostmidlen = (16 - len(get_HostName())) / 2
	lcd.set_cursor_position(hostmidlen,0)
	lcd.write(get_HostName())

#Gets the wireless Nic with wlx in the name as a list and returns the first item in that list
def get_WNIC():
	ifaces = psutil.net_if_addrs()
	wlxinterface = filter(lambda x: 'wlx' in x,ifaces)
	if not wlxinterface:
		wlxinterface = 'None'
	else:
		wlxinterface = wlxinterface[0]
	return wlxinterface

def get_NIC():
	ifaces = psutil.net_if_addrs()
	enxinterface = filter(lambda x: 'enx' in x,ifaces)
	if not enxinterface:
		enxinterface = 'None'
	else:
		enxinterface = enxinterface[0]
	return enxinterface

def display_NIC():
	lcd.set_cursor_position(0,1)
	enxaddr = get_addr(get_NIC())
	if enxaddr != 'Disconnected':
		outputeth = ('E:' + enxaddr)
	    #Take the output of outputeth and get the length less 16chars on display and add the difference as white spaces
	    outputeth = outputeth + (16 - len(outputeth)) * ' '
	    lcd.write(outputeth)
	else:
	    outputeth = ('E:{}'.format(enxaddr))
    	outputeth = outputeth + (16 - len(outputeth)) * ' '
	    lcd.write(outputeth)

def display_WNIC():
	lcd.set_cursor_position(0,2)
	wlxaddr = get_addr(get_WNIC())
	if wlxaddr != 'Disconnected':
		outputwlan = ('W:'+ wlxaddr)
	    #Take the output of outputwlan and get the length less 16chars on display and add the difference as white spaces
		outputwlan = outputwlan + (16 - len(outputwlan)) * ' '
	    lcd.write(outputwlan)
	else:
		outputwlan = ('W:{}'.format(wlxaddr))
        outputwlan = outputwlan + (16 - len(outputwlan)) * ' '
        lcd.write(outputwlan)

#Initial Display
#Display Hostname
display_hostname()
display_NIC()
display_WNIC()

while True:
	display_hostname()
	display_NIC()
	display_WNIC()
	
    #Sets the bar LED lights to a percentage of cputemp to the thermal throttle 80 degrees
	CPUTemp = getCPUtemperature()
#	print CPUTemp
	if float(CPUTemp) > 60.0:
	   print CPUTemp
	   backlight.graph_set_led_duty(0,1)
	   backlight.graph_set_led_state(0,1)
	else:
	   backlight.graph_off()

#	backlight.set_bar(0, [155] * int(float(CpuTemp) / 80 * 10 ))

        # Puts the display to sleep after a minute the button press turns it on again
        if loopcount == 60:
           while loopcount >= 60:
             lcd.clear()
             backlight.off()
             time.sleep(1)

	loopcount = loopcount + 1
	time.sleep(1)

#	lcd.set_cursor_position(0,1)
#	CPUUse = getCPUuse()
#	CPUUse = CPUUse + (16 - len(CPUUse)) * ' '
#	lcd.write(CPUUse)
#	print(psutil.cpu_percent())
#	time.sleep(2)
