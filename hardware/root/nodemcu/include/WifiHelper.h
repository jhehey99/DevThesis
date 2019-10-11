#ifndef __WIFIHELPER_H__
#define __WIFIHELPER_H__

#include <Arduino.h>
#include <ESP8266WiFiMulti.h>

/* Initialization */
ESP8266WiFiMulti wiFiMulti;
const char *ssid = "Connectify-me";
const char *pass = "password";
const int wifiRetry = 30;
bool wifiConnected = false;

/* Function Definitions */
void connectToWifi()
{
  int retryCount = 0;
  wiFiMulti.addAP(ssid, pass);
  Serial.print("Connecting to WIFI");
  while (wiFiMulti.run() != WL_CONNECTED)
  {
    Serial.print('.');
    if (retryCount >= wifiRetry)
    {
      retryCount = 0;
      Serial.println("Failed to connect to WIFI...");
      Serial.println("Retrying to connect to WIFI...");
    }
    delay(10);
  }
  Serial.println("\nSuccessfully connected to WIFI...");
  wifiConnected = true;
  delay(100); // small pause
}

#endif