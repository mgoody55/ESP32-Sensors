from machine import Pin, SoftI2C
from time import sleep
import dht
import sh1106
import machine
import time
from umqttsimple import MQTTClient
import secret

# Onboard LED
led = Pin(2, Pin.OUT)

# DHT22 Temp and Humidity Sensor
sensor = dht.DHT22(Pin(23))

# I2C Setup
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = sh1106.SH1106_I2C(128, 64, i2c)
display.flip(True)

# MQTT Setup
mqtt_server = secret.MQTT_SERVER_IP
mqtt_user = secret.MQTT_USER
mqtt_pass = secret.MQTT_PASSWORD
client_id = 'office_esp32'

topic_sub = b'esp32/office/sensors'
topic_pub = b'esp32/office/sensors'


def sub_cb(topic, msg):
  print((topic, msg))
  if topic == topic_sub and msg == b'received':
    print('ESP received hello message')


def connect_and_subscribe():
  client = MQTTClient(client_id, mqtt_server, port = 1883, user = mqtt_user, password = mqtt_pass, keepalive=30,ssl=False)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to MQTT server at %s, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  machine.reset()


while True:
  if wlan.isconnected():
   display.pixel(122, 6, 1)
   display.wifi_connected_logo(119, 2, 1)
  else:
   display.wifi_disconnected_logo(119, 2, 1)
  
  try:
    client = connect_and_subscribe()
  except OSError as e:
    restart_and_reconnect()

  led.value(True)
  sensor.measure()
  led.value(False)
  tempF = round(sensor.temperature() * (9/5) + 32, 1)
  hum = round(sensor.humidity(), 1)
  
  display.fill(0)
  display.text('T: %.1fF' % tempF, 32, 25, 1)
  display.text('H: %.1f' % hum + '%', 32, 35, 1)
  display.show(full_update=True)

  client.publish(topic_pub + '/temperature', str(tempF))
  client.publish(topic_pub + '/humidity', str(hum))

  print("T: " + str(tempF) + 'F')
  print('H: ' + str(hum) + '%')
  sleep(60)
