from Processing3 import *

def fixBB(bb):
  return [(min(bb[0][0], bb[1][0]), min(bb[0][1], bb[1][1])), (max(bb[0][0], bb[1][0]), max(bb[0][1], bb[1][1]))]
def fixBBMin(bb):
  return (min(bb[0][0], bb[1][0]), min(bb[0][1], bb[1][1]))
def fixBBMax(bb):
  return (max(bb[0][0], bb[1][0]), max(bb[0][1], bb[1][1]))
def isInsideBB(bbMin, bbMax, pos):
  # min and max might be swapped
  fixedMin = fixBBMin((bbMin, bbMax))
  fixedMax = fixBBMax((bbMin, bbMax))
  if (pos[0] >= fixedMin[0] and pos[0] <= fixedMax[0] and pos[1] >= fixedMin[1] and pos[1] <= fixedMax[1]):
    return True
  return False

def isInsideBBList(bbList, pos):
  for bb in bbList:
    if isInsideBB(bb[0], bb[1], pos):
      return True
  return False

def isPlayerInsideBB(bb):
  global pX, pY
  return isInsideBB(bb[0], bb[1], (pX, pY))

def drawBB(min, max, rgb = (255, 0, 0)):
  stroke(rgb[0], rgb[1], rgb[2])
  noFill()
  rect(min[0], min[1], max[0] - min[0], max[1] - min[1])
  return

def isOnEdgeOfBB(bbMin, bbMax, pos):
  fixedMin = fixBBMin((bbMin, bbMax))
  fixedMax = fixBBMax((bbMin, bbMax))
  if (pos[0] == fixedMin[0] or pos[0] == fixedMax[0] or pos[1] == fixedMin[1] or pos[1] == fixedMax[1]):
    return True
  return False