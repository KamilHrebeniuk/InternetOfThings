System simulates 8 light bulbs, which are steered with admin panel. Bulbs could be turned on and off, change communication protocol and change power levels.

Default run configuration for device5005.py:
MQTT 0 4 5005 "Conference right" Power2

Where
1. Protocol
2. Minimal delay between signals
3. Maximal delay between signals
4. Port for admin connection
5. Name
6. MQTT topic


Register new connection in admin panel by typing devices port and then pressing "Register!"
In admin panel you can turn on and off devices, switch between communication protocols with devices adapter HTTP/MQTT (MQTT is default) and change devices power. You can see communicates at console on left and see visualization below. Also, admin panel asks each device for status every 5 seconds.

Default run configuration for adapter.py:
MQTT
HTTP 10

Where
1. Protocol
2. Length od queue to compare (HTTP only)

Adapter receives communications from devices and calculates average voltage and power. On MQTT it counts from the first connection, on HTTP it counts last X requests. Where X is second run parameter.