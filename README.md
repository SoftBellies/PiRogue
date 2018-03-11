# PiRogue
**PiRogue** is a small device meant to ease network interception and analysis. **PiRogue** is based on a [Raspberry Pi 3](https://www.raspberrypi.org/) and [Kali GNU/Linux](https://www.kali.org/).

## Hardware
The **PiRogue** is based on:
*  a Raspberry Pi 3
*  a `TL WN725N` version `2.1` or `2.2` 
*  a 32GB SD-card

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

## Screen customization
**PiRogue** has a tiny OLED screen on top of it. This screen displays two different screens:
*  the boot screen defined in `oled-screen/boot.py`
*  the details screen defined in `oled-screen/infos.py`

## Transparent proxying
While using `mitmproxy` you can use between at least 2 different modes:
* _normal_ you have to specify IP address and port of `mitmproxy` in the HTTP proxy section of the Wifi connection on your target device
* _transparent_ you do not need to specify a HTTP proxy on your target device

An helper script `/usr/share/PiRogue/proxy/transparent.sh` is available. By executing this script, HTTP and HTTPS traffic from `wlan1` will be redirected to `mitmproxy`.