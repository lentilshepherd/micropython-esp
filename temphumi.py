import dht
import machine

DHTPIN = 5

mydht = dht.DHT22(machine.Pin(5))
mydht.measure()
temp = mydht.temperature()
humi = mydht.humidity()

print("Temperature: {}".format(temp))
print("Humidity:    {}".format(humi))

