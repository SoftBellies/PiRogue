PIROGUE_ROOT_DIR=/usr/share/PiRogue
mkdir -p $PIROGUE_ROOT_DIR

# Resize the partition
apt update
apt install -y gparted
#  launch gparted and resize the root partition

# Install foundation
apt dist-upgrade
apt install -y kali-linux-full
apt install -y bash-completion vim git dexdump adb htop thunar-archive-plugin ntp
apt install -y linux-headers-$(uname -r) build-essential python-dev ristretto
apt install -y python-pip python-imaging python-smbus i2c-tools mana-toolkit
pip install RPi.GPIO 

# Change hostname
echo PiRogue > /etc/hostname

# Fix locale issue
echo 'export LC_ALL="en_US.UTF-8"' >> ~/.bashrc

# Install the realtek driver
apt install -y firmware-realtek
#  after the next reboot, wlan1 will be available

# Configure wlan1 as rogue AP
cat >>/etc/network/interfaces <<EOL
auto wlan1
allow-hotplug wlan1
iface wlan1 inet static
    address 10.0.0.1
    netmask 255.0.0.0
    up iptables-restore < /etc/iptables.ipv4.nat; ip6tables-restore < /etc/iptables.ipv6.nat
EOL

# Install hostapd
cd /tmp
wget http://ftp.fr.debian.org/debian/pool/main/w/wpa/hostapd_2.4-1+deb9u1_armhf.deb
dpkg -i hostapd_2.4-1+deb9u1_armhf.deb
apt-mark hold hostapd
systemctl unmask hostapd
systemctl enable hostapd
cd

# Configure hostapd
echo DAEMON_CONF=\"${PIROGUE_ROOT_DIR}/hostapd/hostapd.conf\" >> /etc/default/hostapd
#rm -rf /etc/hostapd/hostapd.conf
#ln -s ${PIROGUE_ROOT_DIR}/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

# Instal dnsmasq
apt install -y dnsmasq
systemctl enable dnsmasq

# Configure dnsmasq
rm -rf /etc/dnsmasq.conf
ln -s ${PIROGUE_ROOT_DIR}/dnsmasq/dnsmasq.conf /etc/dnsmasq.conf

# Configure network routing
echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf
echo net.ipv6.conf.all.forwarding=1 >> /etc/sysctl.conf

# Configure the firewall
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  
iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE  
iptables -A FORWARD -i eth0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT  
iptables -A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT  
iptables -A FORWARD -i wlan1 -o eth0 -j ACCEPT  
iptables -A FORWARD -i wlan1 -o wlan0 -j ACCEPT  

ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  
ip6tables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE  
ip6tables -A FORWARD -i eth0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT  
ip6tables -A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT  
ip6tables -A FORWARD -i wlan1 -o eth0 -j ACCEPT  
ip6tables -A FORWARD -i wlan1 -o wlan0 -j ACCEPT  

# Save firewall configuration
iptables-save > /etc/iptables.ipv4.nat
ip6tables-save > /etc/iptables.ipv6.nat

# Configure I2C
cat >/boot/config.txt <<EOL
dtparam=i2c1=on
dtparam=i2c_arm=on
EOL
cat >/etc/modules <<EOL
i2c-bcm2708 
i2c-dev
EOL

# Install OLED library
cd /tmp
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git ssd1306
cd ssd1306
python setup.py install
cd
rm -rf /tmp/ssd1306

# Add a reboot task in cron table displaying the boot screen
crontab -l > /tmp/crontab
echo @reboot /usr/bin/python ${PIROGUE_ROOT_DIR}/oled-screen/boot.py >> /tmp/crontab
crontab /tmp/crontab
rm /tmp/crontab

# Add a service displaying PiRogue details
ln -s ${PIROGUE_ROOT_DIR}/oled-screen/display_details.service /etc/systemd/system/display_details.service
systemctl enable display_details.service

# Final reboot
reboot