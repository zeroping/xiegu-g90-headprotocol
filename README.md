# xiego-g90-headprotocol
Work to reverse engineer the protocol for the Xiegu G90's head unit.

Discussion about this is curerntly taking place here:
https://xiegug90.groups.io/g/TechnicalAnalysis/


## DB-9 pinout
1 +8V
2 Serial1  - 3.3V 115200 8n1 - From head -  Burst of 96 bytes every 29.5 ms
3 Serial2  - 3.3V 115200 8n1 - To head - Burst every 81.3 ms
4 Power button - Idles at 3.3V, goes to when pressed. Shoots to 11V when off.
5 GND
6 phones1 - Signal Output to headhones - switched via a relay between the built-in speaker and headphone jack
7 phones2 - Near 0V
8 IN_R - 
9 IN_L - 


## Head to Base decoding/printing script
I have a pythom script, log_head.py, that decodes the messages from the detachable head to the unit base. It uses a 3.3V RS-232 adapter, with GND connected, and the head unit's serial output connected to RS-232's adapter's input.



