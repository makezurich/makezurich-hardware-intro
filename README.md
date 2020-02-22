# #MakeZurich hardware intro
Introducing some of the hardware available at [MakeZurich.ch](http://makezurich.ch/).

Found a bug or have a question? [Submit an issue](../../issues).

## Arduino Nano BLE Sense
The [Arduino Nano BLE Sense](https://store.arduino.cc/arduino-nano-33-ble-sense) is a microcontroller, a small computer that runs a single program.

The Nano uses *3.3V* logic. Here is the pinout, a map of all general purpose input/output (GPIO) pins:

<img src="https://live.staticflickr.com/65535/49558575858_893cb7d59e_b.jpg" width="512" style="border-color: coral; border-width: thin;" />

### Installing the Arduino IDE
[Download the Arduino IDE](https://www.arduino.cc/en/Main/Software), we recommend the desktop version, which shows up as *Arduino* once installed.

The IDE (integrated development environment) is a simple tool to write, build and deploy programs.

### Getting started with the Nano
Follow this guide to [get started with the Arduino Nano BLE Sense](https://www.arduino.cc/en/Guide/NANO33BLESense#toc2).

Or just open *Tools > Board > Board Manager...* and add the *Arduino nRF528x Boards* package.

Then select *Tools > Board > Arduino NANO 33 BLE*, plug in the Nano via USB and select it in the *Tools > Port* menu.

Finally, open *File > Examples > Basics > Blink* and click the ⮕ *Upload* button. (Driver issues? Check the guide above.)

### Learning the Arduino language
The [Arduino language](https://www.arduino.cc/reference/en/) is very similar to C, libraries are written in C++.

This is *Blink*, the *Hello, World!* of embedded programming:
```
int ledPin = 13;

void setup() { // runs once
  pinMode(ledPin, OUTPUT);
}

void loop() { // runs forever
  digitalWrite(ledPin, HIGH); // turn the LED pin on
  delay(1000);                // wait for 1000ms = 1s
  digitalWrite(ledPin, LOW);  // turn the LED pin off
  delay(1000);                // wait again
}
```

### Installing a library for the Nano
Follow these steps to [install an Arduino library](https://www.arduino.cc/en/Guide/Libraries).

Or just open *Sketch > Include library > Manage libraries...* and type the library name.

Then check the *File > Examples > LIBRARY_NAME* menu in the Arduino IDE.

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

To connect the Sensirion shield to the Nano you can use the [TODO]() or a [NanUno v2](https://www.thingiverse.com/thing:4171213) hardware adapter.

To use the sensors, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the examples.

### Sending data to TheThingsNetwork with the Murata LoRaWAN board
The [Murata B-L072Z-LRWAN1 board](https://www.st.com/resource/en/data_brief/b-l072z-lrwan1.pdf) can be used as a modem to send data to [TheThingsNetwork](http://thethingsnetwork.org/) (TTN).

To connect the Murata board to the Nano you can use the [TODO]() hardware adapter.

### Sending data from the Nano with Bluetooth Low Energy (BLE)
The Arduino Nano BLE Sense has built-in Bluetooth Low Energy (BLE) connectivity.

This allows you to connect to the Nano from a phone, laptop or another BLE device.

To use it, follow [this tutorial](https://www.arduino.cc/en/Reference/ArduinoBLE) or install the [ArduinoBLE library](https://github.com/arduino-libraries/ArduinoBLE) and check the examples.

## Arduino Uno
The [Arduino Uno](https://store.arduino.cc/arduino-uno-rev3) is a microcontroller.

The Uno uses *5V* logic, the pinout is printed right on the board:

<img src="https://store-cdn.arduino.cc/uni/catalog/product/cache/1/image/1040x660/604a3538c15e081937dbfbd20aa60aad/a/0/a000066_featured_3.jpg" width="512" />

### Getting started with the Uno
Follow the steps in [this tutorial](http://www.tamberg.org/chopen/2018/LoRaWANIoTWorkshop.pdf) (PDF, p.10 - p.41).

Or just select *Tools > Board > Arduino/Genuino Uno*.

Then plug in the Uno via USB and select it in the *Tools > Port* menu.

Finally, open *File > Examples > Basics > Blink* and click the ⮕ *Upload* button.

### Installing a library for the Uno
Follow these steps to [install an Arduino library](https://www.arduino.cc/en/Guide/Libraries).

Then check the *File > Examples > LIBRARY_NAME* menu in the Arduino IDE.

### Measuring air quality with the Sensirion ESS-C3 shield
The [Sensirion ESS-C3 shield](https://developer.sensirion.com/platforms/environmental-sensor-shield/) has environmental sensors to measure temperature, humidity, TVOC and CO2.

To use it, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the examples.

### Sending data to TheThingsNetwork with the Dragino LoRaWAN shield
Follow the steps in [LoRaWAN IoT with Arduino Uno](http://www.tamberg.org/chopen/2018/LoRaWANIoTWorkshop.pdf) (PDF, p.42 - p.63).

## Electronics
The following electronic components are part of the MakeZurich kit.

### Breadboard
Available on [AliExpress](https://www.aliexpress.com/item/32690555189.html).

### Jumper wires
Available on [AliExpress](https://www.aliexpress.com/item/32825083543.html).

### Basic components
Available on [AliExpress](https://www.aliexpress.com/item/32830950459.html).

50x leds, 1x rgb led, 2x photoresistors, 1x thermistor, 5x diode rectifiers, 5x npn transistor, 1x IC 4N35, 1x IC 74HC595, 10x buttons, 2x buzzers (active and passive), 1x potentiometer, 10x 22pf c. caps, 10x 104 c. caps, 5x e. caps 10uf, 5x e caps 100uf, 100x resistors (5x of each: 10R, 100R, 220R, 330R, 1K, 2K, 5K, 10K, 100K, 1M, pin headers)

### Level shifter 3.3V to 5V
Available on [AliExpress](https://www.aliexpress.com/item/32690066582.html).

## License
This tutorial by [MakeZurich.ch](http://makezurich.ch/) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
