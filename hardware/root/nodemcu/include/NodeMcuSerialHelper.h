#ifndef __NODEMCUSERIALHELPER_H__
#define __NODEMCUSERIALHELPER_H__
#include <Arduino.h>
#include <SoftwareSerial.h>

/* Definitions */
#define MASTER_RX   D6
#define MASTER_TX   D5
#define MASTER_BAUD 9600

/* Initialization */
SoftwareSerial  masterSerial(MASTER_RX, MASTER_TX);
String          masterData;

#endif