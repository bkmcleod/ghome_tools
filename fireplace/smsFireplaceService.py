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
from homeassistant.const import STATE_ON
from homeassistant.const import STATE_OFF


outgoingSMSTopic = "/sms/outgoingMessage/"
incomingSMSTopic = "/sms/incomingMessage/fireplace/"

helpMessage = "Options and commands:\nhelp: Help menu\nstart: Enable SMS notification\nstop: Disable SMS notifications\nstatus: Request current status"


def on_connect(client, userdata, flags, rc):
	global incomingSMSTopic
	print("Connected with result code "+str(rc))
	client.subscribe(incomingSMSTopic + "+")#subscribe to topic with the fireplace command
	
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global outgoingSMSTopic, remote, api
	spaceLocation = str(msg.payload).find(' ')
	if (spaceLocation) < 0:#if there isn't a space then there obviously isn't an identifer, so its a single word command for the topic
		command = str(msg.payload)[1:len(str(msg.payload))].replace('\'', '')
	else:
		command = str(msg.payload)[1:(spaceLocation)].replace('\'', '')
		
	
	phoneNumber = msg.topic.replace(incomingSMSTopic, "")	
	if (command == "help"):
		sendHelpMessage(outgoingSMSTopic, phoneNumber)
	elif (command == "status"):
		sendStatusMessage(outgoingSMSTopic, phoneNumber, remote, api)
	elif (command == "start"):
		setMonitorState(outgoingSMSTopic, phoneNumber, remote, api, STATE_ON)
	elif (command == "stop"):
		setMonitorState(outgoingSMSTopic, phoneNumber, remote, api, STATE_OFF)
		
def sendStatusMessage(outgoingSMSTopic, phoneNumber, remote, api):
	message = "Current temp is: " + remote.get_state(api, 'sensor.fireplace_temperature').state
	message = message + "\nCurrent state is: " + remote.get_state(api, 'input_select.fireplace_burn_zone').state
	client.publish(outgoingSMSTopic + phoneNumber, message)
				
def setMonitorState(outgoingSMSTopic, phoneNumber, remote, api, newState):
	print("Set monitor....")
	print(phoneNumber)
	print(newState)
	if phoneNumber == "JordanB":
		remote.set_state(api, 'switch.jordan_fireplace_monitor', new_state=newState)
	elif phoneNumber == "BrendanM":
		remote.set_state(api, 'switch.brendan_fireplace_monitor', new_state=newState)
	elif phoneNumber == "JoelD":
		remote.set_state(api, 'switch.joel_fireplace_monitor', new_state=newState)
	client.publish(outgoingSMSTopic + phoneNumber, "State set.")
		
def sendHelpMessage(outgoingSMSTopic, phoneNumber):
	global helpMessage
	client.publish(outgoingSMSTopic + phoneNumber, helpMessage)		
	
	
api = remote.API('192.168.11.160', 'turninTuna')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.11.160", 1883, 60)

# Loop printing measurements every second.
print('Entering Loop; Press Ctrl-C to quit.')
while True:


	client.loop()
	time.sleep(0.25)