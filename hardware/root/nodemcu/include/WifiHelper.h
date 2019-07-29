#ifndef __WIFIHELPER_H__
#define __WIFIHELPER_H__

#include <Arduino.h>
#include <ESP8266WiFiMulti.h>

/* Initialization */
ESP8266WiFiMulti wiFiMulti;
const char* ssid = "Connectify-me";
const char* pass = "password";
const int wifiRetry  = 30;
const int wifiDelay = 250;
bool wifiConnected = false;

/* Function Definitions */
void connectToWifi() {
  int retryCount = 0;
  bool success = true;
  wiFiMulti.addAP(ssid, pass);
  Serial.print("Connecting to WIFI");
  while(wiFiMulti.run() != WL_CONNECTED) {
    Serial.print('.');
    if(retryCount >= wifiRetry) {
      Serial.println("\nMax retries reached...");
      success = false;
      break;
    }
    delay(wifiDelay);
  }
  if(success) {
    Serial.println("\nSuccessfully connected to WIFI...");
    wifiConnected = true;
  } else {
    Serial.println("Failed to connect to WIFI...");
  }
  delay(1000); // small pause
}

#endif