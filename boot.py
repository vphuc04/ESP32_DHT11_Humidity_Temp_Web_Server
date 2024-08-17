try:
  import usocket as socket
except:
  import socket

import network
from machine import Pin
import dht

import time


import esp
esp.osdebug(None)

import gc
#gc.collect()

ssid = 'BTS'
password = '5concoden@'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

#while station.isconnected() == False:
#  pass

timeout = 10  # Thời gian chờ tối đa là 10 giây
while not station.isconnected() and timeout > 0:
  time.sleep(1)
  timeout -= 1

if station.isconnected():
  print('Connection successful')
  print(station.ifconfig())
else:
  print('Connection failed')

print('Connection successful')
print(station.ifconfig())

gc.collect()


dht_pin = dht.DHT11(Pin(4)) # Uncomment it if you are using DHT11 and comment the above line

