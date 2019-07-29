/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>

#include "JsonBuilder.h"



#define OK 200

#define MASTER_RX   D6
#define MASTER_TX   D5

SoftwareSerial  masterSerial(MASTER_RX, MASTER_TX);
JsonBuilder     builder;
WiFiClient      client;



/* WIFI CONNECTION */
ESP8266WiFiMulti wiFiMulti;

const char* ssid = "Connectify-me";
const char* pass = "password";
const int maxRetry = 30;
bool connected = false;
const int connectingDelay = 500;

void connectToWifi() {
  int retryCount = 0;
  bool success = true;
  wiFiMulti.addAP(ssid, pass);
  Serial.print("Connecting to WIFI");
  while(wiFiMulti.run() != WL_CONNECTED) {
    Serial.print('.');
    if(retryCount >= maxRetry) {
      Serial.println("\nMax retries reached...");
      success = false;
      break;
    }
    delay(connectingDelay);
  }
  if(success) {
    Serial.println("\nSuccessfully connected to WIFI...");
    connected = true;
  } else {
    Serial.println("Failed to connect to WIFI...");
  }
}





/* HTTP SAMPLE POST */
// void httpPost() {
//   // post the json content
//   if(!connected) {
//     Serial.println("Can't Post to server, not connected to wifi...");
//     return;
//   }

//   // get the json string from the builder
//   String content = builder.getJson();
//   Serial.println("ETO UNG JSON");
//   Serial.println(content);

//   // create http client and post the json
//   HTTPClient http;
//   http.begin("http://192.168.41.1:80/display");
//   http.addHeader("Content-Type", "application/json");
//   int httpCode = http.POST(content);
//   String payload = http.getString();
//   Serial.print(httpCode);
//   Serial.print(' ');
//   Serial.println(payload);
//   http.end();
// }

/* HTTP SAMPLE POST */

HTTPClient http;
void httpInit() {
  http.setReuse(true);
  http.begin("http://192.168.41.1:80/display");
  http.addHeader("Content-Type", "application/json");
}

void httpPost(String content) {
  // post the json content
  if(!connected) {
    Serial.println("Can't Post to server, not connected to wifi...");
    return;
  }

  int statusCode = http.POST(content);


  Serial.print("Status Code: ");
  Serial.print(statusCode);

  if(statusCode == OK) {
    Serial.println("OK");
  } else {
    Serial.println("NOT OK");
  }
}

// void testBuildJsonPost(String dataa) {
//     // create json builder object and add body to it
//   if(builder.getBodyCount() > 20) {
//     httpPost(dataa);
//     builder.clear();
//   } else {
//     builder.addBody("10:69:69", dataa);
//   }
// }

#include <WebSocketsClient.h>

WebSocketsClient webSocket;
bool socketConnected = false;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.printf("[WSc] Disconnected!\n");
      socketConnected = false;
      break;
    case WStype_CONNECTED:
      Serial.printf("[WSc] Connected to url: %s\n",  payload);
      socketConnected = true;
      // send message to server when Connected
      // socket.io upgrade confirmation message (required)
      webSocket.sendTXT("5");
      break;
    case WStype_TEXT:
      //Serial.printf("[WSc] get text: %s\n", payload);

      // send message to server
      // webSocket.sendTXT("message here");
      break;
    case WStype_BIN:
      Serial.printf("[WSc] get binary length: %u\n", length);
      hexdump(payload, length);

      // send data to server
      // webSocket.sendBIN(payload, length);
      break;
  }
}

//DITO WEBSOCKET
void connectToWebSocket() {
  int retryCount = 0;
  bool success = true;
  webSocket.beginSocketIO("192.168.41.1", 6969);
  webSocket.onEvent(webSocketEvent);
  Serial.print("Connecting to WebSocket");
  while(!socketConnected) { 
    webSocket.loop();
    Serial.print('.');
    if(retryCount >= maxRetry * 2) {
      Serial.println("\nMax retries reached...");
      success = false;
      break;
    }
    delay(connectingDelay);
  }
  if(success) {
    Serial.println("\nSuccessfully connected to WebSocket...");
  } else {
    Serial.println("Failed to connect to WebSocket...");
  }
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

/* SETUP */
void setup() {
  Serial.begin(9600);
  masterSerial.begin(9600);
  Serial.println("\nSetup...");
  connectToWifi();
  httpInit();
  connectToWebSocket();
}

// int data;
String data;
int f = 60;
int tms = 1 / f * 1000;

/* LOOP */
void loop() {
  webSocket.loop();
  if(masterSerial.available() > 0) {
    data = masterSerial.readStringUntil('~');
    Serial.println(data);
    // httpPost(data);
    // Serial.println("NODE ETO NA UNG DATA");
    // testBuildJsonPost(data);
    // masterSerial.flush();
    // Serial.print(data);

    emit("send", data);
  }
}



// SoftwareSerial NodeSerial(D6,D5); // (Rx, Tx)

// void setup() {

//   // Serial.begin(9600);
//   // Serial.setDebugOutput(true);


//   // Serial.println();
//   // Serial.println();
//   // Serial.println();

//   // for (uint8_t t = 4; t > 0; t--) {
//   //   Serial.printf("[SETUP] WAIT %d...\n", t);
//   //   Serial.flush();
//   //   delay(1000);
//   // }

//   // WiFi.mode(WIFI_STA);
//   // WiFiMulti.addAP("Connectify-me", "connectipassword");

//   // para sa master to node
//   NodeSerial.begin(9600);
//   Serial.begin(9600);

//   pinMode(D6, INPUT);
//   pinMode(D5, OUTPUT);
//   Serial.println("NODE DATA");
// }

// int data;

// void loop() {
//   // read ung sinend nung master arduino
//   if(NodeSerial.available() > 0) {
//     data = NodeSerial.read();
//     Serial.println(data);
//   }
// }




























void wifiTest()
{
  // wait for WiFi connection
  if ((wiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://192.168.41.1/sensor/test")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }
  delay(10000);
}