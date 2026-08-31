#include <Arduino.h>

const int adcPin = 34;

// ==================================================
// SAMPLING CONFIGURATION
// ==================================================

const unsigned long samplePeriodUs = 2000;   // 2000 us = 500 Hz
unsigned long nextSampleTime;


// ==================================================
// SETUP
// ==================================================

void setup() {

  // Serial connection to MacBook / Python
  Serial.begin(460800);

  // ESP32 ADC resolution
  analogReadResolution(12);

  // Initialise sampling timer
  nextSampleTime = micros();
}


// ==================================================
// MAIN LOOP
// ==================================================

void loop() {

  unsigned long now = micros();

  // Take one sample every 2000 microseconds
  // 2000 us = 2 ms = 500 samples/second
  if ((long)(now - nextSampleTime) >= 0) {

    nextSampleTime += samplePeriodUs;

    // ----------------------------------------------
    // Read raw ADC value from GPIO34
    // ----------------------------------------------

    int raw = analogRead(adcPin);


    // ----------------------------------------------
    // Record timestamp
    // ----------------------------------------------

    unsigned long timestamp = micros();


    // ----------------------------------------------
    // Send CSV-formatted data
    //
    // Format:
    // timestamp_us,raw
    //
    // Example:
    // 20128902,1875
    // 20130901,1892
    // ----------------------------------------------

    Serial.print(timestamp);
    Serial.print(",");

    Serial.println(raw);
  }
}