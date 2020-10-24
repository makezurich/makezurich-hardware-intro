// http://tamberg.mit-license.org/

// for a safer #badgelife at https://makezurich.ch/ 2020
// based on https://steigerlegal.ch/2020/07/06/swisscovid-app-bluetooth
// and https://github.com/arduino-libraries/ArduinoBLE/blob/master/examples/Central/Scan/Scan.ino
// and https://github.com/adafruit/Adafruit_NeoPixel/blob/master/examples/strandtest/strandtest.ino

#include <ArduinoBLE.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 4
#define LED_COUNT 11
#define CORONA_APP_SERVICE_UUID "fd6f"

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int nOfCoronaApps = 0;

void setup() {
  Serial.begin(115200);
  //while (!Serial); // only, if USB connected

  strip.begin();
  strip.show(); // all off
  strip.setBrightness(50); // max 255

  if (!BLE.begin()) {
    Serial.println("BLE not ready, press reset!");
    while (1) {} // wait for reset
  }

  Serial.println("BLE central scanning for Corona apps ...");
  BLE.scanForUuid(CORONA_APP_SERVICE_UUID);
}

void loop() {
  BLEDevice peripheral = BLE.available();
  if (peripheral) {
    nOfCoronaApps++; // TODO: skip duplicates
    Serial.print("Discovered Corona app ");
    Serial.println(peripheral.address());
    int n = min(nOfCoronaApps, LED_COUNT);
    for (int i = 0; i < n; i++) {
        strip.setPixelColor(i, strip.Color(0, 255, 0));
    }
    for (int j = n; j < LED_COUNT; j++) {
        strip.setPixelColor(j, strip.Color(255, 0, 0));
    }
    strip.show();
  }
}
