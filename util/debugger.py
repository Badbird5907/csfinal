from level.pathfinder import *
from renderer.key import *
from util.key import *
from renderer.human import *
from renderer.debug.goaleditor import *
from renderer.debug.polyeditor import *
from renderer.debug.raycastdbg import *
from util.polygon import *

def initDebugger():
  global debugger_enabled, debug_bb, drawPathfinder, enableGoalBBEditor, enablePolygonBBEditor
  global enableRayCastDebugger
  debugger_enabled = False
  debug_bb = False
  drawPathfinder = False
  enableGoalBBEditor = False
  enablePolygonBBEditor = False
  enableRayCastDebugger = False
  initGoalEditor()
  initPolyEditor()
  initRCDbg()

def drawControl(key, txt, i, pressed = False, extraOffset = 0, rgb = None):
  renderKey(16, 820 - i * 30, key, pressed, 1)
  if (not rgb == None):
    fill(rgb[0], rgb[1], rgb[2])
  else:
    fill(0)
  text(txt, 55 + extraOffset, 845 - i * 30)
  i += 1

def drawTextTitle(txt, i):
  fill(0)
  text(txt, 16, 845 - i * 30)
  i += 1

def tickDebuggerOverlay():
  global debugger_enabled, debug_bb, drawPathfinder, enableGoalBBEditor, enablePolygonBBEditor
  global enableRayCastDebugger
  if (getKeyTyped() == "j"):
    debugger_enabled = not debugger_enabled
    print("Debugger enabled:", debugger_enabled)
  if (not debugger_enabled):
    return
  if (typedKey == "b"):
    debug_bb = not debug_bb

  global grid, scene
  #print("dg")
  if (typedKey == "g"):
    drawPathfinder = not drawPathfinder
  if (drawPathfinder):
    draw_debugger_grid(grid)
  
  humanSpawned = False
  if (isKeyTyped("h")):
    global pX, pY
    createHuman(pX, pY)
    humanSpawned = True
  
  if (isKeyTyped("k")):
    enableGoalBBEditor = not enableGoalBBEditor
    enablePolygonBBEditor = False
    print("Goal BB editor enabled:", enableGoalBBEditor)
  
  if (isKeyTyped("p") and not enableGoalBBEditor):
    enablePolygonBBEditor = not enablePolygonBBEditor
    print("Polygon BB editor enabled:", enablePolygonBBEditor)
  
  if (isKeyTyped("r")):
    enableRayCastDebugger = not enableRayCastDebugger
    print("Ray cast debugger enabled:", enableRayCastDebugger)
  
  if (scene == "game" and isKeyTyped("e")):
    scene = "end"


  if (enableGoalBBEditor):
    drawGoalEditor()
  elif (enablePolygonBBEditor):
    drawPolyEditor()
  elif (enableRayCastDebugger):
    drawRCDbg()

  # draw controls on bottom left
  fill(0)
  textSize(16)
  if (enableGoalBBEditor):
    ge_drawDebuggerControls()
  elif (enablePolygonBBEditor):
    pe_drawDebuggerControls()
  elif (enableRayCastDebugger):
    rcdbg_drawDebuggerControls()
  else:
    controls = [
      ("j", "Toggle debugger (ON)", debugger_enabled),
      ("b", "Toggle bounding boxes " + ("(ON)" if debug_bb else "(OFF)"), debug_bb),
      ("g", "Toggle pathfinder grid (laggy but cool)", drawPathfinder),
      ("h", "Spawn human", humanSpawned),
      ("k", "Toggle goal bounding box editor", enableGoalBBEditor),
      ("p", "Toggle polygon editor", enablePolygonBBEditor),
      ("r", "Toggle ray cast debugger", enableRayCastDebugger)
    ]
    if (scene == "game"):
      controls.append(("e", "End game", False))
    i = 0
    for control in controls:
      drawControl(control[0], control[1], i, control[2])
      i += 1
    drawTextTitle("Debugger Controls", i)
  textSize(12)
  global pX, pY, velX, velY, humans, mspt, mspt_overhead, mspt_total
  fill(0)
  # text("P: " + str(round(pX, 2)) + ", " + str(round(pY, 2)) + " | Vel: " + str(round(velX, 2)) + ", " + str(round(velY, 2)) + " | M: " + str(mouseX) + ", " + str(mouseY) + " | H: " + str(len(humans)) + " | MSPT: " + str(mspt) + " | MSPTOH: " + str(mspt_overhead) + " | MSPT_TOT: " + str(mspt_total), 16, 870)
  text("P: " + str(round(pX, 2)) + ", " + str(round(pY, 2)), 16, 870)
  text("| Vel: " + str(round(velX, 2)) + ", " + str(round(velY, 2)), 150, 870)
  text("| M: " + str(mouseX) + ", " + str(mouseY), 280, 870)
  text("| H: " + str(len(humans)), 390, 870)
  text("| MSPT(G): " + str(mspt), 450, 870)
  text("| MSPT(O): " + str(mspt_overhead), 550, 870)
  text("| MSPT(T): " + str(mspt_total), 660, 870)
  
  return

def showDbgBB(bb):
  global debug_bb
  if debug_bb:
    drawBB(bb[0], bb[1])

def showDbgBBList(bbs):
  global debug_bb
  if debug_bb:
    for bb in bbs:
      drawBB(bb[0], bb[1])

def showDbgPolyBB(poly, color = None):
  global debug_bb
  if debug_bb:
    drawPolygon(poly, color)

def isDebuggerEnabled():
  global debugger_enabled
  return debugger_enabled