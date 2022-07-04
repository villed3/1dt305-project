# 1DT305 Project

Project for course 1DT305 Applied IoT at Linnæus University. See [the project report](https://github.com/villed3/1dt305-project/tree/main/report) for more information about the project.

## Project Idea: Smart plant monitor

A connected device that measures soil moisture of a potted plant (indoors or outdoors) and its surroundings. The data is sent over LoRa or WiFi and analyzed in order to make assumptions of water consumption of a day with particular conditions. An API with weather data could be used to further analyze conditions. Could also be connected to an automatic watering system.

### Sensors

- Soil moisture sensor
- Rain intensity sensor
- DHT11 temperature and humidity sensor
- BMP180 barometer

Optional sensors:

- Rain sensor
- *LDR5528 photoresistor (not used here)*

### External code libraries used:

- [mqtt.simple](https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple)
- [BMP180](https://github.com/micropython-IMU/micropython-bmp180)
- [SSD1306](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py)

## MQTT-stack with Docker:

- [Mosquitto broker](https://mosquitto.org/) ([docker](https://hub.docker.com/_/eclipse-mosquitto))
- [Node-red](https://nodered.org/) ([docker](https://hub.docker.com/r/nodered/node-red))
- [InfluxDB](https://www.influxdata.com/) ([docker](https://hub.docker.com/_/influxdb))
- *[Grafana]

## Other tools

- https://nabucasa.github.io/esp-web-flasher/
- http://mqtt-explorer.com/