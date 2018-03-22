# Google Location Service live map
Some applications like _Waze_ use GLS to accurately locate you. This plugin is meant to dynamically display GPS locations and Wifi routers locations on a map. Checkout the [Google Location Service reverse engineering](https://esther.codes/reverse-engineering-google-location-gms-specification/).

![screenshot](https://raw.githubusercontent.com/U039b/PiRogue/master/pictures/gls_live_map.png)

## Usage
You had already dumped MITMproxy flow file containing traffic of a travel session using _Waze_ or other application which use location, you can run this plugin with this command:
```
mitmproxy -s /usr/share/PiRogue/mitmproxy/gls_live_map/gls.py -r path/to/your/flow/file
```

If you want to use it during a live capture, using the following command:
```
mitmproxy -s /usr/share/PiRogue/mitmproxy/gls_live_map/gls.py
```

To see the live map, use the following command to open it in Firefox:
```
firefox /usr/share/PiRogue/mitmproxy/gls_live_map/map.html
```

