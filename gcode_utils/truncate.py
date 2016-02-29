#!/usr/bin/python
# inspired by https://github.com/jhessig/metric-gcode-truncator

import re
import fileinput

NDIGITS=4

def replaceFn(match):
  match = match.group(2)
  return "." + match[0:NDIGITS]

regex = re.compile(r"([.])([0-9]+)")
for line in fileinput.input():
  print re.sub(regex, replaceFn, line)
