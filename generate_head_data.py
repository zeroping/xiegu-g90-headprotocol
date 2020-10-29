#!/usr/bin/env python3

import sys
#import pickle
import serial
import time
#import datetime

import xiegug90head
#from construct import Int16ub, Int16ul, Int16bl, Struct
#from construct import *

import zlib
import binascii
import hashlib
import crccheck
import time

#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':0, 'checksum':0xdd33f76e}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':1, 'checksum':0x806ba4ae}
myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':2} #, 'checksum':0xd09e90ea}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':3, 'checksum':0x8dc6c32a}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':4, 'checksum':0x7074f962}
#myvals = {'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':5, 'checksum':0x2d2caaa2}

#won't work - wrong checksum
#all bytes seem to matter
#myvals = {'header': [0x55,0xaa], 'pad1': 0, 'pad2b':0x55, 'unknown2':2, 'ctrl3.tx_disable':False, 'volume':5, 'unknown5':[0xff, 0xff, 0x00, 0x00, 0x00, 0x00], 'checksum':0x2d2caaa2}


from struct import pack,unpack
def modswap(inbytes):
  out = bytearray()
  for sidx in range(len(inbytes)//4):
    tmp = bytearray(inbytes[sidx*4:(sidx*4)+4])
    tmp[0],tmp[1],tmp[2],tmp[3] = tmp[3],tmp[2],tmp[1],tmp[0]
    out += tmp
  return out


def makepacket(inputvals):
  mybytes  = xiegug90head.xiegug90head.build(inputvals)
  crcinst = crccheck.crc.Crc32Mpeg2()
  crcinst.process(modswap(mybytes)[:-4])
  print ("calculated CRC" + str(binascii.hexlify(modswap(crcinst.finalbytes()))))
  inputvals['checksum'] = int.from_bytes(crcinst.finalbytes(), "big")
  mybytes  = xiegug90head.xiegug90head.build(inputvals)
  return mybytes


mybytes = makepacket(myvals)

print("rb ",end="")
for idx in range(len(mybytes)):
  print("{:02x}".format(mybytes[idx]), end="")
print()

with serial.Serial(sys.argv[1], 115200, timeout=1) as ser:
  # turns the volume up and down to prove that the checksum works.
  for iteration in range(2):
    for vol in range(6):
      time.sleep(0.5)
      myvals['volume'] = vol
      print("volume " + str(vol))
      mybytes = makepacket(myvals)
      print("rb ",end="")
      for idx in range(len(mybytes)):
        print("{:02x}".format(mybytes[idx]), end="")
      print()
      ser.write(mybytes)
      
  
  
  time.sleep(0.5)
  myvals['volume'] = 0
  mybytes = makepacket(myvals)
  print("rb ",end="")
  for idx in range(len(mybytes)):
    print("{:02x}".format(mybytes[idx]), end="")
  print()
  ser.write(mybytes)
  
  if(False):
    #turns the base off unit the shutdown_req flag
    time.sleep(0.5)
    myvals['volume'] = 0
    myvals['ctrl2'] = {'shutdown_req':True, 'tuning':False }
    mybytes = makepacket(myvals)
    print("rb ",end="")
    for idx in range(len(mybytes)):
      print("{:02x}".format(mybytes[idx]), end="")
    print()
    ser.write(mybytes)



