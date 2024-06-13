from Processing3 import *

from util.bb import *
from util.key import *
from util.debugger import drawControl, drawTextTitle
from util.math import *

def initGoalEditor():
  global geMin, geBBs, geTileSize, confirmDeleteAllBBs
  geMin = None
  # a list of bounding boxes
  geBBs = []
  geTileSize = 8
  confirmDeleteAllBBs = False
def ge_findClosestMouseSnap():
  # return the nearest SIDE of a bounding box, which we can snap to, doesn't have to be a corner
  maxDist = 20
  global geMin, geBBs, geTileSize
  minDist = None
  minPoint = None
  for bb in geBBs:
    # bb corners
    minX, minY = bb[0]
    maxX, maxY = bb[1]
    
    points = []
    # top / bottom sides
    for x in range(minX, maxX + geTileSize, geTileSize):
      points.append((x, minY))
      points.append((x, maxY))
    # l/r sides
    for y in range(minY, maxY + geTileSize, geTileSize):
      points.append((minX, y))
      points.append((maxX, y))
    
    # calc the euclidean distance between the mouse and each point
    for (x, y) in points:
      # dist = sqrt((p1-q1)^2 + (p2 - q2)^2) https://en.wikipedia.org/wiki/Euclidean_distance
      # dist = sqrt((mouseX - x) ** 2 + (mouseY - y) ** 2)
      dist = euclidean_dist((mouseX, mouseY), (x, y))
      if (minDist is None or dist < minDist) and dist <= maxDist:
        minDist = dist
        minPoint = (x, y)
        
  if minPoint is None:
    return None
  return (minPoint, minDist)

def ge_snapToGrid(pos, tile_size):
  closest = ge_findClosestMouseSnap()
  if (not closest == None): # if a closest bb snap exists, return that
    return (closest[0][0] // tile_size, closest[0][1] // tile_size)
  return (pos[0] // tile_size, pos[1] // tile_size)
def goalEditorMouseClicked():
  global geMin, geBBs, geTileSize, enableGoalBBEditor
  if (not enableGoalBBEditor):
    return
  # left click = place point
  # right click on a bb = remove bb
  snapped = ge_snapToGrid((mouseX, mouseY), geTileSize)
  expanded = (snapped[0] * geTileSize, snapped[1] * geTileSize)

  if (isKeyPressed(65535)): # ctrl
    expanded = (mouseX, mouseY)

  if (mouseButton == LEFT):
    if (geMin == None):
      geMin = expanded # set geMin
    else:
      fixedMin = fixBBMin((geMin, expanded))
      fixedMax = fixBBMax((geMin, expanded))
      bb = (fixedMin, fixedMax)
      geBBs.append(bb) # finish bb, add to the list
      geMin = None # reset geMin
  elif (mouseButton == RIGHT):
    print(len(geBBs), geBBs)
    for i in range(len(geBBs)):
      bb = geBBs[i]
      if (isInsideBB(bb[0], bb[1], (mouseX, mouseY))):
        geBBs.pop(i) # yeet it
        break
      else:
        print("Not inside bb", bb)
  print("---------")
  return

def drawGoalEditor(): # we want to select a number of bounding boxes
  global geMin, geBBs, pX, pY, geTileSize, confirmDeleteAllBBs
  for bb in geBBs:
    drawBB(bb[0], bb[1])

  #mSnap = snapToGrid((mouseX, mouseY), geTileSize) if not isKeyPressed(65535) else ((int(mouseX // 1), int(mouseY // 1)), None)
  altPressed = isKeyPressed(65535)
  if (altPressed):
    mSnap = (mouseX, mouseY)
  else:
    mSnap = ge_snapToGrid((mouseX, mouseY), geTileSize)
  if (not mSnap == None):
    coords = mSnap
    if (not altPressed):
      coords = (mSnap[0] * geTileSize, mSnap[1] * geTileSize)
    ellipse(coords[0], coords[1], 5, 5)
    if (not geMin == None):
      ellipse(geMin[0], geMin[1], 5, 5)
      drawBB(geMin, (coords[0], coords[1]), (0, 0, 255))
  
  if (isKeyTyped("u")):
    if (confirmDeleteAllBBs):
      geBBs = []
      confirmDeleteAllBBs = False
    else:
      confirmDeleteAllBBs = True
  
  if (isKeyPressed("c")):
    geMin = None
  
  if (isKeyPressed("p")):
    print(geBBs)

  return


def ge_drawDebuggerControls():
  global confirmDeleteAllBBs
  i = 0
  altPressed = isKeyPressed(65535)
  controls = [
    ("k", "Toggle goal bounding box editor (ON)", True),
    ("alt", "Let go to turn on snapping" if altPressed else "Hold to turn off snapping" , altPressed),
    ("c", "Cancel placing bounding box", False),
    ("u", "Press again if you want to delete all BBs!" if confirmDeleteAllBBs else "Delete all bounding boxes", confirmDeleteAllBBs, (255, 0, 0) if confirmDeleteAllBBs else None),
    ("p", "Print bounding boxes", False),
  ]
  for control in controls:
    rgb = control[3] if len(control) > 3 else None
    drawControl(control[0], control[1], i, control[2], 0, rgb)
    i += 1
  drawTextTitle("Goal BB Editor", i)
  return