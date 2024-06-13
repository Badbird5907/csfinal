from Processing3 import *
from util.debugger import drawControl, drawTextTitle
from util.raycast import rayIntersectsRay, extrapolateRay, lineSegIntersectsLineSeg
from util.key import isKeyTyped

def initRCDbg():
  global rcDbgLines, rcDbgCurrent, rc_extrapolate
  rcDbgLines = []
  rcDbgCurrent = None
  rc_extrapolate = False
  return
def drawRCDbg():
  global rcDbgLines, rc_extrapolate
  stroke(255,0,0)
  for l in rcDbgLines:
    line(l[0][0], l[0][1], l[1][0], l[1][1])
    
  # draw intersections
  for l in rcDbgLines:
    for l2 in rcDbgLines:
      if (l == l2):
        continue
      if rc_extrapolate:
        ray = extrapolateRay(l, 1000)
        inter = lineSegIntersectsLineSeg(ray, l2)
      else:
        inter = lineSegIntersectsLineSeg(l, l2)
      if (not inter == None):
        fill(0,255,0)
        actual_inter = inter[0]
        ellipse(actual_inter[0], actual_inter[1], 5, 5)
        if (rc_extrapolate):
          stroke(0,255,0)
          # draw a line from the ray to the intersection point for clarity
          x1 = inter[1]
          y1 = inter[2]
          x = inter[3]
          y = inter[4]
          line(x1, y1, x, y)
  fill(255,0,0)
  stroke(255,0,0)
  if (not rcDbgCurrent == None):
    
    ellipse(rcDbgCurrent[0], rcDbgCurrent[1], 5, 5)
    line(rcDbgCurrent[0], rcDbgCurrent[1], mouseX, mouseY)

  if (isKeyTyped("u")):
    rcDbgLines = []
  if (isKeyTyped("t")):
    rc_extrapolate = not rc_extrapolate
  return

def rayCastDbgMouseClicked():
  global rcDbgLines, rcDbgCurrent, enableRayCastDebugger
  if (not enableRayCastDebugger):
    return
  if (mouseButton == LEFT):
    if (rcDbgCurrent == None):
      rcDbgCurrent = [mouseX, mouseY]
    else:
      rcDbgLines.append([rcDbgCurrent, [mouseX, mouseY]])
      rcDbgCurrent = None
  return

def rcdbg_drawDebuggerControls():
  global rc_extrapolate
  controls = [
    ("r", "Toggle ray cast debugger (ON)", True),
    ("u", "Delete everything", False),
    ("t", "Toggle ray extrapolation (" + ("ON" if rc_extrapolate else "OFF") + ")", rc_extrapolate)
  ]
  i = 0
  for control in controls:
    rgb = control[3] if len(control) > 3 else None
    drawControl(control[0], control[1], i, control[2], 0, rgb)
    i += 1
  drawTextTitle("Raycast Debugger", i)
  