#!/usr/bin/env python
# optimizes a gcode file removing useless up-down Z-moves

import fileinput
import re

lastG = 'G0'
lastX = 'X0'
lastY = 'Y0'
lastZ = 'Z0'
wasZOnlyMove = False
uselessMove = False
TOL = 1
zfound = False
xfound = False
yfound = False

def isZMove():
  return zfound and not (xfound or yfound)

def isXYMove():
  return (xfound or yfound) and not zfound

def getVal(moveCode):
  return float(moveCode[1:])

def getDistance(move1, move2):
  return abs(getVal(move1) - getVal(move2))

for line in fileinput.input():
  line = line.strip()
  
  if line.startswith('G'):
    xre = re.search('X[0-9.-]+', line)
    xfound = False
    if xre is not None:
      lastX = xre.group(0)
      xfound = True
    yre = re.search('Y[0-9.-]+', line)
    yfound = False
    if yre is not None:
      lastY = yre.group(0)
      yfound = True
    zre = re.search('Z[0-9.-]+', line)
    zfound = False
    if zre is not None:
      lastZ = zre.group(0)
      zfound = True
    
    if uselessMove:
      if isZMove():
        # suppress this move if we know it's useless
        print '; a useless Z move was suppressed'
        print line # move anyway to target Z
      else:
        # it's not a z move: print everything that happened before
        print lastZCommand
        print lastXYCommand
        print line
      uselessMove = False
      wasZOnlyMove = False
      continue
    
    # the previous one was a z-only move and was suspended
    if wasZOnlyMove:
      wasZOnlyMove = False
      # the previous move was z-only. This should be a XY move. Did it move?
      if isXYMove() and getDistance(lastX, prevX) < TOL and getDistance(lastY, prevY) < TOL:
        # it moved very little in XY: if the next one is a Z move then don't run what happened before.
        uselessMove = True
        lastXYCommand = line
      else:
        # the previous Z move is not useless: print the previous, this and next line
        uselessMove = False
        print lastZCommand
        print line
      continue
    
    uselessMove = False
    if isZMove():
      wasZOnlyMove = True
      lastZCommand = line
      prevX = lastX
      prevY = lastY
    else:
      wasZOnlyMove = False
      print line
  else: # not a G-Line
    print line