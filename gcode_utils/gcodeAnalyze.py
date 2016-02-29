#!/usr/bin/env python
import sys
import os
# path hack so we can import from sibling lib directory. 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lib.GCodeAnalyzer import GCodeAnalyzer
import fileinput

analyzer = GCodeAnalyzer()
for line in fileinput.input():
  analyzer.Analyze(line)
  #print line, analyzer.getPosition()

print "Bounding box:",analyzer.getBoundingBox()
print "Travel distance:", analyzer.getTravelLen()
print "Travel time:", analyzer.getTravelTime()