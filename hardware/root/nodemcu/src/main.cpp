#include "NodeMcuSerialHelper.h"
#include "RFHelper.h"
#include "WifiHelper.h"
#include "WebSocketHelper.h"

void setup() { /* COM16 */

  /* Serial Monitor */ 
  Serial.begin(9600);
  Serial.flush();
  Serial.println("\nSetup...");

  /* RF24 */
  rfInit(rootNode);

  /* Master Serial */
  // masterSerial.begin(MASTER_BAUD);
  // masterSerial.flush();

  /* Wifi */
  connectToWifi();
  
  /* Web Socket */
  connectToWebSocket();
}
void loop() {
  // put your main code here, to run repeatedly:
  network.update();

  while(network.available()) {
		webSocket.loop();

		// read from the RF
		RF24NetworkHeader header;
		network.read(header, &dataBuffer, DATA_SIZE);

		// convert data buffer to string
		String data = String(dataBuffer);
		// Serial.println(data);

		// emit to the web socket
		emit(socketEvent, data);
	}
}


// void loop() {
//   // required in Web Socket
//   webSocket.loop();

//   if(masterSerial.available() > 0) {
//     masterData = masterSerial.readStringUntil('~');
//     // Serial.println(masterData);

//     // send data through websocket
//     emit(socketEvent, masterData);
//   }
// }