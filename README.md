# #MakeZurich hardware intro
Introduction to some of the hardware available at [#MakeZurich](http://makezurich.ch/).

Found a bug or have a question? [Submit an issue](../../issues).

See also: [#MakeZurich software intro](https://github.com/make-zurich/makezurich-software-intro).

## Arduino Nano 33 BLE Sense
The [Arduino Nano 33 BLE Sense](https://store.arduino.cc/arduino-nano-33-ble-sense) is a microcontroller, a small computer that runs a single program.

The Nano uses *3.3V* logic. Here is the pinout, a map of all general purpose input/output (GPIO) pins:

<img src="https://live.staticflickr.com/65535/49558575858_893cb7d59e_b.jpg" width="512" style="border-color: coral; border-width: thin;" />

### Installing the Arduino IDE
[Download the Arduino IDE](https://www.arduino.cc/en/Main/Software), we recommend the desktop version, which shows up as *Arduino* once installed.

The IDE (integrated development environment) is a simple tool to write, build and deploy programs.

### Getting started with the Nano
Follow this guide to [get started with the Arduino Nano 33 BLE Sense](https://www.arduino.cc/en/Guide/NANO33BLESense#toc2).

Or just open *Tools > Board > Board Manager...* and add the *Arduino nRF528x Boards* package.

Then select *Tools > Board > Arduino NANO 33 BLE*, plug in the Nano via USB and select it in the *Tools > Port* menu.

Finally, open *File > Examples > Basics > Blink* and click the ⮕ *Upload* button. (Driver issues? Check the guide above.)

### Learning the Arduino language
The [Arduino language](https://www.arduino.cc/reference/en/) is very similar to C, libraries are written in C++.

This is *Blink*, the *Hello, World!* of embedded programming:
```
int ledPin = 13;

void setup() { // runs once
  pinMode(ledPin, OUTPUT); // set up the LED pin
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
The Arduino Nano 33 BLE Sense has a humidity and temperature sensor, the [HTS221](https://www.st.com/resource/en/datasheet/HTS221.pdf).

To use it, install the [ArduinoHTS221 library](https://www.arduino.cc/en/Reference/ArduinoHTS221) and check the [examples](https://github.com/arduino-libraries/Arduino_HTS221/blob/master/examples).

### Measuring barometric pressure with the Nano
The Arduino Nano 33 BLE Sense has a barometric pressure sensor, the [LPS22HB](https://www.st.com/resource/en/datasheet/lps22hb.pdf).

To use it, install the [ArduinoLPS22HB library](https://www.arduino.cc/en/Reference/ArduinoLPS22HB) and check the [examples](https://github.com/arduino-libraries/ArduinoLPS22HB/blob/master/examples).

### Measuring orientation in space of the Nano
The Arduino Nano 33 BLE Sense has a 9-axis inertial measuring unit (IMU) built-in.

The [LSM9DS1](https://www.st.com/resource/en/datasheet/lsm9ds1.pdf) includes an accelerometer, a gyroscope and a magnetometer.

To use it, install the [ArduinoLSM9DS1 library](https://www.arduino.cc/en/Reference/ArduinoLSM9DS1) and check the [examples](https://github.com/arduino-libraries/ArduinoLSM9DS1/blob/master/examples).

### Measuring noise and recording audio with the Nano
The Arduino Nano 33 BLE Sense has a built-in microphone, the [MP34DT05](https://www.st.com/resource/en/datasheet/mp34dt05-a.pdf) which outputs [PDM signals](https://en.wikipedia.org/wiki/Pulse-density_modulation).

To use it, install the [PDM library](https://www.arduino.cc/en/Reference/PDM) and the [ArduinoSound library](https://www.arduino.cc/en/Reference/ArduinoSound) and check the [examples](https://github.com/arduino-libraries/ArduinoSound/blob/master/examples).

### Measuring gestures, color or proximity with the Nano
The Arduino Nano 33 BLE Sense has a light intensity sensor, the [APDS9960](https://docs.broadcom.com/docs/AV02-4191EN).

The multifunctional sensor can detect gestures, light color and proximity.

To use it, install the [ArduinoAPDS9960 library](https://www.arduino.cc/en/Reference/ArduinoAPDS9960) and check the [examples](https://github.com/arduino-libraries/ArduinoAPDS9960/blob/master/examples).

### Measuring TVOC and CO2 with the Sensirion ESS-C3 shield
The [Sensirion ESS-C3 shield](https://developer.sensirion.com/platforms/environmental-sensor-shield/) has environmental sensors to measure temperature, humidity, TVOC and CO2.

To connect it ([schematic](https://github.com/winkj/ess-hardware-docs/blob/master/ESS_Schematic.PDF)) to the Nano you can use the [TODO]() or a [NanUno v3](https://www.thingiverse.com/thing:4196198) hardware adapter.

To use the sensors, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the [examples](https://github.com/Sensirion/arduino-ess/blob/master/examples).

<img src="https://live.staticflickr.com/65535/49607643343_59944102a7_n.jpg" width="240"/>

### Measuring particulate matter with the Sensirion SPS30 sensor
The [Sensirion SPS30 sensor](https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25/) allows measuring particulate matter up to 2.5 micron (PM2.5).

To use the sensor, install the [Sensirion SPS30 I2C library](https://github.com/Sensirion/arduino-sps) and check the [examples](https://github.com/Sensirion/arduino-sps/tree/master/examples/sps30).

### Sending data from the Nano with Bluetooth Low Energy (BLE)
The Arduino Nano 33 BLE Sense has built-in Bluetooth Low Energy (BLE) connectivity.

This allows you to connect to the Nano from a phone, laptop or another BLE device.

To use it, follow [this tutorial](https://www.arduino.cc/en/Reference/ArduinoBLE) or install the [ArduinoBLE library](https://github.com/arduino-libraries/ArduinoBLE) and check the [examples](https://github.com/arduino-libraries/ArduinoBLE/blob/master/examples).

### Sending data to TheThingsNetwork with the Murata LoRaWAN board
The [Murata B-L072Z-LRWAN1 board](https://www.st.com/resource/en/data_brief/b-l072z-lrwan1.pdf) can be used as a modem to send data to [TheThingsNetwork](http://thethingsnetwork.org/) (TTN).

To connect the Murata board to the Nano you can use the [TODO]() hardware adapter.

To get your data from TTN, see [#MakeZurich software intro](https://github.com/make-zurich/makezurich-software-intro).

### More Nano BLE 33 Sense resources
* Dale Giancono has a nice [collection of Nano BLE 33 Sense examples](https://dalegi.com/).
* And there are quite some [Nano BLE 33 Sense projects on Hackster.io](https://www.hackster.io/search?q=Nano%20BLE%2033%20Sense&i=projects).

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

To use it, install the [Sensirion ESS library](https://github.com/Sensirion/arduino-ess) and check the [examples](https://github.com/Sensirion/arduino-ess/blob/master/examples).

<img src="https://live.staticflickr.com/65535/49573769808_691fbd261f_n.jpg" width="240"/>

### Sending data to TheThingsNetwork with the Dragino LoRaWAN shield
Follow the steps in [LoRaWAN IoT with Arduino Uno](http://www.tamberg.org/chopen/2018/LoRaWANIoTWorkshop.pdf) (PDF, p.42 - p.63).

## LoRaWAN Gateway
The included gateway is a [Tabs Hub](https://miromico.ch/wp-content/uploads/2019/11/Tabs_Hub.pdf) that works with [TheThingsNetwork](https://thethingsnetwork.org/).

## Electronics
The following electronic components are part of the MakeZurich kit.

As a simple rule, before connecting anything, unplug the power / USB cable.

### Breadboard
A [breadboard](https://www.aliexpress.com/item/32690555189.html) allows you to prototype electronic circuits.

Its holes are connected under the hood in columns, plus two rows for ground (GND, black or blue) and power (VCC, red).

### Jumper wires
[Jumper wires](https://www.aliexpress.com/item/32825083543.html) allow you to connect the Arduino to additional modules and components on a breadboard.

### Basic components
[Basic components](https://www.aliexpress.com/item/32830950459.html) like LEDs, resistors and buttons allow you to add input and output capabilities to your Arduino.

50x leds, 1x rgb led, 2x photoresistors, 1x thermistor, 5x diode rectifiers, 5x npn transistor, 1x IC 4N35, 1x IC 74HC595, 10x buttons, 2x buzzers (active and passive), 1x potentiometer, 10x 22pf c. caps, 10x 104 c. caps, 5x e. caps 10uf, 5x e caps 100uf, 100x resistors (5x of each: 10R, 100R, 220R, 330R, 1K, 2K, 5K, 10K, 100K, 1M, pin headers).

### Level shifter 3.3 to 5V
[Level shifters](https://www.aliexpress.com/item/32690066582.html) are required to connect 3.3V modules to an Arduino Uno which uses 5V logic.

### Soldering
[Soldering is easy](https://mightyohm.com/files/soldercomic/FullSolderComic_EN.pdf), there are soldering stations and helping hands at the Bitwäscherei space.

### PCB etching
Etching PCBs is possible at the Bitwäscherei space, try any Tuesday from 8pm.

## Support
#MakeZurich on the [TTN Switzerland Slack](ttn-ch.slack.com)

## License
This tutorial by [MakeZurich.ch](http://makezurich.ch/) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
