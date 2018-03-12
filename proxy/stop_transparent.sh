echo "Stop redirecting HTTP and HTTPS traffic from wlan1 to mitmproxy"
iptables -t nat -D PREROUTING -i wlan1 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -D PREROUTING -i wlan1 -p tcp --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -D PREROUTING -i wlan1 -p tcp --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -D PREROUTING -i wlan1 -p tcp --dport 443 -j REDIRECT --to-port 8080
echo "Complete"