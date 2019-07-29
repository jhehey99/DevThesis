#ifndef __RFHELPER_H__
#define __RFHELPER_H__

#include <Arduino.h>
#include "RF24.h"
#include "RF24Network.h"

/* Definitions */
  /* TODO: Reassign RF_CE and RF_CS Values as needed */
  #define RF_CE       9   
  #define RF_CS       10
  #define DATA_SIZE   32

/* Initialization */
  /* RF  */
  RF24 radio(RF_CE, RF_CS);
  RF24Network network(radio);

  /* Network channel and address */
  const uint16_t channel  = 69;
  const uint16_t rootNode = 00;
  const uint16_t ecgNode  = 01;
  const uint16_t ppgNode  = 02;

  /* Buffer */
  char dataBuffer[DATA_SIZE] = { 0 };

/* Function Definitions */
  /* 
  * @param _to: address to write to 
  * @param _message: message to be sent over the network
  * @return bool: if successfully written to network
  */
  bool networkWrite(const uint16_t& _to, const String& _message) {

    // use dataBuffer to write messages
    memset(&dataBuffer[0], 0, DATA_SIZE);
    _message.toCharArray(dataBuffer, DATA_SIZE);

    // send the message over the network
    RF24NetworkHeader header(_to);
    return network.write(header, &dataBuffer, DATA_SIZE);
  }

#endif