## Synopsis

Experiments in IOT using micropython on the ESP8266.

All examples expect wifi credentials in JSON format in a file called wificonf.json

$ cat wificonf.json 
{"SSID2": "password2", "SSID1": "password1"}

## Installation

Copy the script and wificonf.json to the ESP8266 flash.  For exmample, using ampy:
$ampy --port /dev/tty.<whatever> put temphumiaio.py

If you want the script to run automatically when the ESP8266 is powered on, call it main.py on the device flash:
$ampy --port /dev/tty.<whatever> put temphumiaio.py main.py

## References

http://docs.micropython.org/en/v1.8/esp8266/
https://thingspeak.com/
https://io.adafruit.com/
