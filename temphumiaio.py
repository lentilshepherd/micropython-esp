import time
import dht
import machine
import network
import socket
import gc
import esp

# constants
DHTPIN = 5
LEDPIN = 0
LEDOFF = 1
LEDON = 0

# functions
def ledon(ledpin):
    ledpin.value(LEDON)

def ledoff(ledpin):
    ledpin.value(LEDOFF)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('lentil', 'greats1ab')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return(wlan)

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    print()
    s.close()

def main():
    aioaddress = "io.adafruit.com"
    aiokey = "0739e3013b3ebf90cbfb961fb45c7f4e5b2ed5e9"

    # setup
    mydht = dht.DHT22(machine.Pin(5))
    ledpin = machine.Pin(LEDPIN, machine.Pin.OUT)
    ledpin.value(LEDOFF)
    wlan = do_connect()


    # infinite loop
    while True:
        ledon(ledpin)
        mydht.measure()
        ledoff(ledpin)
        temp = round(mydht.temperature(),1)
        humi = round(mydht.humidity(),1)
        memfree = esp.freemem()
        print("Temperature: {:.1f}".format(temp))
        print("Humidity:    {:.1f}".format(humi))
        print("Memory free: {:.1f}".format(memfree))
        print()
        http_get('http://io.adafruit.com/api/groups/environmentals/send.json?x-aio-key={}&esp1temp={:.1f}&esp1humidity={:.1f}&esp1memfree={}'.format(
            aiokey,
            temp,
            humi,
            memfree
            ))

        time.sleep_ms(30000)

if __name__ == "__main__":
    main()
