import json
import pprint
import quopri
import subprocess
import tempfile
import sys, os, random, json, logging
import io as sio
import binascii
from mitmproxy import io 
from mitmproxy.exceptions import FlowReadException
 
pp = pprint.PrettyPrinter(indent=4)

 
def extract_string(value):
    try:
        return value.decode()
    except AttributeError:
        return value
 
 
def extract_headers(flow):
    headers = flow.headers
    return {extract_string(key): extract_string(value) for (key, value) in
            headers.items()}
 

def decode_protoc(lines):
    obj = []
    prefix = ''
    prev = []
    cursor = 0
    for ll in lines:
        l = ll.strip()
        if '{' in l:
            name = l[:l.find('{')]
            prev.append(name)
        elif ':' in l:
            name = l[:l.find(':')]
            prefix = ';'.join(prev)
            value = l[l.find(':')+1:]
            obj.append('%s;%s=%s'%(prefix, name, value))
        elif '}' in l:
            prev.pop()
    return obj

 
def extract_content(flow):
    content = flow.request.content[92:]
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(content)
        tf.close()
        try:
            content = subprocess.check_output("cat %s | gzip -cd | protoc --decode_raw"%tf.name, input=content, shell=True)
            os.unlink(tf.name)
            buf = sio.StringIO(str(content.decode().replace(' ','')))
            lines = buf.readlines()
            content = content.decode()
            return decode_protoc(lines)
        except Exception:
            os.unlink(tf.name)

 
def extract_request(flow):
    request = flow.request
    host = request.pretty_host
    url = request.pretty_url
    headers = extract_headers(request)
    content = extract_content(request)
    return {"host": host, "url": url, "headers": headers, "content": content}
 
 
def extract_response(flow):
    response = flow.response
    if not response:
        return None
    status = response.status_code
    headers = extract_headers(response)
    content = extract_content(response)
    return {"status": status, "headers": headers, "content": content}
 
 
def extract(flow):
    request = extract_request(flow)
    response = extract_response(flow)
    return {"request": request, "response": response}
 

def extract_bssids(data):
    bssids = []
    for _, l in enumerate(data):
        if l.startswith('4;17;3;6;1=') or l.startswith('4;17;5;1;1='):
            bssids.append(l[l.find('=')+1:])

    return bssids

def toU32(bits):
    import struct
    return struct.unpack_from(">I", bits)[0]

def toS32(bits):
    import struct
    return struct.unpack_from(">i", bits)[0]

def get_locs(data):
    locs = []
    lat = 0
    lon = 0
    for _, l in enumerate(data):
        # Lat
        if l.startswith('4;3;1;1='):
            loc = l[l.find('=')+1:]
            b = bytearray.fromhex(loc[2:])
            lat = int(loc,16)/10000000.0

        # Lon
        if l.startswith('4;3;1;2='):
            loc = l[l.find('=')+1:]
            b = bytearray.fromhex(loc[2:])
            lon = toS32(b)/10000000.0

        if lat != 0 and lon != 0:
            print((lat,lon))
            locs.append((lat,lon))
            lat = 0
            lon = 0
    return locs


 
def get_bssid_loc(bssid):
    import requests
    r = requests.get('https://api.mylnikov.org/wifi?v=1.1&bssid=%s'%hex(int(bssid))[2:])
    if r.status_code == 200:
        loc = r.json()
        if loc['result'] != 200:
            return None
        return (loc['data']['lat'],loc['data']['lon'])

markers = []
markersFile = 'france2/markers.csv'
try:
    os.unlink(markersFile)
except:
    pass

def response(flow):
    url = flow.request.url
    i = 0
    if 'https://www.google.com/loc/m/api' in url:
        content = extract_content(flow)
        bssids = extract_bssids(content)
        gps_locations = get_locs(content)
        locations = []
        for bssid in bssids:
            loc = get_bssid_loc(bssid)
            if loc:
                markers.append(loc)
                locations.append(loc)
        with open(markersFile, 'a') as mf:
            for m in locations:
                mf.write('%s;%s;%s;1\n'%(i,m[0],m[1]))
                i += 1
            for m in gps_locations:
                mf.write('%s;%s;%s;2\n'%(i,m[0],m[1]))
                i += 1



## mitmweb -p 8088 
# ./france2/venv/bin/mitmweb -p 8080  -s "./france2/gls.py" -r waze.flows