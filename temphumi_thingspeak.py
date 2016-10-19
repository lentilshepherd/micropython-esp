import time
import dht
import machine
import network
import socket
import gc

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
    thingspeakaddress = "api.thingspeak.com"
    writeAPIKey = "1KQT1C2UPYQYS7U5"

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
        memfree = gc.mem_free()
        print("Temperature: {}".format(temp))
        print("Humidity:    {}".format(humi))
        print("Memory free: {}".format(memfree))
        print()

        http_get('http://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}'.format(
            writeAPIKey,
            temp,
            humi,
            memfree
            ))

        time.sleep_ms(30000)

if __name__ == "__main__":
    main()
