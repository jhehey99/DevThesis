#include "RFHelper.h"

/* Definitions */
/* Initialization */
/* Function Definitions */

void setup() { /* COM3 */
  // put your setup code here, to run once:
  Serial.begin(9600);
  radio.begin();
  network.begin(channel, rootNode);
}

void loop() {
  // put your main code here, to run repeatedly:
  network.update();
  while(network.available()) {
    RF24NetworkHeader header;
    network.read(header, &dataBuffer, DATA_SIZE);
    Serial.println(dataBuffer);
  }
}
