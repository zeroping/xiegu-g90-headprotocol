#!/usr/bin/env python3

import sys
#import pickle
import serial
import time
#import datetime


def readPacket(ser, readtime=1):
  byte1 = ser.read(1)
  if(byte1 != bytes(b'\x55')):
    print("Not synced yet " + byte1.hex())
    return
  byte2 = ser.read(1)
  if(byte2 != bytes(b'\xaa')):
    print("Syncing... " + byte2.hex())
    return
  
  packetbytes = ser.read(94)
  packetbytes = bytes(b'\x55\xaa') + packetbytes
  return packetbytes


def printpacket(pktbytes):
  if pktbytes:
    for idx in range(len(pktbytes)):
      print("{:>3} ".format(idx), end="")
    print()
    for idx in range(len(pktbytes)):
      print(" {:02x} ".format(pktbytes[idx]), end="")
    print()
    print("Freq A: " + str(pktbytes[4] + (pktbytes[5]<<8) + (pktbytes[6]<<16) + (pktbytes[7]<<24)))
    print("Freq B: " + str(pktbytes[20] + (pktbytes[21]<<8) + (pktbytes[22]<<16) + (pktbytes[23]<<24)))
    print("Pre/ATT: " + str(pktbytes[8])) # none, pre, att
    print("Mode: " + str(pktbytes[9])) # lsb, USB, CW, CWR, NFM, AM
    print("AGC: " + str(pktbytes[10])) #  AGC--, AGC-S, AGC-F, AGC-A
    print("Filter low : " + str(100 + (pktbytes[13]*25)))
    print("Filter high: " + str(125 + (pktbytes[12]*25)))
    
    print("FFT gain: " + str(pktbytes[19])) #1=auto, 2-10 direct
    
    print("Panel lock: " + str(True if (pktbytes[36]&0x01) else False))
    print("Spit : " + str(True if (pktbytes[36]&0x02) else False))
    print("Output : " + str("headphones "if (pktbytes[36]&0x04) else "speaker"))
    print("Mic compression : " + str(True if (pktbytes[36]&0x08) else False))
    print("NB : " + str("on" if (pktbytes[36]&0x10) else "off"))
    print("Tuner enabled : " + str(True if (pktbytes[36]&0x20) else False))    
    print("V/M : " + str("VFO" if (pktbytes[36]&0x40) else "MEM"))
    
    print("CW QSK : " + str(True if (pktbytes[38]&0x01) else False))
    print("TX disable? : " + str(False if (pktbytes[38]&0x02) else True)) #from being out of band?
    print("CW disp: " + str(True if (pktbytes[38]&0x10) else False))
    
    print("RCLK Tune: " + str(((pktbytes[38] + (pktbytes[39]<<8) ) >> 5 ) -1000))
    
    print("Gain: " + str( (pktbytes[42] + ((pktbytes[43] & 0x03) <<8)) >> 3 ))
    
    print("Band stack: " + str("Full" if (pktbytes[43]&0x04) else "Ham"))
    print("Beep enable: " + str(True if (pktbytes[43]&0x08) else False))
    
    print("RF Power: " + str(pktbytes[44])) # 1-20
    
    print("NB level: " + str( ((pktbytes[46] & 0xF0) >> 4 )))
    print("NB width: " + str( (pktbytes[46] & 0x0F )))
    
    print("Volume: " + str(pktbytes[48])) # 0-28
    
    print("CW QSK time: " + str(pktbytes[51] * 100 )) #ns
    
    print("Mem CH: " + str(pktbytes[53])) #memory writes and clears don't appear to cross the bus though
    print("VFO : " + str("B" if (pktbytes[54]&0x01) else "A"))
    
    print("CW WPM: " + str(pktbytes[60]))
    print("CW M/L/R: " + str( ((pktbytes[61] & 0x03) ))) # man, autio-l, auti-r
    print("CW Mode : " + str("B" if (pktbytes[61]&0x04) else "A"))
    print("CW Ratio: " + str( 2 +  0.1 * (pktbytes[61] >>4 ) ))
    
    print("Aux in vol: " + str( (pktbytes[83] & 0x0F )))
    print("Aux out vol: " + str( (pktbytes[83] & 0xF0 ) >> 4))


def logFrom(ser):
  iteration = 0
  ser.timeout = 0.1

  try:
    while(1):
      

      rxPacket = readPacket(ser,100)
      if(rxPacket):
        print("Got a packet: ")
        printpacket(rxPacket)
        print()
      
        
  except KeyboardInterrupt:
    print("got interrupt, exiting")


with serial.Serial(sys.argv[1], 115200, timeout=1) as ser:
  logFrom(ser)
