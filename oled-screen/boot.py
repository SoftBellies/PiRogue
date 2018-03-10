import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
im = Image.open('/usr/share/PiRogue/oled-screen/pirogue.ppm').convert('1')
top = 36
while True:
    draw = ImageDraw.Draw(im)
    draw.text((0, top),    "  PCAP or it didn't", font=font, fill=255)
    draw.text((0, top+14), "       happen!!    ", font=font, fill=255)
    disp.image(im)
    disp.display()
    time.sleep(.1)

