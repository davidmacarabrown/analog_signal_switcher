from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

indicator = machine.Pin(25, machine.Pin.OUT)
indicator.value(0)
indicator.toggle()

# sda object, args: i2c channel, SDA Pin, SCL pin, frequency)
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

#old obj (width Px, heightPx, i2c object)
oled = SSD1306_I2C(128, 32, i2c)

# oled.text("SELECT LOCATION", 0,0)
# oled.text(" 1  2  3  4  5",0,14)

def off():
    oled.fill(0)
    oled.show()

#char, startPosition(x) y start position hard coded
def drawCharM(x): #vert height 32px 0-31 startPx from point on bottom edge, scanning left to right
#to draw "A" at 3px wide, oled.hline 3px Wide x 2px High
    
    #Y range 31 - 0     # X width 2px Y depth 2px
    #X range 0 - 127
    #start location 0, 31
    y = 0
    oled.fill_rect(x, y, 4, 32, 1)
    x+=4
    y+=1
    oled.vline(x,y,4,1)
    while x <= 15:
        oled.vline(x,y,4,1)
        x+=1
        y+=1
#     x+=1
    oled.vline(x,y,4,1)
    while x <= 27:
        x+=1
        y-=1
        oled.vline(x,y,4,1)
    x+=1
    y=0
    oled.fill_rect(x, y, 4, 32, 1)
    
drawCharM(0)
oled.show()
        
# oled.pixel(0,31,1)
# oled.show()

# drawChar()
        
# oled.fill_rect(0,0,32,32,1)

# oled.pixel(10,10,1)