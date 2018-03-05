import paho.mqtt.client as mqtt #import the client1
import time

#import time
import os
import sys
import logging
import json

import pychromecast
import pychromecast.controllers.dashcast as dashcast

IGNORE_CEC = os.getenv('IGNORE_CEC') == 'True'
SUBSCRIBE = 'chromecast/+/command/dashcast'
MQTT_SERVER = os.getenv('MQTT_SERVER', 'iot.eclipse.org')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

############
def on_connect(client, userdata,flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	print("Subscribing to topic ",SUBSCRIBE)
	client.subscribe(SUBSCRIBE)

def on_message(client, userdata, message):
 print("Message received: " ,str(message.payload.decode("utf-8")))
 print("-Topic: ",message.topic)
 print("-QOS: ",message.qos)
 print("-Retain: ",message.retain)
 #print(message.topic.split('/'))
 	
 try:
	#print(message.payload.json())
 	json_decode=str(message.payload.decode("utf-8","ignore"))
 	print("Decoding Json")
 	parsed_json=json.loads(json_decode)
 except json.decoder.JSONDecodeError:
    print("Error passing JSON")
    return
	
 DISPLAY_NAME = str(message.topic.split('/')[1])
 print("Chromecast: "+DISPLAY_NAME)
 print("Url: "+parsed_json["url"])
 print("Force: "+str(parsed_json["force"]))
 cast_url(DISPLAY_NAME, parsed_json["url"],parsed_json["force"])
 
def cast_url(display, url, force):
	print("Searching for Chromecasts")
	casts = pychromecast.get_chromecasts()
	if len(casts) == 0:
		print("No Devices Found")
		return

	cast = next(cc for cc in casts if display in (None, '') or cc.device.friendly_name == display)

	if not cast:
		print('Chromecast with name', display, 'not found')
		return

	d = dashcast.DashCastController()
	cast.register_handler(d)

	print()
	print(cast.device)
	time.sleep(1)
	print()
	print(cast.status)
	print()
	print(cast.media_controller.status)
	print()

	if not cast.is_idle:
		print("Killing current running app")
		cast.quit_app()
		time.sleep(5)

	time.sleep(1)

	# Test that the callback chain works. This should send a message to
	# load the first url, but immediately after send a message load the
	# second url.
	warning_message = 'If you see this on your TV then something is broken'
	d.load_url(url, force,
			   callback_function=lambda result:
			   d.load_url(url,force))
 
########################################
#broker_address="192.168.1.184"
print("Starting MQTT")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.on_connect=on_connect
print("Connecting to Broker: "+MQTT_SERVER)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_SERVER) #connect to broker
#client.loop_start() #start the loop
client.loop_forever()

#print("Publishing message to topic","chromecast/TV/command/dashcast")
#client.publish("chromecast/TV/command/dashcast","{'"+DASHBOARD_URL+"', 'true'}")
#time.sleep(4) # wait
#client.loop_stop() #stop the loop
