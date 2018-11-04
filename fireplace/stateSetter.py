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


currentTemp=260.0
newData= True
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/fireplace/exahust")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global currentTemp, newData
	print(msg.topic+" "+str(msg.payload))
	currentTemp = float(msg.payload)
	newData=True

	
api = remote.API('192.168.11.160', 'turninTuna')
print(remote.validate_api(api))	



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.11.160", 1883, 60)

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	if (newData):
		try:
			if currentTemp >= 250.0:
				print('Over')
				remote.call_service(api, 'input_select', 'select_option', {'entity_id':'input_select.fireplace_burn_zone', 'option':'Over Temperature'})
				#os.system('curl -s --data-binary \'{\"entity_id\":\"input_select.fireplace_burn_zone\",\"option\":\"Over Temperature\"}\' -H \'content-type: application/json;\' http://192.168.11.160:8123/api/services/input_select/select_option?api_password=turninTuna')
			if currentTemp >= 135.0 and currentTemp < 250.0:
				print('Optimal')
				remote.call_service(api, 'input_select', 'select_option', {'entity_id':'input_select.fireplace_burn_zone', 'option':'Optimal Burn Zone'})
				#os.system('curl -s --data-binary \'{\"entity_id\":\"input_select.fireplace_burn_zone\",\"option\":\"Optimal Burn Zone\"}\' -H \'content-type: application/json;\' http://192.168.11.160:8123/api/services/input_select/select_option?api_password=turninTuna')
			if currentTemp >= 50.0 and currentTemp < 135.0:
				print('Under')
				remote.call_service(api, 'input_select', 'select_option', {'entity_id':'input_select.fireplace_burn_zone', 'option':'Below Temperature'})
				#os.system('curl -s --data-binary \'{\"entity_id\":\"input_select.fireplace_burn_zone\",\"option\":\"Below Temperature\"}\' -H \'content-type: application/json;\' http://192.168.11.160:8123/api/services/input_select/select_option?api_password=turninTuna')
			if currentTemp < 50.0:
				print('Off')
				remote.call_service(api, 'input_select', 'select_option', {'entity_id':'input_select.fireplace_burn_zone', 'option':'Not Burning'})
				#os.system('curl -s --data-binary \'{\"entity_id\":\"input_select.fireplace_burn_zone\",\"option\":\"Not Burning\"}\' -H \'content-type: application/json;\' http://192.168.11.160:8123/api/services/input_select/select_option?api_password=turninTuna')
			newData=False
		except:
			print('Home Assistant Error')
	client.loop()
	time.sleep(1.0)