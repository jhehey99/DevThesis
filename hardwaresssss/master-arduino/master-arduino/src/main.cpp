
// receiver

#include "Arduino.h"
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "JsonBuilder.h"
#include <SoftwareSerial.h>

#define IDX_TIME      0
#define IDX_VALUE     1
#define DATA_SIZE     32

#define NODE_RX   5
#define NODE_TX   6

#define RF_CE     9
#define RF_CS     10

SoftwareSerial  nodeSerial(NODE_RX, NODE_TX);
RF24            radio(RF_CE, RF_CS);
JsonBuilder     builder;
const byte      address[6] = "00001";

void testCreateData(char* data) {
  if(builder.getBodyCount() >= 10) {
    // SEND TO NODEMCU TO POST
    String json = builder.getJson();
    nodeSerial.print(json);
    Serial.println("ETO UNG JSON"); // can rm
    Serial.println(json);           // can rm
    builder.clear();
  } else {
    // split ung data into time and value. ',' ang delimeter
    String time, value;
    int len = strlen(data);
    for(int i = 0; i < len; i ++) {
      if(data[i] == ',') {
        String dataStr = String(data);
        time = dataStr.substring(0, i);
        value = dataStr.substring(i+1, len);
      }
    }
    builder.addData(time, value);
    // builder.addBody(time, value);
  }
}

void setup() {
  Serial.begin(9600);
  nodeSerial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    char data[DATA_SIZE] = "";
    radio.read(&data, sizeof(data));
    String nodeData = String(data) + '~';
    Serial.println(nodeData);
    nodeSerial.print(nodeData);
    // testCreateData(data);
  }
}





















// TODO, MAGKAIBA PALA UNG PIPE NG
// READING AND WRITING NG RF

//TODO ESP SEND THROUGH WIFI UNG NARECEIVE NA DATA 

// #include "Arduino.h"
// // #include "Master.h"
// #include "RfStream.h"
// #include <SoftwareSerial.h>
// #include <math.h>


// SoftwareSerial nodeSerial(5, 6); // RX TX

// void setup() {
//   Serial.begin(9600);
//   nodeSerial.begin(115200);
// }


// int value = 0;
// int f = 60;
// int tms = 1.0 / f * 1000;
// float angle = 0;

// void loop() {

//   // get new value
//   value = 512 * sin(2 * PI * angle) + 512;
//   angle += (1.0/f);
//   Serial.println(value);

//   String valStr = String(value) + "\n";
//   nodeSerial.print(valStr);
//   // nodeSerial.println(value);
//   delay(tms);
// }




























// SoftwareSerial NodeSerial(5, 6); // Rx, Tx

// char text[32] = "";
// void receive() {
//   if(radio.available()) {
//     // char text[32] = "";
//     radio.read(&text, sizeof(text));
//     Serial.println(text);
//   }
// }

// void setup() {
//   Serial.begin(9600);
//   // initMaster();
//   // initSampling();  
//   // initRfRead();
//   NodeSerial.begin(9600);
//   pinMode(5, INPUT);
//   pinMode(6, OUTPUT);
// }

// void loop() {
//   // initMaster();
//   // initSampling();
//   // receive();
//   NodeSerial.listen();
//   if(NodeSerial.available() > 0) {
//     NodeSerial.write(text);
//   }

//   delay(500);
// }
