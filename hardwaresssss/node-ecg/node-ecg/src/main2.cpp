// // transmitter
// #include "Arduino.h"
// #include <SPI.h>                            //Communication Interface with modem
// #include "nRF24L01.h"
// #include "RF24.h"                          //library to control radio modem
// #include "string.h"
// #include <ArduinoJson.h>
// #include <math.h>
// #include<stdio.h> 


 
// #define ADDRESS_SIZE  6
// #define START_SIZE    5
// #define STOP_SIZE     4
// #define TYPE_SIZE     6
// #define DATA_SIZE     32
// #define INT_SIZE      10

// const byte address[ADDRESS_SIZE] = "00001";
// char start[START_SIZE] = "START";
// char stop[STOP_SIZE] = "STOP";
// char type[TYPE_SIZE] = "TYPE:1";
// char data_buffer[DATA_SIZE] = "";

// //Creating an object
// RF24 radio(9,10); 

// void rfSetup()
// {
//   radio.begin();
//   radio.openWritingPipe(address);
//   radio.setPALevel(RF24_PA_MIN);
//   radio.stopListening();
// }

// void rfStartWrite()
// {
//   radio.write(&start, START_SIZE);
//   delay(10);
//   radio.write(&type, TYPE_SIZE);
//   delay(10);
// }

// void rfWriteLine(char data[])
// {
//   strncpy(data_buffer, data, strlen(data));
//   radio.write(&data_buffer, DATA_SIZE);
//   memset(&data_buffer[0], 0, DATA_SIZE);
//   delay(10);
// }

// void rfStopWrite()
// {
//   radio.write(&stop, STOP_SIZE);
//   radio.write("\n", 2);
//   delay(10);
// }



// int x = 0;
// int count = 10;




// void receive() {
//   if(radio.available()) {
//     char text[32] = "";
//     radio.read(&text, sizeof(text));
//     Serial.println(text);
//   }
// }

// // open reading pipe
// // open writing pipe

// void initRfRead() {
//   radio.begin();
//   radio.openReadingPipe(0, address);
//   radio.setPALevel(RF24_PA_MIN);
//   radio.startListening();
// }

// void initRfWrite() {
//   radio.begin();
//   radio.openWritingPipe(address);
//   radio.setPALevel(RF24_PA_MIN);
//   radio.stopListening();
// }

// void setup() {
//     // rfSetup();
//   // initRfRead();
//   initRfWrite();
//   Serial.begin(9600);
//   Serial.println("NODE SETUP...");

// }
// // \ TODO PANO PAGKAMAGKAIBA NG ADDRESS
// // \ DAPAT MAGKAIBA RIN NG PIPE

// // \ TODO: PARSE THE DATA,
// // \ GET TYPE
// // \ GET CONTENT

// int value = 0;
// float angle = 0;


//   char int_buffer[INT_SIZE] = "";

// void loop() {
//   // receive();

//   value = (512*sin(M_PI*angle)) + 512;
//   angle += 0.05;

//   sprintf(int_buffer,"%d", value);

//   char d[] = "Data: ";
//   strncat(d, int_buffer, INT_SIZE);

//   Serial.print("BUFFER: ");
//   Serial.println(int_buffer);
  
//   rfWriteLine(d);

//   delay(100);

//     // rfStartWrite();

//     // char d[] = "hello hello ";

//     // // int to string
//     // snprintf(int_buffer, INT_SIZE, "%d", x);
    
//     // // concatenate string
//     // strncat(d, int_buffer, INT_SIZE);

//     // rfWriteLine(d);
//     // delay(1000);
//     // x ++;

//     // count --;
//     // if (count <= 0) {
//     //   rfStopWrite();
//     //   count = 10;
//     //   delay(3000);
//     // }
// }

