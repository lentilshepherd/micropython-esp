from myesplib import *

def main():
    aiourlbase = "http://io.adafruit.com/api/groups/environmentals/send.json"
    aioparams = {"x-aio-key": "0739e3013b3ebf90cbfb961fb45c7f4e5b2ed5e9"}

    # setup
    mydht = dht.DHT22(machine.Pin(5))
    uid = getuid()
    ledpin = machine.Pin(LEDPIN, machine.Pin.OUT)
    ledpin.value(LEDOFF)
    credentials = readjson(WIFIFILE)
    wlan = network.WLAN(network.STA_IF)
    connect_best(wlan, credentials)

    # infinite loop
    while True:
        # connect WLAN if not already
        if not wlan.isconnected():
            wlan = connect_best(wlan, credentials)

        # get stats from DHT
        results = polldht(mydht, ledpin)
        results["freemem"] = gc.mem_free()

        for k,v in results.items():
            print("{}: {}".format(k,v))

        print()

        # construct URL with key and results
        paramstr = "&".join(["{}={}".format(k,v) for k,v in aioparams.items()])
        resultstr = "&".join(["{}{}={}".format(k,uid,v) for k,v in results.items()])
        urlvarstr = "&".join([paramstr, resultstr])
        url = "?".join([aiourlbase, urlvarstr])
        print(url)

        # send results to Adafruit IO
        response = get(url)
        print(response.text)
        response.close()

        time.sleep_ms(30000)

if __name__ == "__main__":
    main()
