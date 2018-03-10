import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

def get_iface_ip_address(iface):
    cmd = "ifconfig %s | grep \"inet \" | awk '{print $2}'" % iface
    ip = subprocess.check_output(cmd, shell = True )
    if len(str(ip).strip()) < 1:
        return "not connected"
    return str(ip)

def is_rogue_alive():
    cmd = "ps cax | grep 'hostapd' | wc -l"
    hostapd = subprocess.check_output(cmd, shell = True )
    return int(hostapd) > 0

def get_rogue_ssid():
    cmd = "grep -E \"^\W*?ssid\" /etc/hostapd/hostapd.conf | cut -d '=' -f2"
    ssid = subprocess.check_output(cmd, shell = True )
    if len(str(ssid).strip()) < 1 or not is_rogue_alive():
        return "not configured"
    return str(ssid)

def get_ssh_port():
    cmd = "grep -E \"^\W*?Port\" /etc/ssh/sshd_config | awk '{print $2}'"
    port = subprocess.check_output(cmd, shell = True )
    if len(str(port).strip()) < 1:
        return "not configured"
    return 'SSID: %s' % str(port)

def is_capturing():
    cmd = "ps cax | grep 'mitm\|wireshark' | wc -l"
    capture = subprocess.check_output(cmd, shell = True )
    if int(capture) == 0:
        return "not capturing"
    return 'capturing'
    
def get_disk_space():
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    disk = subprocess.check_output(cmd, shell = True )
    return str(disk)
    
def get_free_mem():
    cmd = "free -m | awk 'NR==2{printf \"RAM %.2f%%\", $3*100/$2 }'"
    mem = subprocess.check_output(cmd, shell = True )
    return str(mem)
    
def get_stats():
    return '%s %s'% (get_disk_space(), get_free_mem())

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
im = Image.open('/usr/share/PiRogue/oled-screen/infos.ppm').convert('1')
top = 0
left = 12
while True:
    draw = ImageDraw.Draw(im)
    draw.rectangle(((left, 0), (width, height)), fill=255)
    draw.text((left, top+0),     get_stats(), font=font, fill=0)
    draw.text((left, top+10),    get_iface_ip_address('eth0'), font=font, fill=0)
    draw.text((left, top+20),    get_iface_ip_address('wlan0'), font=font, fill=0)
    draw.text((left, top+30),    get_iface_ip_address('wlan1'), font=font, fill=0)
    draw.text((left, top+40),    get_rogue_ssid(), font=font, fill=0)
    draw.text((left, top+52),    is_capturing(), font=font, fill=0)
    disp.image(im)
    disp.display()
    time.sleep(.1)

