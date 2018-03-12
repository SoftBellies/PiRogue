#!/bin/bash

IF=$1
STATUS=$2

function add_rules {
        iptables -t nat -A POSTROUTING -o $1 -j MASQUERADE
        iptables -A FORWARD -i $1 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -A FORWARD -i wlan1 -o $1 -j ACCEPT
        ip6tables -A FORWARD -i $1 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
        ip6tables -A FORWARD -i wlan1 -o $1 -j ACCEPT
}

function remove_rules {
        iptables -t nat -D POSTROUTING -o $1 -j MASQUERADE
        iptables -D FORWARD -i $1 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
        iptables -D FORWARD -i wlan1 -o $1 -j ACCEPT
        ip6tables -D FORWARD -i $1 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
        ip6tables -D FORWARD -i wlan1 -o $1 -j ACCEPT
}

if [ "$IF" == "wlan0" ]
then
        case "$2" in
                up)
                        # interface is up
                        echo "wlan0 up" >> /tmp/pirogue_routing
                        add_rules $IF
                        ;;
                down)
                        # interface will be down
                        echo "wlan0 down" >> /tmp/pirogue_routing
                        remove_rules $IF
                        ;;
                pre-up)
                        # interface will be up
                        ;;
                post-down)
                        # interface is down
                        ;;
                *)
                        ;;
        esac
fi

if [ "$IF" == "eth0" ]
then
        case "$2" in
                up)
                        # interface is up
                        echo "eth0 up" >> /tmp/pirogue_routing
                        add_rules $IF
                        ;;
                down)
                        # interface will be down
                        echo "eth0 down" >> /tmp/pirogue_routing
                        remove_rules $IF
                        ;;
                pre-up)
                        # interface will be up
                        ;;
                post-down)
                        # interface is down
                        ;;
                *)
                        ;;
        esac
fi
