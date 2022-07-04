# Server stack

This project uses a combination of applications forming a complete server stack. The applications are deployed using [Docker](https://www.docker.com/) for simplicity. The applications used are:

- [Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) as MQTT broker
- [InfluxDB](https://hub.docker.com/_/influxdb) as database
- [Node-RED](https://hub.docker.com/r/nodered/node-red) as data fetcher and visualizer

## Usage

Download and install [Docker](https://www.docker.com/products/docker-desktop/).

Rename ``.env.example`` to ``.env`` and modify the InfluxDB admin password to your liking.

Start the stack from this directory with:

```bash
$ docker compose -p 1dt305-project up -d
```

Rename the ```mosquitto.passwd.example``` to ```mosquitto.passwd``` and change the user password of the helium user. Encrypt the passwords from within the mosquitto container with:

```bash
$ mosquitto_passwd -U mosquitto/passwd
```

Restart the container after encrypting the passwords.

Make sure to forward port ```8080``` to your host in your router to allow MQTT traffic to reach it.

A database and user for nodered is created by the script, but you may want to add a retention policy for the data. Enter the terminal for InfluxDB using:

```bash
$ docker exec -it 1dt305-influxdb influx
```

And create the policy with something like this:

```sql
> create retention policy thirtydays on nodered duration 30d replication 1 default
```

Measurements can be cleared in InfluxDB using:
```sql
> drop series from /.*/
```

Update the nodes in Node-RED that use Mosquitto and InfluxDB to use the correct password. Also update the Mosquitto password in the ```env.py``` file in the source code for the edge device.

## Remove

If you would like to remove all containers, do:

```bash
$ docker compose -p 1dt305-project down
```

## Additional resources

### Node-RED modules:
- [Dashboard](https://flows.nodered.org/node/node-red-dashboard)
- [InfluxDB](https://flows.nodered.org/node/node-red-contrib-influxdb)

