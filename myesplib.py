"Utility functions for IOT projects on the ESP8266 running micropython"

import time
import dht
import machine
import network
import gc
import esp
import json
import ubinascii
import urequests

# constants
DHTPIN = 5
LEDPIN = 0
LEDOFF = 1
LEDON = 0
WIFIFILE = 'wificonf.json'

# functions
def ledon(ledpin):
    "Turn on onboard LED"
    ledpin.value(LEDON)

def ledoff(ledpin):
    "Turn off onboard LED"
    ledpin.value(LEDOFF)

def readjson(filename):
    "Read JSON file into dictionary"
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def connect_ssid(wlan, ssid, password = None, timeout = 10):
    "Connect to a named SSID with optional password and timeout"
    print('Trying to connect to network {}'.format(ssid))
    wlan.connect(ssid, password)
    for timer in range(timeout):
        if wlan.isconnected():
            print('Success')
            return(ssid)
        else:
            time.sleep(1)
    print('Timed out')
    
def connect_best(wlan, credentials):
    "Connect to known SSID with strongest signal"
    wlan.active(True)
    ssids = wlan.scan()
    ssids = [ (x[0].decode('utf-8'), x[3]) for x in ssids ]
    ssids.sort(reverse=True, key=lambda x: int(x[1])) # sort by signal strength
    print('Wireless networks detected:')
    if len(ssids) == 0:
        print('None')
    for entry in ssids:
        print(entry)
    for ssid, _ in ssids:
        if not ssid in credentials:
            continue
        connssid = connect_ssid(wlan, ssid, credentials[ssid])
        if connssid:
            print('Connected to {}'.format(connssid))
            return connssid
    print("Failed to connect to any wireless network")

def polldht(dht, ledpin = None):
    """Collect measurements from DHT and return in a dictionary.
       If ledpin is specified, turn it on before measurement, and off after.
    """
    if ledpin:
        ledon(ledpin)
    dht.measure()
    results = {}
    results['temp'] = dht.temperature()
    results['humi'] = dht.humidity()
    if ledpin:
        ledoff(ledpin)
    return results

def getuid():
    "Return ESP unique ID as a string"
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')
