#ifndef __MASTER_H__
#define __MASTER_H__

#include "Arduino.h"
#include "RfStream.h"

// \ Master State
typedef enum { Standby, Ready, Sampling, End } state_t;
state_t state;

// \ Master Functions

// \ initialize master arduino
void initMaster() {
    state = Standby;
    Serial.println("Initializing Master...");
    delay(5);
}

// \ changes the state of the master arduino
void nextState() {
    if(state == End)
        state = Standby;
    else
        state = (state_t) (((int) state) + 1);
    
    Serial.print("State Changed, State = ");
    Serial.println((int) state);
}

void initSampling() {
    Serial.println("Initializing Sampling...");
    // \ dapat naka standby bago mag initialize sampling
    if(state != Standby)
        return;

    // \ ready state
    nextState();

    // \ send Ready signal to the nodes
    /*  START
     *  CMD:1
     *  STOP
     */

    // \ start write muna
    // \ writeline (content = READY)

    // \ ready signal to string
    itostr((int) state);
    initRfWrite();
    rfStartWrite(CMD);
    rfWriteLine(int_buffer);
    rfStopWrite();
}





#endif
