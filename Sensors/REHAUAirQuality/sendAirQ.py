#!/usr/bin/python

# Import required modules
import os
import time
import paho.mqtt.client as mqtt


# Define credentials and connection details of MQTT broker
user = "digitalhhz"
passwd = "hackathon"
mqttbroker = "192.168.0.12"
channel = "hhz/125/4/1/1/0/1"

# Define path of the airsensor-script and command to be executed
dir = "/home/pi/Scripts/airsensor"
cmd = dir + " -v -o"

# Execute airsensor-script to get air quality value
valAirQ = ""
p = os.popen(cmd,"r")

while 1:
    # Save air quality value to a variable
    valAirQ = p.readline()
    if not valAirQ: break
    valAirQ = valAirQ.replace("\n", "")    

    # Send air quality value to MQTT broker
    def on_connect(client, userdata, flags, rc):
      print("Connected with result code " + str(rc))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set(user, passwd)
    client.connect(mqttbroker, 1883, 60)
    client.publish(channel, valAirQ)

