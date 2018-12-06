import time
from dothat import lcd
from dothat import backlight
import dothat.touch as nav
from dot3k.menu import Menu, MenuOption
#lcd.set_contrast(18)
lcd.clear()

write_option(row = 0, 
    text = 'Hello this is some scrolling text', 
   scroll=True, # Enable auto-scrolling
   scroll_speed=200,  # Delay between each scroll position
   scroll_delay=2000, # Delay ( in ms ) until auto-scrolling starts
   scroll_repeat=10000, # Delay ( in ms ) before auto-scroll repeats
   scroll_padding='  '  # Padding added to the end of the text so it doesn't just wrap around onto itself
)
