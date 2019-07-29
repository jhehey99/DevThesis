#ifndef __WEBSOCKETHELPER_H__
#define __WEBSOCKETHELPER_H__

#include <WebSocketsClient.h>

/* Initialization */
WebSocketsClient webSocket;
const char* socketUrl   = "192.168.41.1";
const char* socketEvent = "send";
const int   socketPort  = 6969;
const int   socketDelay = 250;
const int   socketRetry = 50;
bool socketConnected    = false;

/* Function Definitions */
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.printf("[WSc] Disconnected!\n");
      socketConnected = false;
      break;
    case WStype_CONNECTED:
      Serial.printf("\n[WSc] Connected to url: %s\n",  payload);
      socketConnected = true;
      // socket.io upgrade confirmation message (required)
      webSocket.sendTXT("5");
      break;
  }
}

void connectToWebSocket() {
  int retryCount = 0;
  bool success = true;
  webSocket.beginSocketIO(socketUrl, socketPort);
  webSocket.onEvent(webSocketEvent);
  Serial.print("Connecting to WebSocket");
  while(!socketConnected) { 
    webSocket.loop();
    Serial.print('.');
    if(retryCount >= socketRetry) {
      Serial.println("\nMax retries reached...");
      success = false;
      break;
    }
    delay(socketDelay);
  }
  if(success) {
    Serial.println("\nSuccessfully connected to WebSocket...");
  } else {
    Serial.println("Failed to connect to WebSocket...");
  }
  delay(1000); // small pause
}

void emit(const String& event, const String& message, bool isJson = false) {
  if(socketConnected) {
    String txt("42[\"" + event + "\",");
    if(isJson) txt += message + "]";
    else txt += "\"" + message + "\"]";
    webSocket.sendTXT(txt);
  } else {
    Serial.println("[WSc] can't emit, webSocket not connected...");
  }
}


#endif