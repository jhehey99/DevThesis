#include "RFHelper.h"

/* Definitions */

/* Initialization */
  /* Sine wave function */
  long t_start;
  double t;
  int value = 0;
  float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)

  /* Data */
  String to_send;
  uint8_t count = 0;
  uint8_t size = 2;
  bool refresh = false;

  /* Update Interval */
  uint8_t interval = 15; // ms
  unsigned long t_prev;
  unsigned long t_cur;


/* Function Definitions */

void readValue() {
  // get running time
  t = (millis() - t_start) / 1000.0;

  // get new value
  value = 512 * sin(2 * PI * f_sin * t) + 512;
}

void formatValue() {
  // recreate to_send string
  if(refresh) { 
    to_send = String(ecgNode);
  }

  // add to_send time and value
  to_send += ',' + String(millis()) + ',' + String(value);
}

void send() {
  Serial.println(to_send);
  bool ok = networkWrite(rootNode, to_send);
}

/* Update is called every time interval */
void update() {
  readValue();
  formatValue();
  if (count >= size - 1) {
    refresh = true;
    count = 0;
    send();
  } else {
    count ++;
    refresh = false;
  }
}

void setup() { /* COM6 */
  Serial.begin(9600);
  rfInit(ecgNode);
}

void loop() {
  // get current time
  t_cur = millis();

  // update rf network
  network.update();

  // check if time interval passed
  if (t_cur - t_prev >= interval) {
    t_prev = t_cur;
    update();
  }
}
