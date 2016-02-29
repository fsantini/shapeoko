import pygame
import time
  
xDict = { 
  'axes' : [ 0, 3 ],
  'axesMult' : [ 50, 5 ],
  'hats' : [ (0,0) ],
  'hatsMult' : [ 1 ],
  'btns' : [],
  'btnsMult': []
}

yDict = {
  'axes' : [ 1, 2 ],
  'axesMult' : [ -50, -5 ],
  'hats' : [ (0,1) ],
  'hatsMult' : [ 1 ],
  'btns' : [],
  'btnsMult': []
}

zDict = {
  'axes' : [],
  'axesMult' : [],
  'hats' : [],
  'hatsMult' : [],
  'btns' : [ 4, 5, 6, 7 ],
  'btnsMult' : [ 1, -1, 0.1, -0.1]
}
  
class JoyStatus:
  def __init__(self):
    # Set up the joystick
    pygame.joystick.init()
    #print "Number of joysticks:", pygame.joystick.get_count()
    if pygame.joystick.get_count() == 0:
      print "No Joystick available"
      self.joystick = None
    else:
      self.joystick = pygame.joystick.Joystick(0)
      self.joystick.init()
      
  def getAxis(self, axis):
    if not self.joystick: return 0
    if axis < self.joystick.get_numaxes():
      return self.joystick.get_axis(axis)
    return 0
  
  def getHat(self, hat):
    if not self.joystick: return 0      
    if hat < self.joystick.get_numhats():
      return self.joystick.get_hat(hat)
    return 0
  
  def getButton(self, btn):
    if not self.joystick: return 0
    if btn < self.joystick.get_numbuttons():
      return self.joystick.get_button(btn)
    return 0
  
  def getMovement(self, axisDict):
    # check axes
    for joyAxisIndex in range(0,len(axisDict['axes'])):
      joyAxis = axisDict['axes'][joyAxisIndex]
      if self.getAxis(joyAxis) != 0:
        return self.getAxis(joyAxis)*axisDict['axesMult'][joyAxisIndex]
      
    # check hats
    for joyHatIndex in range(0,len(axisDict['hats'])):
      joyHat = axisDict['hats'][joyHatIndex]
      hatN = joyHat[0]
      hatVal = joyHat[1]
      value = self.getHat(hatN)[hatVal]
      if value != 0:
        return value*axisDict['hatsMult'][joyHatIndex]
      
    # check buttons
    for btnIndex in range(0,len(axisDict['btns'])):
      btn = axisDict['btns'][btnIndex]
      value = self.getButton(btn)
      if value != 0:
        return value*axisDict['btnsMult'][btnIndex]
    return 0

  def getXYZ(self):
    xMovement = self.getMovement(xDict)
    yMovement = self.getMovement(yDict)
    zMovement = self.getMovement(zDict)
    return (xMovement, yMovement, zMovement)
  
## main loop
if __name__ == '__main__':
  pygame.init()
  joy = JoyStatus()
  while (True):
    pygame.event.get()
    xyz = joy.getXYZ()
    if xyz != (0,0,0):
      print xyz
      
    time.sleep(0.1)
    
    
    
