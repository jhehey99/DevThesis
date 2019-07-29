#ifndef __ARDUINOSERIALHELPER_H__
#define __ARDUINOSERIALHELPER_H__

#include <SoftwareSerial.h>

/* Definitions */
#define NODE_RX   5
#define NODE_TX   6
#define NODE_BAUD 9600

/* Initialization */
SoftwareSerial  nodeSerial(NODE_RX, NODE_TX);
char terminator = '~';

#endif