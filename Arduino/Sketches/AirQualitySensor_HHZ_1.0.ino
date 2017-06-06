/******************************************************************* 
 * EDIT: June 05, 2017
 * DESCRIPTION 
 * As part of an one-year project at Herman Hollerith Zentrum (HHZ),
 * an IoT environment was set up. The original script was modified 
 * to integrate the sensor into our IoT environment.
 * 
 * ADDITIONAL INFORMATION
 * -  Used sensor: MQ-135 (air quality sensor)
 * -  Please refer to the MQ-135s official data sheet at: https://www.mysensors.org/dl/57c3ebeb071cb0e34c90057a/design/SNS-MQ135.pdf
 * -  This sketch is based on Georg Krocker's MQ-135 Arduino Library. Please refer to at it: https://hackaday.io/project/3475-sniffing-trinket/log/12363-mq135-arduino-library
 * -  NOTE: According to the datasheet, the sensor is capable of detecting NH3, NOx, alcohol, benzene, smoke and CO2. However, this sketch only focuses on CO2. Therefore, the sensor is calibrated to measure CO2 concentrations in ppm.
 * -  NOTE: Only use the code between "START" and "END" in the setup-function if the sensor has been turned off for more than 15 minutes or has been relocated to another place. Else, comment it for a faster start.
 * -  NOTE: Use the calculated calibration value, respectively 'RZERO' to calibrate the sensor according to atmospheric CO2 levels (400ppm). Replace the RZERO value in MQ135.h by the calculated RZERO value of this script.
 * -  NOTE: Calibration should be done on fresh air.
 * -  Modified by manh3141 
 */

// Define meta-data for sensor
char MY_SENSOR_METADATA[] = "HHZ EG-125 AirQuality_TAG"; // Friendly-name of the sensor (replace "TAG" with your individual tag)
char MY_SKETCH_VERSION[] = "1.0"; // Sketch version

// Enable debug prints
#define MY_DEBUG

// Enable and select radio type attached
#define MY_RADIO_NRF24
//#define MY_RADIO_RFM69

// Include required libraries
#include <MySensors.h>
#include "MQ135.h"

// Define global variables
MQ135 gasSensor = MQ135(A0); // Define 'A0' as input pin for data
#define CHILD_ID 1   // Id of the sensor child
unsigned long SLEEP_TIME = 60000; // 1 minute sleep time between reports (in milliseconds)

// Initialize airquality message
MyMessage msg(CHILD_ID, V_LEVEL);


void setup() {
  Serial.begin(115200);

  // ***** START *****
  // Only run this section highlighted by "START" and "END" if the sensor has been turned off for more than 15 minutes or has been relocated to another place.
  // Else you can comment it for a faster start since the sensor is still calibrated correctly.
  
  // Let the sensor warm up for two minutes (required for getting accurate values)
  delay(120000);

  // Calculate a calibration value (used for calibrating the sensor in MQ135.h by replacing the RZERO value)
  Serial.println("Sensor warm-up started");

  float calibrVal = 0;
  float i = 5; // Set calibration duration to 5 minutes
  for(int x = (int) i; x > 0; x--){   
    Serial.print("Sensor warm-up in progress - ");
    Serial.print(x);
    Serial.println(" minute(s) left");
    delay(60000);
    calibrVal = calibrVal + gasSensor.getRZero(); // Cumulate the collected rzero values
  }

  Serial.println("Sensor warm-up finished - ready to use");
  Serial.println("---");
  calibrVal = calibrVal / i; // Calculate the average calibration value
  Serial.print("Calibration value: ");
  Serial.println(calibrVal);
  Serial.println("---");

  // ***** END *****
}

void presentation(){
  sendSketchInfo(MY_SENSOR_METADATA, MY_SKETCH_VERSION);   // Send the sketch version information to the gateway and Controller
  present(CHILD_ID, S_AIR_QUALITY);  // Register all sensors to gw (they will be created as child devices)
}

void loop() {
  float ppmVal = gasSensor.getPPM(); // Get the current CO2 ppm value
  Serial.println(ppmVal);
  send(msg.set((int16_t)ceil(ppmVal)));  // Typecast ppmVal from float to int and send the ppm value to gw
  sleep(SLEEP_TIME); // Sleep until another message is sent to the gateway
}
