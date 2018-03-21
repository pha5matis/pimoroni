#!/usr/bin/env python

import fcntl
import socket
import struct
import time
import os
import sys
import dot3k.lcd as lcd
import dot3k.backlight as backlight
import dot3k.joystick as nav
import psutil

#Clears the LCD and sets contrast on Start
lcd.clear()
lcd.set_contrast(47)

#Function to get CPU Temp
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#Function to get CPU Usage
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

#The Button press turns the backlight on and off.
ButtonStatus = 'Off'
@nav.on(nav.BUTTON)
def handle_button(pin):
    global ButtonStatus
    global loopcount
    if ButtonStatus == 'On':
	backlight.off()
	ButtonStatus = 'Off'
    else:
       loopcount = 0
       backlight.rgb(229, 0,255)
       ButtonStatus = 'On'


#The down joystick shuts the pi down
@nav.on(nav.DOWN)
def handle_down(pin):
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

loopcount = 0

while True:
	# Print Hostname Centred Uppercase
	host = socket.gethostname()
	host = '{}'.format(host.upper())
	hostmidlen = (16 - len(host)) / 2
	lcd.set_cursor_position(hostmidlen,0)
	lcd.write(host)

	# Get Interfaces and IP Addresses
	# Finds wireless devices with wlx in the name as a list and returns the first item in that list
	ifaces = psutil.net_if_addrs()
	wlxinterface = filter(lambda x: 'wlx' in x,ifaces)

	# If the list is returned without data set the wlxinterface to none this prevents an empty list
	if not wlxinterface:
	   wlxinterface = 'None'
	else:
	   wlxinterface = wlxinterface[0]

	wlxinterface = get_addr(wlxinterface)

	# Todo make this the same as above so it is dynamic
	enxb827eba4274e = get_addr('enxb827eba4274e')

	lcd.set_cursor_position(0,1)
	if enxb827eba4274e != 'Disconnected':
	    outputeth = ('E:' + enxb827eba4274e)
	    #Take the output of outputeth and get the length less 16chars on display and add the difference as white spaces
	    outputeth = outputeth + (16 - len(outputeth)) * ' '
	    lcd.write(outputeth)
	else:
	    outputeth = ('E:{}'.format(enxb827eba4274e))
             #Take the output of outputeth and get the length less 16chars on display and add the difference as white spaces
	    outputeth = outputeth + (16 - len(outputeth)) * ' '
	    lcd.write(outputeth)

	lcd.set_cursor_position(0,2)
	if wlxinterface != 'Disconnected':
	   outputwlan = ('W:'+ wlxinterface)
	   outputwlan = outputwlan + (16 - len(outputwlan)) * ' '
	   lcd.write(outputwlan)

	else:
	   outputwlan = ('W:{}'.format(wlxinterface))
           outputwlan = outputwlan + (16 - len(outputwlan)) * ' '
           lcd.write(outputwlan)

	#Sets the bar LED lights to a percentage of cputemp to the thermal throttle 80 degrees
	CpuTemp = getCPUtemperature()
	backlight.set_bar(0, [155] * int(float(CpuTemp) / 80 * 10 ))

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
