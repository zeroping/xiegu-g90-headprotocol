#!/usr/bin/env python3

import sys
#import pickle
import serial
import time
#import datetime

import xiegug90head
#from construct import Int16ub, Int16ul, Int16bl, Struct
#from construct import *


#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':0, 'checksum':0xdd33f76e}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':1, 'checksum':0x806ba4ae}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':2, 'checksum':0xd09e90ea}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':3, 'checksum':0x8dc6c32a}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':4, 'checksum':0x7074f962}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':5, 'checksum':0x2d2caaa2}

#won't work - wrong checksum
#all bytes seem to matter
#myvals = {'header': [0x55,0xaa], 'pad1': 0, 'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':5, 'unknown5':[0xff, 0xff, 0x00, 0x00, 0x00, 0x00], 'checksum':0x2d2caaa2}



mybytes  = xiegug90head.xiegug90head.build(myvals)

print("rb ",end="")
for idx in range(len(mybytes)):
  print(" {:02x}".format(mybytes[idx]), end="")
print()

with serial.Serial(sys.argv[1], 115200, timeout=1) as ser:
  ser.write(mybytes)

