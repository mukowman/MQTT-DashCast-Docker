# MQTT-DashCast-Docker
A Dashcast docker controller using MQTT
Credit to madmod/dashcast-docker, used as a base for this docker.

This docker will subscribe to an MQTT topic and launch DashCast on the specified ChromeCast

## Discovery and control

Using MQTT you can control ChromeCast to launch DashCast using the following topic. `FRIENDLY_NAME` is the dispaly name used to configured for each Chromecast.

	chromecast/FRIENDLY_NAME/command/dashcast
  
Publish a json array with two elements (website url and force boolean) to
`chromecast/FRIENDLY_NAME/command/dashcast`, e.g. `{"url":"https://darksky.net/forecast/-33.8548,151.2165/ca12/en","force":false}`.
The 'force' boolean is used for some sites forbid loading using the default method. Use this option to force them to load.  Doing so makes DashCast loose control of the chromecast.

## How to use this image

```console
$ docker run --name DashCast --restart unless-stopped --net=host -e MQTT_SERVER="192.168.0.10" -e MQTT_USERNAME="user" -e MQTT_PASSWORD="password" -d mukowman/MQTT-DashCast-Docker
```
This will start a python based MQTT client listening on topic chromecast/+/command/dashcast.
Any messages received will start a DashCast session on the specified ChromeCast
