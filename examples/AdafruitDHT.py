#!/usr/bin/python
import time  
import sys  
import httplib, urllib  
import json
import Adafruit_DHT


deviceId = "D1QxLyzK"  
deviceKey = "GazI00ZLnPHecd25"


def post_to_mcs(payload):  
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            not_connected = 0
        except (httplib.HTTPException, socket.error) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
    response = conn.getresponse()
    print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()

while True:  
    h0,t0 = Adafruit_DHT.read_retry(11,4)
    payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},{"dataChnId":"temperature","values":{"value":t0}}]}
    post_to_mcs(payload)
    time.sleep(10)
