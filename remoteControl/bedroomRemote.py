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
import keys
import paho.mqtt.client as mqtt
import homeassistant.remote as remote
from datetime import datetime
from homeassistant.const import STATE_ON
from homeassistant.const import STATE_OFF
from homeassistant.const import SERVICE_TURN_ON 
import string


incomingRemoteTopic = "/bedroom/TVRemoteOut/press/"


def on_connect(client, userdata, flags, rc):
	global incomingRemoteTopic
	print("Connected with result code "+str(rc))
	client.subscribe(incomingRemoteTopic)#subscribe to topic with the fireplace command
	
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global remote, api
	hold = str(msg.payload)[2:(len(str(msg.payload))-1)]
	keysPressed = hold.split(',')
	
	
	keysPressed = [ int(x) for x in keysPressed ]
	print ("Keys Pressed: " + str(keysPressed))
	
	if (len(keysPressed)==1): #only if one button is pressed ie) not a combo
		if (keys.KEY_UP in keysPressed): #Up Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_up')})
			
		if (keys.KEY_DOWN in keysPressed): #Down Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_down')})
			
		if (keys.KEY_LEFT in keysPressed): #Left Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_left')})
			
		if (keys.KEY_RIGHT in keysPressed): #Right Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_right')})
			
		if (keys.KEY_BACK in keysPressed): #KEY_BACK Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_back')})
			
		if (273 in keysPressed): #KEY_BACK Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_back')})
			
		if (keys.KEY_PLAYPAUSE in keysPressed): #KEY_PLAYPAUSE Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_play_pause')})
			
		if (keys.KEY_ENTER in keysPressed): # KEY_ENTER Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_select')})
			
		if (272 in keysPressed): # KEY_ENTER Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_select')})
			
		if (keys.KEY_HOMEPAGE in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_home')})
			
		if (keys.KEY_FASTFORWARD in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_fast_forward')})
			
		if (keys.KEY_REWIND in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_fast_backward')})
			
		if (keys.KEY_COMPOSE in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_guide')})
			
		if (keys.KEY_SEARCH in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_star')})
			
		if (keys.KEY_VOLUMEUP in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendan_tv_vol_up')})
			
		if (keys.KEY_VOLUMEDOWN in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendan_tv_vol_down')})
			
		if (keys.KEY_MUTE in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendan_tv_mute')})
			
		if (keys.KEY_POWER in keysPressed): # Button Pressed
			remote.call_service(api, 'switch', 'toggle', {'entity_id': '{}'.format('switch.brendan_bedroom_tv_power')})
			
		if (keys.KEY_1 in keysPressed): # Button Pressed
			remote.call_service(api, 'light', 'toggle', {'entity_id': '{}'.format('light.brendan_bedroom_tv_light')})
			
		if (keys.KEY_2 in keysPressed): # Button Pressed
			remote.call_service(api, 'light', 'toggle', {'entity_id': '{}'.format('light.brendan_bedroom_fan_1')})
			remote.call_service(api, 'light', 'toggle', {'entity_id': '{}'.format('light.brendan_bedroom_fan_2')})
			remote.call_service(api, 'light', 'toggle', {'entity_id': '{}'.format('light.brendan_bedroom_fan_3')})
			
		if (keys.KEY_3 in keysPressed): # Button Pressed
			remote.call_service(api, 'light', 'toggle', {'entity_id': '{}'.format('light.brendan_bedroom_night_stand')})
			
		if (keys.KEY_CONFIG in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_set_tv_to_pi')})
			
		if (keys.KEY_MAIL in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_set_tv_to_chromecast')})
			
		if (keys.KEY_WWW in keysPressed): # Button Pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_set_tv_to_roku')})
			
			
	if (len(keysPressed)==2): # two button combo
		if (keys.KEY_UP in keysPressed)and (keys.KEY_HOMEPAGE in keysPressed): #Up and home pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_stop	')})
			
		if (keys.KEY_UP in keysPressed)and (keys.KEY_BACK in keysPressed): #Up and home pressed
			remote.call_service(api, 'script', 'turn_on', {'entity_id': '{}'.format('script.brendans_bedroom_media_instant_replay	')})
		

#To implement: 
#- 

	
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