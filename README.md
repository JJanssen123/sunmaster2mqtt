# sunmaster2mqtt
Python script for reading Mastervolt Sunmaster solar inverter data and publish data as mqtt messages

To use this script you need a RS485 to TCP converter like <a target="_blank" href="https://nl.aliexpress.com/item/32514008468.html">this (ethernet)</a> or <a href="https://nl.aliexpress.com/item/4000133437266.html" target="_blank">this (wifi)</a>. Put the ip-address of this converter in settings.py.

Connect the RS485 output of the inverter to the TCP converter using a RJ45 connector, for instance a cut in half network cable. Connect wire 4 (568B-blue) to A and wire 3 (568B-green/white) to B. Do NOT use the Masterbus connection of the inverter. You can connect more than one inverter by looping them through. The script is confirmed to work for three inverters with thanks to Nico Viersen.

You will need the Eclipse Paho MQTT Python client library, use pip for installation: pip3 install paho-mqtt

The script returns the current running values of each connected inverter. Once per day it collects the last 30 daily production amounts. Alle values are sent as mqtt messages to your mqtt broker. In settings.py you can set the brokers address, the topic and some other mqtt stuff.

The script is meant to run every minute (or 5) as a cronjob e.g. * * * * * /usr/bin/python3 /home/pi/sunmaster2mqtt/sunmaster2mqtt.py > /home/pi/sunmaster2mqtt/cronlog.txt. Be careful running it every minute when you have more than one inverter; getting the 30 day production numbers takes about 40 seconds per inverter.

If you don't want to use mqtt, there's a <a target="_blank" href="https://github.com/kloknibor/MasterVoltXS">Home Assistant integration</a> by Robin Kolk based on this script.
