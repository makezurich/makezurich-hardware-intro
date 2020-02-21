# #MakeZurich hardware intro
Introducing some of the hardware available at [MakeZurich.ch](http://makezurich.ch/).

Found a bug or have a question? [Submit an issue](../../issues).

## Arduino Nano BLE Sense
The [Arduino Nano BLE Sense](https://store.arduino.cc/arduino-nano-33-ble-sense) is a microcontroller, a small computer that runs a single program.

The Nano uses *3.3V* logic. Here is the pinout, a map of all general purpose input/output (GPIO) pins:

<img src="https://live.staticflickr.com/65535/49558575858_893cb7d59e_b.jpg" width="512" style="border-color: coral; border-width: thin;" />

### Getting started with the Nano
Follow this guide to [get started with the Arduino Nano BLE Sense](https://www.arduino.cc/en/Guide/NANO33BLESense).

### Installing a library for the Nano
Follow these steps to [install an Arduino library](https://www.arduino.cc/en/Guide/Libraries).

### Measuring humidity and temperature with the Nano
The Arduino Nano BLE Sense has a humidity and temperature sensor, the [HTS221](https://www.st.com/resource/en/datasheet/HTS221.pdf).

To use it, install the [ArduinoHTS221 library](https://www.arduino.cc/en/Reference/ArduinoHTS221) and check the examples.

### Measuring barometric pressure with the Nano
The Arduino Nano BLE Sense has a barometric pressure sensor, the [LPS22HB](https://www.st.com/resource/en/datasheet/lps22hb.pdf).

To use it, install the [ArduinoLPS22HB library](https://www.arduino.cc/en/Reference/ArduinoLPS22HB) and check the examples.

### Measuring orientation in space of the Nano
The Arduino Nano BLE Sense has a 9-axis inertial measuring unit (IMU) built-in.

The [LSM9DS1](https://www.st.com/resource/en/datasheet/lsm9ds1.pdf) includes an accelerometer, a gyroscope and a magnetometer.

To use it, install the [ArduinoLSM9DS1 library](https://www.arduino.cc/en/Reference/ArduinoLSM9DS1) and check the examples.

### Measuring noise and recording audio with the Nano
The Arduino Nano BLE Sense has a built-in microphone, the [MP34DT05](https://www.st.com/resource/en/datasheet/mp34dt05-a.pdf) which outputs [PDM signals](https://en.wikipedia.org/wiki/Pulse-density_modulation).

To use it, install the [PDM library](https://www.arduino.cc/en/Reference/PDM) and the [ArduinoSound library](https://www.arduino.cc/en/Reference/ArduinoSound) and check the examples.

### Measuring gestures, color or proximity with the Nano
The Arduino Nano BLE Sense has a light intensity sensor, the [APDS9960](https://docs.broadcom.com/docs/AV02-4191EN).

The multifunctional sensor can detect gestures, light color and proximity.

To use it, install the [ArduinoAPDS9960 library](https://www.arduino.cc/en/Reference/ArduinoAPDS9960) and check the examples.

### Measuring air quality with the Sensirion ESS-C3 shield
The [Sensirion ESS-C3 shield](https://developer.sensirion.com/platforms/environmental-sensor-shield/) has environmental sensors to measure temperature, humidity, TVOC and CO2.

To connect the Sensirion shield to the Nano you need a hardware adapter, e.g. the [NanUno v2](https://www.thingiverse.com/thing:4171213).

To use the sensors, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the examples.

### Sending data to TheThingsNetwork with the Murata LoRaWAN module
TODO

### Sending data from the Nano with Bluetooth Low Energy (BLE)
TODO

## Arduino Uno
The [Arduino Uno](https://store.arduino.cc/arduino-uno-rev3) is a microcontroller.

The Uno uses *5V* logic, the pinout is printed right on the board:

<img src="https://store-cdn.arduino.cc/uni/catalog/product/cache/1/image/1040x660/604a3538c15e081937dbfbd20aa60aad/a/0/a000066_featured_3.jpg" width="512" />

### Getting started with the Uno
Follow the steps in [this tutorial](http://www.tamberg.org/chopen/2018/LoRaWANIoTWorkshop.pdf) (PDF, p.10 - p.41).

### Installing a library for the Uno
Follow these steps to [install an Arduino library](https://www.arduino.cc/en/Guide/Libraries).

### Measuring air quality with the Sensirion ESS-C3 shield
The [Sensirion ESS-C3 shield](https://developer.sensirion.com/platforms/environmental-sensor-shield/) has environmental sensors to measure temperature, humidity, TVOC and CO2.

To use it, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the examples.

### Sending data to TheThingsNetwork with the Dragino LoRaWAN shield
Follow the steps in [this tutorial](http://www.tamberg.org/chopen/2018/LoRaWANIoTWorkshop.pdf) (PDF, p.42 - p.63).
