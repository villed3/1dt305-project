# Smart Soil Monitor

**Vilgot Ledstam (vl222nf)**

![Setup](images/setup.jpg)

This is an IoT project with a soil monitor connected to a web dashboard, using several different environmental sensors to allow for estimates of water consumption of either a potted plant or an outdoor plant. It is connected to the Internet using WiFi, but could just as well have been connected using LoRa. This tutorial will describe how the project was carried out and how it can be replicated.

This project was done as part of the course "[1DT305 - Introduction to Applied IoT](https://lnu.se/en/course/introduction-to-applied-internet-of-things/distance-international-summer/)" at [Linnæus University](https://lnu.se/en/).

## Objective

Being able to track the water status of your plants would be very useful, would it not? It would be even more useful if you could see the typical rate of water consumption, and somehow determine in advance how much water your plants will consume based on weather forecasts. The next step would be to have an automatic or remotely controlled watering system.

I chose this project because it had been on my mind for a while because of my tendency to leave my apartment for longer periods as a student on distance. I generally tend to forget to water them even while being home, so even more reason.

Analyzing the measured data over long periods of time in combination with weather data (temperature, humidity, air pressure and rain intensity) could give a very accurate insight about your vegetation. It would not be limited to just house plants and gardening, it could also be applied for agriculture, forestry and general park management.

Of course there are already plenty of projects like this already in production, but this project shows how easily an individual could implement something like this for personal use.

## Material

The components used in this project are listed below. Their usage and where to buy them is also listed.

| Picture                                                        | Component                                           | Description                                                                                                                                                                                                                                                                                      | Can be bought from                                                                                                                                                                                                                                     |
| -------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ![Heltec WiFi LoRa 32 (V2)](images/heltec_wifi_lora_32_v2.png) | Heltec WiFi LoRa 32 (V2) (w. pins and antenna)      | Microcontroller with an [ESP32](https://en.wikipedia.org/wiki/ESP32) microprocessor.  Has a built-in 128x64 OLED display, a battery connector and a LoRa chip (with external antenna). Wireless capabilites include LoRa, WiFi, and Bluetooth (supports low energy). Requires soldering of pins. | [Amazon SE](https://www.amazon.se/gp/product/B08243JHMW/)                                                                                                                                                                                              |
| ![Breadboard](images/breadboard.jpg)                           | Breadbord (full-size)                               | Solderless breadboard with 840 connections and polarity indicators. A smaller sized board could suffice.                                                                                                                                                                                         | [Electrokit](https://www.electrokit.com/en/product/solderless-breadboard-840-tie-points-2/)                                                                                                                                                            |
| ![Jumper wires](images/wires.jpg)                              | Jumper wires                                        | Wires to connect sensor with MPU on the breadboard. Only male-male wires are required. Shorter length breadbord wires can also be used to reduce clutter.                                                                                                                                        | [AZ-Delivery](https://www.az-delivery.de/products/40-stk-jumper-wire-male-to-male-20-zentimeter)<br/>(40-pack, male-male),<br/>[AZ-Delivery](https://www.az-delivery.de/products/3er-set-40-stk-jumper-wire-m2m-f2m-f2f)<br/>(120-pack, various types) |
| ![Soil moisture sensor](images/soil.jpg)                       | Soil moisture sensor (w. comparator module)         | Capacitive soil moisture sensor with a comparator module. A threshold can be set with the potentiometer on the comparator to provide a digital output, high or low, if the threshold is met or not. The comparator module also outputs the analog value directly.                                | [Amazon SE](https://www.amazon.se/dp/B07V6SZYZW/)                                                                                                                                                                                                      |
| ![DHT11](images/dht11.jpg)                                     | DHT11 temperature and humidity sensor               | Temperature and humidity sensor with low precision, connected with GPIO. Only used for humidity in this project, since the barometer provides temperature measuring.                                                                                                                             | [Amazon SE](https://www.amazon.se/dp/B089W8DB5P/)                                                                                                                                                                                                      |
| ![BMP180 barometer](images/bmp180.jpg)                         | BMP180 barometer                                    | A high precision barometer, with I2C interface. Also measures temperature. The unit used in this project requires soldering.                                                                                                                                                                     | [Amazon SE](https://www.amazon.se/dp/B07D8S617X/)                                                                                                                                                                                                      |
| ![Rain sensor](images/rain.jpg)                                | (Optional)<br/>Rain sensor                          | Capacitive rain sensor, with identical comparator module as the soil moisture sensor. Only applicable for outdoor use, but still used in this project.                                                                                                                                           | [AZ-Delivery](https://www.az-delivery.de/products/regen-sensor-modul)                                                                                                                                                                                  |
| ![NPN transistor](images/npn.jpg)                              | (Optional)<br/>NPN transistor or equivalent CMOS circuit | Used as a digital switch for the power supply, to save power and extend the lifespan of the capacitive sensors when not in use. A CMOS inverter constructed from NMOS and PMOS transistors are used in this project instead, simply because that is what I had on hand.                                            | [Electrokit](https://www.electrokit.com/produkt/mpsa14-to-92-npn-30v-500ma/)                                                                                                                                                                           |

You will of course also need a USB-A to micro USB cable for programming and powering the Heltec board, but you probably already have one.

All sensors can be bought as a kit, the one I bought was from [AZ-Delivery](https://www.az-delivery.de/products/16-in-1-kit-zubehorset-fur-raspberry-pi-arduino-und-andere-mikrocontroller) (comes with additional sensors).

Any 3.7V battery with JST-PH connector could be used as power supply. Different capacity batteries can be bought from [Electrokit](https://www.electrokit.com/?s=lipo+3.7v&post_type=product)

I wanted to use a photoresistive sensor as well, to measure sunlight intensity, but the one I got from the kit was attached to a comparator module without analog output. I could have removed the resistor and used it separately, but I decided not to because I already had several sensors to deal with.

## Computer setup

### Code platform: MicroPython

It was recommended to use the [MicroPython](https://micropython.org/) as code platform, so I chose to use it for this project. MicroPython includes a modified subset of the Python standard library specifically tailored towards microprocessors. It is used with the Python language and allows for code to be run directly on the board without needing to compile, and has an interactive prompt that runs from the device.

The Heltec board needs to be flashed with the MicroPython firmware before any code can be uploaded. If you intend to use WiFi, you can use the latest official MicroPython binary for ESP32, downloaded from [here](https://micropython.org/download/esp32/). That page also has instructions on how to flash the device. LoRa is not included in this version because generic ESP32 devices do not have LoRa built in. If you want to use LoRa, you can use the [binary from PyCom](https://docs.pycom.io/updatefirmware/device/) instead, but other libraries may also differ from the official version.

If your operating system does not recognize the device, you can install the driver manually. It can be downloaded from [here](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers). Choose the latest version for your OS and run the installer unzipped from the download.

### IDE: Visual Studio Code

I chose to use [Visual Studio Code](https://code.visualstudio.com/) as IDE for the project since it is the one I am most familiar with and it has the [Pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr) extension available, which you need in order to upload code to the device and interact with it. I had some problem uploading code with Pymakr, so I switched to the [preview version](https://marketplace.visualstudio.com/items?itemName=pycom.pymakr-preview) of the extension which worked better. At one point I also tried to use [Atom IDE](https://atom.io/) with Pymakr extension, but I had worse problems there so I switched back.

You can download Visual Studio Code from [here](https://code.visualstudio.com/Download). In order to install the Pymakr plugin, open VS Code, click the "Extensions" icon in the side panel and search for "pymakr". I installed the preview version but the main might work as well.

![Install pymakr](images/code-pymakr.png)

When in the project folder, the project will show up in the Pymakr view. You will need to add the device to the project to be able to interact with it, by connecting it and clicking "ADD DEVICES" underneath the project.

![Add device](images/code-add.png)

If you have the correct driver installed it will show up as "Silicon Labs CP210x...". Simply select it and click "OK".

![Select device](images/code-select.png)

Hovering over the newly added device in the Pymakr view will reveal options for the device. First click the connect icon to connect to the device. Then you will be able to upload the code by clicking the upload icon.

![Upload code](images/code-upload.png)

After the upload has finished, run the new code by clicking the reset button on the physical board (labelled "RST") .

<!-- Once installed, you will find the Pymakr icon in the side panel, which reveals the Pymakr options. You create a project by clicking "Create Project" or the + sign next to "Projects".

![Select template](images/code-pymakr-proj.png)

After selecting a directory where the project shall be located, you will be prompted to enter a project name and select a template.

![Select template](images/code-projname.png)
![Select template](images/code-template.png)

Using the "empty" template will generate a ```boot.py``` and a ```main.py``` file, which you can see in the file view in the side panel. -->

## Putting everything together

## Cloud platform

## The code

## Transmitting data

My initial goal was to use LoRa for the communication because it is very practical if it is used outdoors, because it does not require much power and it has a wide reach. There are different established LoRa networks that are basically free to use, for example The Things Network and Helium. After trying to connect to both of these networks without success, I concluded that LoRa would not work for my project without buying my own LoRa gateway.

I decided to use WiFi instead, and connect the device to my home network. This is done 

## Presenting data

## Finalizing the design
