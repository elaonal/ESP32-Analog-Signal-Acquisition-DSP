#include <Arduino.h>

/// @brief 

const int adcPin = 34;

// ==================================================
// SAMPLING CONFIGURATION
// ==================================================

const unsigned long samplePeriodUs = 2000;   // 2000 us = 500 Hz
unsigned long nextSampleTime;


// ==================================================
// MOVING AVERAGE FILTER
// ==================================================

const int windowSize = 5;

int samples[windowSize] = {0};
int sampleIndex = 0;

long runningSum = 0;
int samplesCollected = 0;


// ==================================================
// IIR FILTER
// ==================================================

const float alpha = 0.3;

float iirValue = 0.0;
bool iirInitialised = false;


// ==================================================
// SETUP
// ==================================================

void setup() {

  Serial.begin(460800);

  // ESP32 ADC resolution
  analogReadResolution(12);

  nextSampleTime = micros();
}


// ==================================================
// MAIN LOOP
// ==================================================

void loop() {

  unsigned long now = micros();

  // Sample every 2000 microseconds = 500 Hz
  if ((long)(now - nextSampleTime) >= 0) {

    nextSampleTime += samplePeriodUs;


    // ==================================================
    // 1. RAW ADC ACQUISITION
    // ==================================================

    int raw = analogRead(adcPin);


    // ==================================================
    // 2. MOVING AVERAGE FILTER
    // ==================================================

    // Remove oldest sample from running sum
    runningSum -= samples[sampleIndex];

    // Store newest sample
    samples[sampleIndex] = raw;

    // Add newest sample
    runningSum += raw;

    // Move to next position
    sampleIndex++;

    if (sampleIndex >= windowSize) {
      sampleIndex = 0;
    }

    // Handle first few samples at startup
    if (samplesCollected < windowSize) {
      samplesCollected++;
    }

    float movingAverage =
        runningSum / (float)samplesCollected;


    // ==================================================
    // 3. IIR FILTER
    // ==================================================

    if (!iirInitialised) {

      // Initialise with first ADC value
      iirValue = raw;
      iirInitialised = true;

    } else {

      // y[n] = alpha*x[n] + (1-alpha)*y[n-1]

      iirValue =
          alpha * raw +
          (1.0 - alpha) * iirValue;
    }


    // ==================================================
    // 4. TIMESTAMP
    // ==================================================

    unsigned long timestamp = micros();


    // ==================================================
    // 5. CSV SERIAL OUTPUT
    // ==================================================
    //
    // Format:
    // timestamp_us,raw,moving_average,iir
    //

    Serial.print(timestamp);
    Serial.print(",");

    Serial.print(raw);
    Serial.print(",");

    Serial.print(movingAverage, 1);
    Serial.print(",");

    Serial.println(iirValue, 1);
  }
}