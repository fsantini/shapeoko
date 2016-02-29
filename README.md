shapeoko
========
Python utilities to communicate with the Shapeoko desktop CNC machine
and its GRBL controller.

bin/
----
shapeoko commandline utilities. run with --help option for more info.

- gcat: send a gcode file to the grbl controller
- gdraw: use keypresses to interactively move the shapeoko tool.
- gsh:  send gcode commands to the grbl controller
- gjoycat: jog the spindle using a joypad to set zero; then send a file (requires pygame)

lib/
----
- grblstuff.py: library for chatting with the grbl.
- getch.py: get a keypress
- GCodeAnalyzer.py: analyze gcode to get time, length, bounding box and stuff
- JoyStatus.py: manages the joypad

gcode_utils/
----
Various utilities to manage gcode

- gcode3dZopt.py: optimizes heekscad 3D gcode by avoiding to follow the 3D profile of the model, and replacing it with G0 moves
- gcodeAnalyze.py: executable wrapper for GCodeAnalyzer, returning bounding box and time
- gcodeconv.py: convert grbl-style gcode (without redundant G1/G0) produced by heekscad into more verbose and general gcode
- gcodeopt.py: inspired by gcodemillopt, optimizes MakerCam gcode by minimizing G0 moves
- gcodeupdownopt.py: removes useless up/down moves
- truncate.py: truncates MakerCam gcode. Modified from https://github.com/jhessig/metric-gcode-truncator

data/
----
sample gcode files (give these to gcat), including the shapeoko hello world.

