# Smart Soil Monitor

**Vilgot Ledstam (vl222nf)**

![Setup](images/setup.jpg)

This is an IoT project with a soil monitor connected to a web dashboard, using several different sensors to allow for estimates of water consumption of either a potted plant or an outdoor plant. It is connected to the Internet using WiFi, but could just as well have been connected using LoRa. This tutorial will describe how the project was carried out and how it can be replicated.

This project was done as part of the course "[1DT305 - Introduction to Applied IoT](https://lnu.se/en/course/introduction-to-applied-internet-of-things/distance-international-summer/)" at [Linnæus University](https://lnu.se/en/).

## Objective

Being able to track the water status of your plants would be very useful, would it not? It would be even more useful if you could see the typical rate of water consumption, and somehow determine in advance how much water your plants will consume based on weather forecasts. The next step would be to have an automatic or remotely controlled watering system.

I chose this project because it had been on my mind for a while because of my tendency to leave my apartment for longer periods as a student on distance. I generally tend to forget to water them even while being home, so even more reason.

Analyzing the measured data over long periods of time in combination with weather data could give a very accurate insight about your vegetation. It would not be limited to just house plants and gardening, it could also be applied for agriculture, forestry and general park management.

Of course there are already plenty of projects like this already in production, but this project shows how easily an individual could implement something like this for personal use.

## Material

The components used in this project are listed below. Their usage and where to buy them is also listed.

| Picture                                                        | Component                                           | Description                                                                                                                                                                                                                                                                                      | Can be bought from                                                                                                                                                                                                                             |
| -------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Heltec WiFi LoRa 32 (V2)](images/heltec_wifi_lora_32_v2.png) | Heltec WiFi LoRa 32 (V2) (w. pins and antenna)      | Microcontroller with an [ESP32](https://en.wikipedia.org/wiki/ESP32) microprocessor.  Has a built-in 128x64 OLED display, a battery connector and a LoRa chip (with external antenna). Wireless capabilites include LoRa, WiFi, and Bluetooth (supports low energy). Requires soldering of pins. | [Amazon SE](https://www.amazon.se/gp/product/B08243JHMW/)                                                                                                                                                          |
| ![Breadboard](images/breadboard.jpg)                           | Breadbord (full-size)                               | Solderless breadboard with 840 connections and polarity indicators. A smaller sized board could suffice.                                                                                                                                                                                         | [Electrokit](https://www.electrokit.com/en/product/solderless-breadboard-840-tie-points-2/)                                                                                                                                                    |
| ![Jumper wires](images/wires.jpg)                              | Jumper wires                                        | Wires to connect sensor with MPU on the breadboard. Only male-male wires are required. Shorter length breadbord wires can also be used to reduce clutter.                                                                                                                                        | [AZ-Delivery](https://www.az-delivery.de/products/40-stk-jumper-wire-male-to-male-20-zentimeter) (40-pack, male-male),<br/>[AZ-Delivery](https://www.az-delivery.de/products/3er-set-40-stk-jumper-wire-m2m-f2m-f2f) (120-pack, various types) |
| ![Soil moisture sensor](images/soil.jpg)                       | Soil moisture sensor (w. comparator module)         | Capacitive soil moisture sensor with a comparator module. A threshold can be set with the potentiometer on the comparator to provide a digital output, high or low, if the threshold is met or not. The comparator module also outputs the analog value directly.                                | [Amazon SE](https://www.amazon.se/dp/B07V6SZYZW/)                                                                                                                                                                                              |
| ![DHT11](images/dht11.jpg)                                     | DHT11 temperature and humidity sensor               | Temperature and humidity sensor with low precision, connected with GPIO. Only used for humidity in this project, since the barometer provides temperature measuring.                                                                                                                             | [Amazon SE](https://www.amazon.se/dp/B089W8DB5P/)                                                                                                                                                                                              |
| ![BMP180 barometer](images/bmp180.jpg)                         | BMP180 barometer                                    | A high precision barometer, with I2C interface. Also measures temperature. The unit used in this project requires soldering.                                                                                                                                                                     | [Amazon SE](https://www.amazon.se/dp/B07D8S617X/)                                                                                                                                                                                              |
| ![Rain sensor](images/rain.jpg)                                | (Optional)<br/>Rain sensor                          | Capacitive rain sensor, with identical comparator module as the soil moisture sensor. Only applicable for outdoor use, but still used in this project.                                                                                                                                           | [AZ-Delivery](https://www.az-delivery.de/products/regen-sensor-modul)                                                                                                                                                                          |
| ![NPN transistor](images/npn.jpg)                              | (Optional)NPN transistor or equivalent CMOS circuit | Used as a digital switch for the power supply, to save power and extend the lifespan of the capacitive sensors when not in use. A CMOS inverter constructed from NMOS and PMOS transistors are used in this project because I had some laying around.                                            | [Electrokit](https://www.electrokit.com/produkt/mpsa14-to-92-npn-30v-500ma/)                                                                                                                                                                   |

All sensors can be bought as a kit from [AZ-Delivery](https://www.az-delivery.de/products/16-in-1-kit-zubehorset-fur-raspberry-pi-arduino-und-andere-mikrocontroller) (comes with additional sensors).

Any 3.7V battery with JST-PH connector could be used as power supply. Different capacity batteries can be bought from [Electrokit](https://www.electrokit.com/?s=lipo+3.7v&post_type=product)

## Computer setup

## Putting everything together

## The code

## Transmitting data

## Presenting data

## Finalizing the design
