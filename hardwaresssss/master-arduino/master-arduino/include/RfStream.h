#ifndef __RFSTREAM_H__
#define __RFSTREAM_H__

#include "Arduino.h"
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "Utils.h"

#define ADDRESS_SIZE  6
#define START_SIZE    5
#define STOP_SIZE     4
#define TYPE_SIZE     6
#define CONTENT_SIZE  32
#define HCONTENT_SIZE 7

const byte address[ADDRESS_SIZE] = "00001";
char start[START_SIZE] = "START";
char stop[STOP_SIZE] = "STOP";
char type[TYPE_SIZE] = "TYPE:"; // TODO, FUNCTION TO RESET TYPE
char content_header[HCONTENT_SIZE] = "CONTENT";
char content_buffer[CONTENT_SIZE] = "";

// \ RF object
RF24 radio(9,10);

// \ RF can write command or data
typedef enum { CMD, DAT } content_t;

// \ RF is busy when it is writing content_buffer
bool busy = false;

void initRf() {
    Serial.println("Initializing RFStream...");
    busy = false;
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MIN);
    radio.stopListening();
    delay(5);
}

void initRfRead() {
    Serial.println("RFStream - Initialize Reading Pipe...");
    radio.begin();
    radio.openReadingPipe(0, address);
    radio.setPALevel(RF24_PA_MIN);
    radio.startListening();
}

void initRfWrite() {
    Serial.println("RFStream - Initialize Writing Pipe...");
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MIN);
    radio.stopListening();
}

// TODO: READ AND WRITE PALITAN UNG INITRF

void rfStartWrite(content_t cnt_t) {
    if(busy) {
        Serial.println("RF is busy...");
        return;
    }

    Serial.println("RF StartWrite...");

    // \ convert cnt_t to string and append to type buffer
    itostr((int) cnt_t);
    strncat(type, int_buffer, INT_SIZE);

    // \ write START signal
    radio.write(&start, START_SIZE);
    // \ write type of content to be sent
    radio.write(&type, TYPE_SIZE);
    // \ remove content type
    type[TYPE_SIZE-1] = '\0';

    Serial.println("RF START sent...");
}

void rfWriteLine(char content[]) {
    Serial.println("RF Writing contents...");
    busy = true;
    strncpy(content_buffer, content, strlen(content));
    radio.write(&content_header, HCONTENT_SIZE);
    radio.write(&content_buffer, CONTENT_SIZE);
    delay(10);
}

void rfStopWrite() {
    Serial.println("RF StopWrite...");

    // \ write STOP signal
    radio.write(&stop, STOP_SIZE);
    // \ rf is not busy anymore
    busy = false;

    // \ flush the transmit buffer
    radio.flush_tx();

    Serial.println("RF STOP sent...");
}

#endif