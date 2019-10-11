#include "RFHelper.h"
#include "WifiHelper.h"
#include "WebSocketHelper.h"

/* Verify Signal Event Definitions */

void onSendBloodPressureSignal()
{
  network.update();
  Serial.println("On Send Blood Pressure Signals");
  RF24NetworkHeader header(ppgArmNode);
  strncpy(dataBuffer, "setMode:BP", DATA_SIZE);
  bool ok = network.write(header, &dataBuffer, DATA_SIZE);
  Serial.print("OK: ");
  Serial.println(ok);
}

void onSendOxygenSaturationSignal()
{
  network.update();
  Serial.println("On Send Oxygen Saturation Signals");
  RF24NetworkHeader header(ppgArmNode);
  strncpy(dataBuffer, "setMode:OS", DATA_SIZE);
  bool ok = network.write(header, &dataBuffer, DATA_SIZE);
  Serial.print("OK: ");
  Serial.println(ok);
}

void setup()
{ /* COM13 */

  /* Set Verify Signal Event Handlers */
  SendBloodPressureSignal = &onSendBloodPressureSignal;
  SendOxygenSaturationSignal = &onSendOxygenSaturationSignal;

  /* Serial Monitor */
  Serial.begin(9600);
  Serial.flush();
  Serial.println("\nSetup...");

  /* RF24 */
  rfInit(rootNode);

  /* Wifi */
  connectToWifi();

  /* Web Socket */
  connectToWebSocket();
}

void loop()
{
  // put your main code here, to run repeatedly:
  verifySocket();
  network.update();
  //webSocket.loop();

  while (network.available())
  {
    // read from the RF
    RF24NetworkHeader header;
    network.read(header, &dataBuffer, DATA_SIZE);

    // convert data buffer to string
    String data = String(dataBuffer);
    Serial.println(data);

    // emit to the web socket
    emit(socketSendEvent, data);
  }
}
