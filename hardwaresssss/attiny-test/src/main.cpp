#include "Arduino.h"
// #include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "Time.h"

#define ADDRESS_SIZE  6
#define DATA_SIZE     32
#define INT_SIZE      10

const byte address[ADDRESS_SIZE] = "00001";
char data_buffer[DATA_SIZE] = "";
char int_buffer[INT_SIZE] = "";

//Creating an object
RF24 radio(6, 7); 

void initRfWrite() {
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void rfWriteLine(char data[]) {
  strncpy(data_buffer, data, strlen(data));
  radio.write(&data_buffer, DATA_SIZE);
  memset(&data_buffer[0], 0, DATA_SIZE);
}

void rfWriteLine(String data) {
  data.toCharArray(data_buffer, DATA_SIZE);
  radio.write(&data_buffer, DATA_SIZE);
  memset(&data_buffer[0], 0, DATA_SIZE);
}

/* SETUP */
void setup() {
  initRfWrite();
  Serial.begin(9600);
  Serial.println("NODE SETUP...");
}

int value = 0;
int f = 100;
int tms = 1.0 / f * 1000;
float angle = 0;

Time t;

// TODO: IPADDING MO UNG MILLISECOND KASI MAY PROBLEMA SA STRING COMPARISON
/* LOOP */
void loop() {
  // get new value
  value = 512 * sin(2 * PI * angle) + 512;
  angle += (1.0/f);
  sprintf(int_buffer,"%d", value);
  String entry = t.getTime() + ',';
  entry.concat(int_buffer);
  Serial.println(entry);
  rfWriteLine(entry);
  delay(tms);
}
