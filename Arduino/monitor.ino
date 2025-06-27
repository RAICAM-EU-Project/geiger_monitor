/*!
  @file geiger.ino
  @brief    Detect CPM radiation intensity and expose it via I2C
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd
  @licence     The MIT License (MIT)
  @author [fengli]
  @version  V1.0
  @date  2021-9-17
  @get from https://www.dfrobot.com
*/

#include <DFRobot_Geiger.h>
#include <Wire.h>

#if defined ESP32
#define detect_pin D3
#else
#define detect_pin 7
#endif

DFRobot_Geiger geiger(detect_pin);

// Latest radiation value
float radiation_uSvh = 0.0;

void setup()
{
  Serial.begin(115200);
  geiger.start();

  // Start I2C as slave at address 0x08
  Wire.begin(0x08);
  Wire.onRequest(sendRadiation);
}

void loop()
{
  delay(1000);  // Read every 1 second
  radiation_uSvh = geiger.getuSvh();
  //Serial.print("Radiation (uSv/h): ");
  Serial.println(radiation_uSvh);
}

// Called when Jetson requests data
void sendRadiation()
{
  byte* data = (byte*)&radiation_uSvh;
  Wire.write(data, sizeof(float));
}
