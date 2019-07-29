#include "Arduino.h"
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "Time.h"
#include "JsonBuilder.h"

#define ADDRESS_SIZE  6
#define DATA_SIZE     32
#define INT_SIZE      10

const byte address[ADDRESS_SIZE] = "00001";
char data_buffer[DATA_SIZE] = "";
char int_buffer[INT_SIZE] = "";

//Creating an object
RF24 radio(9,10); 

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

long t_start;
double t;

/* SETUP */
void setup() {
  initRfWrite();
  Serial.begin(9600);
  Serial.println("NODE SETUP...");
  t_start = millis();
}

float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)
int value = 0;

Time time;

JsonBuilder builder;


void _rfWriteLine(const String& data, const int dataLength){
  int begin = 0;
  while(begin < dataLength) {
    data.toCharArray(data_buffer, DATA_SIZE, begin);
    Serial.println(data_buffer);
    radio.write(&data_buffer, DATA_SIZE);
    memset(&data_buffer[0], 0, DATA_SIZE);
    begin += DATA_SIZE;
  }
}


// TODO: IPADDING MO UNG MILLISECOND KASI MAY PROBLEMA SA STRING COMPARISON
/* LOOP */
void loop() {
  // get delta time
  t = (millis() - t_start) / 1000.0;
  // get new value
  value = 512 * sin(2 * PI * f_sin * t) + 512;

  // create entry { time, value }
  sprintf(int_buffer,"%d", value);
  String entry = time.getTime() + ',' + int_buffer;

  if(builder.getBodyCount() < 32) {
    builder.addData(entry);
  } else {
    builder.endData();
    _rfWriteLine(builder.getJson(), builder.getDataLength());
    builder.clear();
  }
  // Serial.println(entry);
  // rfWriteLine(entry);
  delay(10);
}
