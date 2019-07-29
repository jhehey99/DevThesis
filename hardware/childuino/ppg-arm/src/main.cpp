#include "RFHelper.h"

/* Definitions */

/* Initialization */
  /* Sine wave function */
  long t_start;
  double t;
  int value = 0;
  float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)

/* Function Definitions */

void setup() { /* COM12 */
  // put your setup code here, to run once:
  Serial.begin(9600);
  rfInit(ppgArmNode);
}

void loop() {
  // put your main code here, to run repeatedly:
  network.update();

  // get delta time
  t = (millis() - t_start) / 1000.0;
  // get new value
  value = 512 * sin(2 * PI * f_sin * t) + 512;

  String valueStr(value);

  valueStr += " : PPG ARM";
  bool ok = networkWrite(rootNode, valueStr);
  // RF24NetworkHeader header(/*to node*/ rootNode);
  // bool ok = network.write(header,&value,sizeof(value));
  Serial.print(ok);
}
