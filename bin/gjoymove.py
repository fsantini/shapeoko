#!/usr/bin/env python 
#
# gdraw: simple interactive drawing program maps keypresses to gcodes
# and sends them to grbl on an arduino via a usb serial connection on
# OSX.
#

# config:

SERIAL_PATH='/dev/ttyACM*'
STD_FEED=2000
STD_FEED_Z=1000


import sys
import os.path
import pygame
# path hack so we can import from sibling lib directory. 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.realpath(__file__)))))
from lib.grblstuff import setup_logging, hello_grbl, do_command
from lib.JoyStatus import JoyStatus
import time

#debug:

#def do_command(grbl, cmd, wait=False):
  #print cmd
  #time.sleep(0.1)

#def hello_grbl(pattern=None, conf=None):
  #return True

def joyjog(grbl):  
  do_command(grbl, "G21") # set mm
  do_command(grbl, "G91") # incremental step mode
  pygame.init()
  joy = JoyStatus()
  
  returnStatus = False
  lastCommandWasZero = False
  myXYZ = [0,0,0]
  
  while (True):
    pygame.event.get()
    xyz = joy.getXYZ()
    if xyz != (0,0,0):
      lastCommandWasZero = False
      # go slower in Z moves
      if xyz[2] != 0:
	feed = STD_FEED_Z
      else:
	feed = STD_FEED
      # run command and wait for it to finish
      cmd = "G01 X%.3f Y%.3f Z%.3f F%d" % (xyz[0], xyz[1], xyz[2], feed)
      myXYZ[0] += xyz[0]
      myXYZ[1] += xyz[1]
      myXYZ[2] += xyz[2]
      sys.stdout.write("\rX: %.3f, Y: %.3f, Z: %.3f           " % (myXYZ[0],myXYZ[1],myXYZ[2]))
      sys.stdout.flush()
      
      #print cmd
      do_command(grbl, cmd, True) 
      
    if joy.getButton(0) and not lastCommandWasZero:
      lastCommandWasZero = True
      print "\rSetting zero                          "
      myXYZ = [0,0,0]
      sys.stdout.write("\rX: %.3f, Y: %.3f, Z: %.3f           " % (myXYZ[0],myXYZ[1],myXYZ[2]))
      sys.stdout.flush()
      do_command(grbl, "G92 X0 Y0 Z0") #set home with button 0
      
    if joy.getButton(3):
      lastCommandWasZero = False
      print "\rGoing home                            "
      myXYZ = [0,0,0]
      sys.stdout.write("\rX: %.3f, Y: %.3f, Z: %.3f           " % (myXYZ[0],myXYZ[1],myXYZ[2]))
      sys.stdout.flush()
      do_command(grbl, "G90")
      do_command(grbl, "G00 X0 Y0 Z0", True) # go to home
      do_command(grbl, "G91")
      
    if joy.getButton(8):
      returnStatus = True
      break
    
    if joy.getButton(9):
      returnStatus = False
      break

  do_command(grbl, "G90") # absolute positioning
  print ""
  return returnStatus
  
def main():
  grbl = hello_grbl(SERIAL_PATH)
  if not grbl:
    sys.exit(0)
  
  print "Use joystick to move; Button 1 sets home; Button 4 goes to home; Button 9 exits"
  joyjog(grbl)
  
  grbl.close()

if __name__ == "__main__":
    sys.exit(main())