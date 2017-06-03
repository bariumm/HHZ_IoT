/**
 * The MySensors Arduino library handles the wireless radio link and protocol
 * between your home built sensors/actuators and HA controller of choice.
 * The sensors forms a self healing radio network with optional repeaters. Each
 * repeater and gateway builds a routing tables in EEPROM which keeps track of the
 * network topology allowing messages to be routed to nodes.
 *
 * Created by Henrik Ekblad <henrik.ekblad@mysensors.org>
 * Copyright (C) 2013-2015 Sensnology AB
 * Full contributor list: https://github.com/mysensors/Arduino/graphs/contributors
 *
 * Documentation: http://www.mysensors.org
 * Support Forum: http://forum.mysensors.org
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 2 as published by the Free Software Foundation.
 *
 *******************************
 *
 * REVISION HISTORY
 * Version 1.0 - Henrik Ekblad
 *
 * DESCRIPTION
 * Motion Sensor example using HC-SR501
 * http://www.mysensors.org/build/motion
 *
 */


 /******************************************************************* 
 * EDIT: June 03, 2017
 * DESCRIPTION 
 * As part of an one-year project at Herman Hollerith Zentrum (HHZ),
 * an IoT environment was set up. The original script was modified 
 * to integrate the sensor into our IoT environment.
 * 
 * ADDITIONAL INFORMATION
 * -  Used sensor: HC-SR501 (motion sensor)
 * -  Modified by manh3141 
 */

// Define meta-data for sensor
char MY_SENSOR_METADATA[] = "HHZ EG-125 Motion_TAG"; // Friendly-name of the sensor (replace "TAG" with your individual tag)
char MY_SKETCH_VERSION[] = "1.0"; // Sketch version

// Enable debug prints
#define MY_DEBUG

// Enable and select radio type attached
#define MY_RADIO_NRF24
//#define MY_RADIO_RFM69

// Include required libraries
#include <MySensors.h>

unsigned long SLEEP_TIME = 120000; // 2 minutes sleep time between reports (in milliseconds)
#define DIGITAL_INPUT_SENSOR 3   // The digital input you attached your motion sensor.  (Only 2 and 3 generates interrupt!)
#define CHILD_ID 1   // Id of the sensor child

// Initialize motion message
MyMessage msg(CHILD_ID, V_TRIPPED);

void setup()
{
	pinMode(DIGITAL_INPUT_SENSOR, INPUT); // sets the motion sensor digital pin as input
}

void presentation()
{
	sendSketchInfo(MY_SENSOR_METADATA, MY_SKETCH_VERSION);   // Send the sketch version information to the gateway and Controller
	present(CHILD_ID, S_MOTION);  // Register all sensors to gw (they will be created as child devices)
}

void loop()
{
	// Read digital motion value
	bool tripped = digitalRead(DIGITAL_INPUT_SENSOR) == HIGH;
	Serial.println(tripped);
  send(msg.set(tripped?"1":"0"));  // Send tripped value to gw

	// Sleep until interrupt comes in on motion sensor
	sleep(digitalPinToInterrupt(DIGITAL_INPUT_SENSOR), CHANGE, SLEEP_TIME);
}


