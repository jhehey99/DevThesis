/*
  #include <Arduino.h>

  #define led 3

  void on(int ms = 100) {
    digitalWrite(led, HIGH);
    delay(ms);
  }

  void off(int ms = 100) {
    digitalWrite(led, LOW);
    delay(ms);
  }

  void setup() {
    // put your setup code here, to run once:
    pinMode(led, OUTPUT);
    on(); off(); on(); off(); on(); off(); 
    delay(500);
    on(); off(); on(); off(); on(); off(); 
    delay(500);
    on(); off(); on(); off(); on(); off(); 
    delay(500);
  }

  void loop() {
    // put your main code here, to run repeatedly:
    on(500);
    off(500);
  }
*/



#include <RF24Network.h>
#include <RF24.h>

RF24 radio(3, 4);                    // nRF24L01(+) radio attached using Getting Started board 

RF24Network network(radio);          // Network uses that radio

const uint16_t this_node = 01;        // Address of our node in Octal format
const uint16_t other_node = 00;       // Address of the other node in Octal format

const unsigned long interval = 200; //ms  // How often to send 'hello world to the other unit

unsigned long last_sent;             // When did we last send?
unsigned long packets_sent;          // How many have we sent already


struct payload_t {                  // Structure of our payload
  unsigned long ms;
  unsigned long counter;
};

#define led 3

void on(int ms = 100) {
  digitalWrite(led, HIGH);
  delay(ms);
}

void off(int ms = 100) {
  digitalWrite(led, LOW);
  delay(ms);
}

void setup(void)
{
  // radio.begin();
  // network.begin(/*channel*/ 90, /*node address*/ this_node);
  pinMode(led, OUTPUT);
  on(); off(); on(); off(); on(); off(); 
  delay(500);
  on(); off(); on(); off(); on(); off(); 
  delay(500);
  on(); off(); on(); off(); on(); off(); 
  delay(500);

}

void loop() {
  on(500); off(500);
  // network.update();                          // Check the network regularly
  // payload_t payload = { millis(), packets_sent++ };
  // RF24NetworkHeader header(/*to node*/ other_node);
  // bool ok = network.write(header,&payload,sizeof(payload));
}

 