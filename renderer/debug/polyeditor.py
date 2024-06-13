from Processing3 import *

from renderer.toast import createToast
from util.key import *
from util.debugger import drawControl, drawTextTitle
from util.math import *
from util.polygon import *

def initPolyEditor():
  global pePolyPoints, peTileSize, confirmDeleteAllBBs
  pePolyPoints = []
  peTileSize = 8
  confirmDeleteAllBBs = False
  return

def pe_findClosestMouseSnap():
  maxDist = 20
  global pePolyPoints, peTileSize
  minDist = None
  minPoint = None
  for point in pePolyPoints:
    dist = euclidean_dist((mouseX, mouseY), point)
    if (minDist is None or dist < minDist) and dist <= maxDist:
      minDist = dist
      minPoint = point
  if minPoint is None:
    return None
  return (minPoint, minDist)

def pe_snapToGrid(pos, tile_size):
  closest = pe_findClosestMouseSnap()
  if (not closest == None):
    return (closest[0][0] // tile_size, closest[0][1] // tile_size)
  return (pos[0] // tile_size, pos[1] // tile_size)

def drawPolyEditor():
  global pePolyPoints, peTileSize, confirmDeleteAllBBs, enablePolygonBBEditor
  # draw the points
  validPoly = isValidPolygon(pePolyPoints)
  fill(255, 0, 0)
  if (validPoly):
    stroke(0, 0, 255)
  else:
    stroke(255, 0, 0)

  snapped = pe_snapToGrid((mouseX, mouseY), peTileSize)
  expanded = (snapped[0] * peTileSize, snapped[1] * peTileSize)
  ellipse(expanded[0], expanded[1], 5, 5)

  for point in pePolyPoints:
    ellipse(point[0], point[1], 5, 5)
  
  drawPolygon(pePolyPoints)
  
  if (not validPoly and len(pePolyPoints) > 0):
    line(pePolyPoints[-1][0], pePolyPoints[-1][1], expanded[0], expanded[1])

  if (isKeyTyped("u")):
    if (confirmDeleteAllBBs):
      pePolyPoints = []
      confirmDeleteAllBBs = False
    else:
      confirmDeleteAllBBs = True
  
  if (isKeyTyped("o")):
    print(pePolyPoints)
  return

def polyEditorMouseClicked():
  global enablePolygonBBEditor, pePolyPoints
  if (not enablePolygonBBEditor):
    return
  if (isValidPolygon(pePolyPoints)): # disable if the polygon is valid
    createToast("This polygon is completed.", 3000)
    return
  snapped = pe_snapToGrid((mouseX, mouseY), peTileSize)
  expanded = (snapped[0] * peTileSize, snapped[1] * peTileSize)
  pePolyPoints.append(expanded)
  return

def pe_drawDebuggerControls():
  global confirmDeleteAllBBs
  i = 0
  altPressed = isKeyPressed(65535)
  controls = [
    ("p", "Toggle polygon editor (ON)", True),
    #("alt", "Let go to turn on snapping" if altPressed else "Hold to turn off snapping" , altPressed),
    ("u", "Press again if you want to delete all pBBs!" if confirmDeleteAllBBs else "Delete all bounding boxes", confirmDeleteAllBBs, (255, 0, 0) if confirmDeleteAllBBs else None),
    ("o", "Print the polygon", False),
  ]
  for control in controls:
    rgb = control[3] if len(control) > 3 else None
    drawControl(control[0], control[1], i, control[2], 0, rgb)
    i += 1
  drawTextTitle("Polygon Editor", i)
  return