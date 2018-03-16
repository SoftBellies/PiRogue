![logo](https://git.0x39b.fr/lambda/PiRogue/raw/master/pictures/icon.png)

# PiRogue
**PiRogue** is a small device meant to ease network interception and analysis. **PiRogue** is based on a [Raspberry Pi 3](https://www.raspberrypi.org/) and [Kali GNU/Linux](https://www.kali.org/). This project is for educational purpose. 

By default, **PiRogue** will mount a rogue Wifi access point with the SSID `PiRogue` without password available on `wlan1` which is the Wifi dongle. The Internet connection will be dynamically shared with the rogue Wifi network. **PiRogue** will automatically share the active connection (`wlan0` or `eth0`). 

The OLED screen on top of the **PiRogue** will display: 
*  disk and memory information
*  ethernet IP address
*  Wifi IP address
*  rogue Wifi IP address
*  rogue Wifi SSID
*  indication about network capture

Since **PiRogue** is based on [Kali GNU/Linux](https://www.kali.org/), it offers [plenty of tools](https://tools.kali.org/).

This project was initiated with the participation of [@MaliciaRogue](https://twitter.com/MaliciaRogue).

## Hardware
The **PiRogue** is based on:
*  a Raspberry Pi 3
*  a `TL WN725N` version `2.1` or `2.2` 
*  a 32GB SD-card

A custom 3D printed case is [available on Thingiverse](https://www.thingiverse.com/thing:2822262).

## Installation
First of all, you have to resize the `root` partition. So install `gparted`:
```
apt update
apt install -y gparted
```
and use it to resize the partition.

To install and configure your **PiRogue**, just clone the project Git repository:
```
git clone http://git.0x39b.fr/lambda/PiRogue.git /usr/share/PiRogue
```
Then, start the installation (_it will take a long time and ask questions_):
```
cd /usr/share/PiRogue
sh install.sh
```

Remember that all the **PiRogue** files reside in `/usr/share/PiRogue`.

## Demo
*  [Ep1 - Capture HTTP/S traffic](https://www.youtube.com/watch?v=o0OSaSh0HJw)

## Screen customization
**PiRogue** has a tiny OLED screen on top of it. This screen displays two different screens:
*  the boot screen defined in `oled-screen/boot.py`
*  the details screen defined in `oled-screen/infos.py`

## Transparent proxying
While using `mitmproxy` you can use between at least 2 different modes:
* _normal_ you have to specify IP address and port of `mitmproxy` in the HTTP proxy section of the Wifi connection on your target device
* _transparent_ you do not need to specify a HTTP proxy on your target device

An helper script `/usr/share/PiRogue/proxy/transparent.sh` is available. By executing this script, HTTP and HTTPS traffic from `wlan1` will be redirected to `mitmproxy`.
