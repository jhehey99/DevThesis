#include "RFHelper.h"
#include "ArduinoSerialHelper.h"

/* Definitions */
/* Initialization */
/* Function Definitions */

void setup() { /* COM3 */
  // put your setup code here, to run once:
  Serial.begin(9600);
  nodeSerial.begin(NODE_BAUD);
  rfInit(rootNode);
}

void loop() {
  // put your main code here, to run repeatedly:
  network.update();
  while(network.available()) {
    // read from the RF
    RF24NetworkHeader header;
    network.read(header, &dataBuffer, DATA_SIZE);

    // terminate the string
    String data = String(dataBuffer) + terminator;
    Serial.println(data);

    // send data to nodemcu
    nodeSerial.print(data);
  }
}
