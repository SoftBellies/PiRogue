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
Then, start the installation (_it will take a long time and ask you questions_):
```
cd /usr/share/PiRogue
sh install.sh
```

Remeber that all the **PiRogue** files reside in `/usr/share/PiRogue`.