// #include "RFHelper.h"

#include "ATTiny/RF24_arch_config.h"
// /* Initialization */
//   /* Sine wave function */
//   long t_start;
//   double t;
//   int value = 0;
//   float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)

// void setup() {
//   // put your setup code here, to run once:
//   radio.begin();
//   network.begin(channel, ecgNode);
// }

// void loop() {
//   // put your main code here, to run repeatedly:
//   network.update();

//   // get delta time
//   t = (millis() - t_start) / 1000.0;
//   // get new value
//   value = 512 * sin(2 * PI * f_sin * t) + 512;

//   String valueStr(value);
//   valueStr += " : TINY ECG";
//   networkWrite(rootNode, valueStr);
// }
// CE and CSN are configurable, specified values for ATtiny85 as connected above
#define CE_PIN 3
#define CSN_PIN 4
//#define CSN_PIN 3 // uncomment for ATtiny85 3 pins solution
#include "RF24.h"
RF24 radio(CE_PIN, CSN_PIN);
byte addresses[][6] = {
  "1Node","2Node"};
unsigned long payload = 0;
void setup() {
  // Setup and configure rf radio
  radio.begin(); // Start up the radio
  radio.setAutoAck(1); // Ensure autoACK is enabled
  radio.setRetries(15,15); // Max delay between retries & number of retries
  radio.openWritingPipe(addresses[1]); // Write to device address '2Node'
  radio.openReadingPipe(1,addresses[0]); // Read on pipe 1 for device address '1Node'
  radio.startListening(); // Start listening
}
void loop(void){
  
  radio.stopListening(); // First, stop listening so we can talk.
  payload++;
  radio.write( &payload, sizeof(unsigned long) );
  radio.startListening(); // Now, continue listening
    unsigned long started_waiting_at = micros(); // Set up a timeout period, get the current microseconds
  boolean timeout = false; // Set up a variable to indicate if a response was received or not
  while ( !radio.available() ){ // While nothing is received
    if (micros() - started_waiting_at > 200000 ){ // If waited longer than 200ms, indicate timeout and exit while loop
      timeout = true;
      break;
    }
  }
  if ( !timeout ){ // Describe the results
    unsigned long got_time; // Grab the response, compare, and send to debugging spew
    radio.read( &got_time, sizeof(unsigned long) );
  }
  // Try again 1s later
  delay(1000);
}