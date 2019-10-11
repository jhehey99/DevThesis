
#include "RFHelper.h"

/* Definitions */
#define SENSOR_IN 2 // kase ADC2 ung pin pero PB4 sya


/* Initialization */
/* Sine wave function */
long t_start;
double t;
int value = 0;
float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)
bool toggle = true;

enum ParameterMode {
  BloodPressure,
  OxygenSaturation
};

ParameterMode mode;

/* Function Definitions */
void setup() { /* COM12 */
  // put your setup code here, to run once:
  rfInit(ppgArmNode);
  pinMode(PB3, OUTPUT);
}

int count = 0;
int max = 500;

void loop() {
  // put your main code here, to run repeatedly:
  network.update();

  // get analogValue
  value = analogRead(SENSOR_IN);

  if(count > max) {
    toggle = !toggle;
    count = 0;
    // toggle the state of LEDs then add delay when toggling
    digitalWrite(PB3, !toggle);
    delay(200);
  }

  // digitalWrite(PB3, !toggle);

  if(toggle) {
    sprintf(dataBuffer, "%d", ppgArmNode);
  } else {
    sprintf(dataBuffer, "%d", ppgArmNodeRed);
  }

  dataBuffer[1] = ',';
  int last = sprintf(dataBuffer + 2, "%ld", millis());
  dataBuffer[last + 2] = ',';
  sprintf(dataBuffer + last + 3, "%d", value);

  // write to rf24 network
  RF24NetworkHeader header(rootNode);
  bool ok = network.write(header, &dataBuffer, DATA_SIZE);
  count ++;
}
