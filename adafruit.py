import serial.tools.list_ports

import sys

import time

import random
import json
from Adafruit_IO import MQTTClient
from secret import adaUsername, adaKey
# from controller import *
#from simple_ai import image_detector

#from port import *

# from rs485 import *

#from adafruit import *

class Adafruit_MQTT:

    AIO_FEED_IDs = [
                        "sys.mixer1", 
                        "sys.mixer2", 
                        "sys.mixer3",
                        "sys.next-cycle",
                        "sys.area1",
                        "sys.pump-in", 
                        "sys.pump-out",
                        "sys.active"
                    ]
    AIO_USERNAME = adaUsername
    AIO_KEY = adaKey
    recvCallBack = None

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)
    
    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed...")

    def publish(self, feed_id, value):
        self.client.publish(feed_id,value)
        # print(f"published {feed_id} to adafruit with {value} ")

    def disconnected(self, client):
        print("Disconnected... Trying to reconnect.")
        self.client.reconnect()

    def message(self, client, feed_id, payload):
        try:
            # Assuming payload is a JSON string, parse it
            data = json.loads(payload)
            if self.recvCallBack:
                self.recvCallBack(feed_id, data)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from payload: {payload}")

    def setRecvCallBack(self, func):
        self.recvCallBack = func

    def __init__(self):
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()






# Create an instance of Adafruit_MQTT

# mqtt_instance = Adafruit_MQTT()
client = Adafruit_MQTT() # public client --> sẽ dùng ở MAIN

# while True:
# 	# readSerial(mqtt_instance.client)
# 	time.sleep(2)
