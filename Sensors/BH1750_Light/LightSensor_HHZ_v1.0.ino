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
 * Version 1.0 - idefix
 * 
 * DESCRIPTION
 * Arduino BH1750FVI Light sensor
 * communicate using I2C Protocol
 * this library enable 2 slave device addresses
 * Main address  0x23
 * secondary address 0x5C
 * connect the sensor as follows :
 *
 *   VCC  >>> 5V
 *   Gnd  >>> Gnd
 *   ADDR >>> NC or GND  
 *   SCL  >>> A5
 *   SDA  >>> A4
 * http://www.mysensors.org/build/light
 */


/******************************************************************* 
 * EDIT: June 03, 2017
 * DESCRIPTION 
 * As part of an one-year project at Herman Hollerith Zentrum (HHZ),
 * an IoT environment was set up. The original script was modified 
 * to integrate the sensor into our IoT environment.
 * 
 * ADDITIONAL INFORMATION
 * -  Used sensor: BH 1750 (light sensor)
 * -  Cabling: ADDR was left out
 * -  Integrate the BH 1750 library from https://github.com/mysensors/MySensorsArduinoExamples/tree/master/libraries/BH1750
 *    before compiling this script
 * -  Modified by manh3141 
 */

// Define sensor meta data
char MY_SENSOR_METADATA[] = "HHZ _LOC_ Light_TAG_"; // Friendly-name of the sensor (replace _TAG_ with your individual tag and _LOC_ with the location of the sensor)
char MY_SKETCH_VERSION[] = "1.0"; // Sketch version

// Enable debug prints to serial monitor
#define MY_DEBUG 

// Enable and select radio type attached
#define MY_RADIO_NRF24
//#define MY_RADIO_RFM69

// Include required libraries
#define MY_NODE_ID 3 // Node id
#include <SPI.h>
#include <MySensors.h>  
#include <BH1750.h>
#include <Wire.h>

#define CHILD_ID_LIGHT 1
unsigned long SLEEP_TIME = 600000; // 10 minute sleep time between reports (in milliseconds)

BH1750 lightSensor;

// V_LIGHT_LEVEL should only be used for uncalibrated light level 0-100%.
// If your controller supports the new V_LEVEL variable, use this instead for
// transmitting LUX light level.
MyMessage msg(CHILD_ID_LIGHT, V_LIGHT_LEVEL);
// MyMessage msg(CHILD_ID_LIGHT, V_LEVEL);  

void setup(){ 
  lightSensor.begin();
}

void presentation()  {
  sendSketchInfo(MY_SENSOR_METADATA, MY_SKETCH_VERSION); // Send the sketch version information to the gateway and controller
  present(CHILD_ID_LIGHT, S_LIGHT_LEVEL); // Register all sensors to gateway (they will be created as child devices)
}

void loop()      
{     
  uint16_t lux = lightSensor.readLightLevel(); // Get Lux value
  Serial.println(lux);
  send(msg.set(lux)); 
  sleep(SLEEP_TIME);
}
