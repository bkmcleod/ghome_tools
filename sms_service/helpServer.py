import paho.mqtt.client as mqtt
import time
outgoingSMSTopic = "/sms/outgoingMessage/"
incomingHelpMessageTopic = "/sms/incomingMessage/help/"
helpMessage = "This system is designed to interface with the 36 South Road Home Automation System.\nCurrent subsystems:\nfireplace\n\nTry \"fireplace help\" for example"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	global incomingHelpMessageTopic
	print("Connected with result code "+str(rc))
	client.subscribe(incomingHelpMessageTopic + "+")
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global outgoingSMSTopic, incomingHelpMessageTopic, helpMessage
	if incomingHelpMessageTopic in msg.topic:#if its a help request
		client.publish(outgoingSMSTopic + msg.topic.replace(incomingHelpMessageTopic, ""), helpMessage, qos=0, retain=False)

#login and connect to MQTT	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.11.160", 1883, 60)


# Loop printing measurements every second.
print('Entering Loop; Press Ctrl-C to quit.')
while True:#main loop for the program

	client.loop()
	
	time.sleep(0.5)