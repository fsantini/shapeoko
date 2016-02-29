#!/usr/bin/env python

import math
import fileinput
import re
import sys

def safeInt(val):
  try:
    return int(val)
  except:
    return 0
    
def safeFloat(val):
  try:
    return float(val)
  except:
    return 0

def logPrint(msg):
  sys.stderr.write(msg + "\n")
  

# find a code in a gstring line   
def findCode(gcode, codeStr):
  pattern = re.compile(codeStr + "\\s*(-?[\d.]*)",re.I)
  m=re.search(pattern, gcode)
  if m == None:
    return None
  else:
    return m.group(1)

def euclidean_distance( start, end ):
  return math.sqrt( sum( [ (e-s)**2 for (s,e) in zip(start, end) ] ) )


class GCodeSet:

    
    def __init__(self):
      self.lines = []
      self.start = [0,0]
      self.end = [0,0]
      self.cuttingZ = 0
      self.cuttingStarted = False
      self.safeZ = 0
      
    
    def setStart(self,start):
      self.start = list(start) # copy and not reference, as it is a list
    
    # returns true if the block ended
    def addLine(self, line):
      self.lines.append(line.strip())
      code_g = findCode(line, "G")
      
      # not a movement code: leave it alone
      if code_g == None or safeFloat(code_g) not in [0,1,2,3]:
        return False
      
      code_x = findCode(line, "X")
      code_y = findCode(line, "Y")
      
      code_g = safeInt(code_g)
      
      if not self.cuttingStarted:
        # if we haven't started cutting yet, update start point  
        if code_x != None:
          self.start[0] = safeFloat(code_x)
          self.end[0] = safeFloat(code_x)
        if code_y != None:
          self.start[1] = safeFloat(code_y)
          self.end[1] = safeFloat(code_x)
      else: # if the cutting started, update end
        if code_g != 0:
          if code_x != None:
            self.end[0] = safeFloat(code_x)
          if code_y != None:
            self.end[1] = safeFloat(code_y)
      
      # we start cutting: don't update start anymore
      if code_g != 0 and not self.cuttingStarted:
        #logPrint("Cutting started: we are at: %.3f, %.3f" % (self.start[0], self.start[1]))
        self.cuttingStarted = True
      
      if code_g == 1 and findCode(line, "Z") != None: # g2 and g3 cannot have a Z
        self.cuttingZ = safeFloat(findCode(line, "Z"))
        return False
      
      # remove all g0 except for G0 Z
      if code_g == 0:
        if findCode(line, "Z") != None:
          self.safeZ = safeFloat(findCode(line, "Z"))
          #logPrint("Found block end: %s" % line)
          return True
        
        # remove the last G0 code because it was just useless movement
        #logPrint("Removing G0 line: %s" % line)
        self.lines.pop()
      return False
        
      
    def printBlock(self):
      self.lines.insert(0, "G0 X%.4f Y%.4f" % (self.start[0], self.start[1]))
      self.lines.insert(0, "(new block)")
      gcode = "\n".join(self.lines)
      gcode += "\n"
      return gcode
    
    def getDistance(self, otherSet):
      return euclidean_distance(self.end, otherSet.start)
    
    
if __name__ == "__main__":
  gcodeSetList = []
  curGCodeSet = GCodeSet()
  
  preamble = []  
  epilogue = []
  
  isPreamble = True
  isEpilogue = False
  
  # read file and divide it into sets
  for line in fileinput.input():
    if line.find(";") >= 0:
      line = line[:line.find(";")] # remove comments
    if line.find("(") >= 0:
      line = line[:line.find("(")] # remove comments
    
    line = line.strip() 
    
    if isPreamble:
      code_g = findCode(line,"G")
      # he preamble can contain: 1) No G-Codes, 2) No G0-3 codes, 3) G0 Z moves, but not XY
      if code_g == None or safeInt(code_g) not in [0,1,2,3] or (findCode(line, "X") == None and findCode(line, "Y") == None):
        preamble.append(line)
        continue
      else:
        logPrint("preamble end")
        isPreamble = False
        
    # M5 and/or M30 end the gcode
    code_m = findCode(line,"M")
    if code_m != None:
      code_m = safeInt(code_m)
      if code_m in [5, 30]:
        isEpilogue = True
        
    if isEpilogue:
      epilogue.append(line)
      continue
        
    finishedSet = curGCodeSet.addLine(line)
    if finishedSet:
      gcodeSetList.append(curGCodeSet)
      newStart = curGCodeSet.end
      curGCodeSet = GCodeSet()
      curGCodeSet.setStart(newStart)
      
  # the file does not end with an up G0 code: add the last block anyway
  if not finishedSet:
    curGCodeSet.addLine("G0 Z%.4f" % gcodeSetList[-1].safeZ)
    gcodeSetList.append(curGCodeSet)
  
  logPrint("Number of sets: %d" % len(gcodeSetList))
  logPrint("Optimizing...")
  optimizedList = []
  optimizedList.append(gcodeSetList[0])
  gcodeSetList.pop(0)
  while len(gcodeSetList) > 0:
    curRefSet = optimizedList[-1]
    optSet = gcodeSetList[0]
    optSetIndex = 0
    distance = 1e6
    for curTestSetIndex in range(0,len(gcodeSetList)):
      curTestSet = gcodeSetList[curTestSetIndex]
      newDist = curRefSet.getDistance(curTestSet)
      if newDist < distance:
        distance = newDist
        optSet = curTestSet
        optSetIndex = curTestSetIndex
    optimizedList.append(optSet)
    gcodeSetList.pop(optSetIndex)
    
  logPrint("Opt list len: %d" % len(optimizedList))
  print "\n".join(preamble)
  for gcodeSet in optimizedList:
    #logPrint("block start: %.3f, %.3f" % (gcodeSet.start[0], gcodeSet.start[1]))
    #logPrint("N lines in block: %d" % len(gcodeSet.lines))
    print gcodeSet.printBlock()
  print "\n".join(epilogue)
  