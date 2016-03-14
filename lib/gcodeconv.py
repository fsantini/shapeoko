#!/usr/bin/env python

import fileinput
import re


class GCodeConverter:
  lastG = 'G0'
  lastX = 'X0'
  lastY = 'Y0'
  
  def __init__(self):
    pass
  
  def convert(self, line):
    line = line.strip()
    if line.startswith('G'):
      self.lastG = line.split(' ')[0] # get the GCode
      #is there an X?
      xre = re.search('X[0-9.-]+', line)
      xfound = False
      if xre is not None:
        self.lastX = xre.group(0)
        xfound = True
      yre = re.search('Y[0-9.-]+', line)
      yfound = False
      if yre is not None:
        self.lastY = yre.group(0)
        yfound = True
        
      # there can't be an X without Y
      if xfound and not yfound:
        line += ' ' + self.lastY
      elif yfound and not xfound:
        line += ' ' + self.lastX
  
      return line
    elif line.startswith('X') or line.startswith('Y') or line.startswith('Z'):
      #is there an X?
      xre = re.search('X[0-9.-]+', line)
      xfound = False
      if xre is not None:
        self.lastX = xre.group(0)
        xfound = True
      yre = re.search('Y[0-9.-]+', line)
      yfound = False
      if yre is not None:
        self.lastY = yre.group(0)
        yfound = True
        
      # there can't be an X without Y
      if xfound and not yfound:
        line += ' ' + self.lastY
      elif yfound and not xfound:
        line += ' ' + self.lastX
  
      return self.lastG + ' ' + line
    else:
      return line
  

if __name__ == "__main__":
  conv = GCodeConverter()
  for line in fileinput.input():
    print conv.convert(line)
  