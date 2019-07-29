#include "RFHelper.h"

/* Definitions */
#define SENSOR_IN 2 // kase ADC2 ung pin pero PB4 sya


/* Initialization */
	/* Sine wave function */
	long t_start;
	double t;
	int value = 0;
	float f_sin = 1.0;  // 0.5 Hz - frequency of sine wave (for test)

/* Function Definitions */

void setup() { /* COM15 */
	// put your setup code here, to run once:
	rfInit(ecgNode);
}


void loop() {
	// put your main code here, to run repeatedly:
	network.update();

	// get delta time
	// t = (millis() - t_start) / 1000.0;
	// get new value
	// value = 512 * sin(2 * PI * f_sin * t) + 512;

	// get analogValue
	value = analogRead(SENSOR_IN);

	// build buffer
	sprintf(dataBuffer, "%d", ecgNode);
	dataBuffer[1] = ',';
	int last = sprintf(dataBuffer + 2, "%ld", millis());
	dataBuffer[last + 2] = ',';
	sprintf(dataBuffer + last + 3, "%d", value);

  // write to rf24 network
	RF24NetworkHeader header(rootNode);
	bool ok = network.write(header,&dataBuffer,DATA_SIZE);
}
