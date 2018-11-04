#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
import os
import paho.mqtt.client as mqtt
import homeassistant.remote as remote
from datetime import datetime


currentTemp=0
prevTemp=0
sendMessageState=0
messageSent=0

outgoingSMSTopic = "/sms/outgoingMessage/"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/fireplace/exahust")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global currentTemp, prevTemp
	print(msg.topic+" "+str(msg.payload))
	prevTemp=currentTemp
	currentTemp = float(msg.payload)

	
api = remote.API('192.168.11.160', 'turninTuna')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.11.160", 1883, 60)

# Loop printing measurements every second.
print('Entering Loop; Press Ctrl-C to quit.')
while True:

	if currentTemp < 135.0 and prevTemp>=135.0: #if before it was optimal, and now its sub optimal
		if messageSent==0:
			print("State Tranisiton")
			messageSent=1
			if remote.get_state(api, 'switch.jordan_fireplace_monitor').state == 'on':
				client.publish(outgoingSMSTopic + "JordanB", "Fireplace has dropped below optimal temperature at " + str(datetime.now()))
			if remote.get_state(api, 'switch.brendan_fireplace_monitor').state == 'on':
				client.publish(outgoingSMSTopic + "BrendanM", "Fireplace has dropped below optimal temperature at " + str(datetime.now()))
			if remote.get_state(api, 'switch.joel_fireplace_monitor').state == 'on':
				client.publish(outgoingSMSTopic + "JoelD", "Fireplace has dropped below optimal temperature at " + str(datetime.now()))
	else:
		messageSent=0
	client.loop()
	time.sleep(0.25)