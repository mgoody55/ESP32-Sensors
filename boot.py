# boot.py -- run on boot-up
import network
from machine import Pin, SoftI2C
import sh1106
from time import sleep
import secret

ssid = secret.SSID
wifi_password = secret.WIFI_PASSWORD

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = sh1106.SH1106_I2C(128, 64, i2c)
display.flip(True)

display.text('Initializing', 0, 0, 1)
display.show()

wlan = network.WLAN(network.STA_IF); wlan.active(True)
wlan.scan()                             # Scan for available access points
wlan.connect(ssid, wifi_password)   # Connect to an AP
wlan.isconnected()                      # Check for successful connection
print("Connected to WiFi. Waiting 3s before proceeding")
sleep(3)
