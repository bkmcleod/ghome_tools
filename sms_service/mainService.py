from googlevoice import Voice
from googlevoice.util import ParsingError
from googlevoice.util import input
import time
import os
import paho.mqtt.client as mqtt
import csv
from googlevoice import Voice
import sys
import BeautifulSoup
from datetime import datetime

messageQueue = []
outgoingMessageTopic = "/sms/outgoingMessage/"
incomingMessageTopic = "/sms/incomingMessage/"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	global outgoingMessageTopic
	print("Connected with result code "+str(rc))
	client.subscribe(outgoingMessageTopic + "+")
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global outgoingMessageTopic
	if outgoingMessageTopic in msg.topic:#if its an SMS to send
		add_sms_to_queue(msg.topic, msg.payload)
		
def add_sms_to_queue(topicNumber, message):
	global messageQueue
	phoneNumber = get_number_from_address_book(topicNumber)
	messageQueue.append([phoneNumber, message])
	
	
def get_number_from_address_book(numberString):
	global addressBook, outgoingMessageTopic
	numberString = numberString.replace(outgoingMessageTopic, "")
	for row in addressBook:
		if numberString == row[0]:
			numberString = row[1]
	return numberString	
def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems
def isWhiteListed(phoneNumber):
	global addressBook
	for line in addressBook:
		if (line[1] == phoneNumber):
			return True
	return False
def getNameFromWhitelist(phoneNumber):
	global addressBook
	for line in addressBook:
		if (line[1] == phoneNumber):
			return line[0]
	return "BrendanM"
def publish_new_sms(messageFromGV, client, incomingMessageTopic):
	#extract the topic its meant for
	topic = ""
	command = ""
	spaceLocation = messageFromGV['text'].find(' ')
	if (spaceLocation) < 0:#if there isn't a space then there obviously isn't an identifer, so its a single word command for the topic
		topic = messageFromGV['text'].lower()
	else:
		#if we get to this point there's an identifer with additional commands
		topic = messageFromGV['text'][0:(spaceLocation)].lower()
	command = messageFromGV['text'][(spaceLocation+1):(len(messageFromGV['text']))].lower()
	phoneNumber = messageFromGV['from'].replace('(', "").replace(')', "").replace(' ', "").replace('+', "").replace(':', "")
	if (isWhiteListed(phoneNumber)):
		phoneNumber = getNameFromWhitelist(phoneNumber)
		client.publish(incomingMessageTopic + topic + "/" + phoneNumber, command, qos=0, retain=False)
		print("Topic: " + topic + "; Command: " + command + "; Number: " + phoneNumber)
	else:
		add_sms_to_queue(phoneNumber, "Error, phone number not whitelisted")

def clear_sms_queue(messageQueue):
	for message in messageQueue:
		print("Sending: " + message[0] + "; " + message[1])
		voice.send_sms(message[0], message[1])
		
#login and connect to MQTT	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.11.160", 1883, 60)

#login and connect to GoogleVoice
voice = Voice()
print("Logging into GV...")
voice.login()

print("Reading whitelist...")
#Load the address book from file
datafile = open('whitelist.csv', 'r')
whitelistReader = csv.reader(datafile,delimiter=';')
addressBook = []
for row in whitelistReader:
    addressBook.append(row)    
addressBook.pop(0)

print("Current Address Book: ")
print(addressBook)
# Loop printing measurements every second.

print('Entering Loop; Press Ctrl-C to quit.')
add_sms_to_queue("6035711332", "SMS Service Restarted " + str(datetime.now()))

while True:#main loop for the program

	client.loop()	
	#print("checking SMS...")
	try:
                voice.sms()
        except ParsingError:#reload the SMS from Google Voice
                print("Parse error...")
                time.sleep(5.0)
                continue
	#reload the SMS from Google Voice
	newMessages = extractsms(voice.sms.html)#extract all new messages
	for singleMessage in newMessages:
		publish_new_sms(singleMessage, client, incomingMessageTopic)
	clear_sms_queue(messageQueue)
	#print("Clearing old messages...")
	if (len(newMessages)+len(messageQueue))>0:
		for message in voice.sms().messages:
			message.delete()
	messageQueue=[]
	time.sleep(2.5)
