from Processing3 import *
from renderer.brainrot import playBrainRot
from scene.scene import *
from renderer.key import *
from util.font import loadMinecraftFont
from util.ticker import *
from renderer.renderer import *
from renderer.fps import drawFPS
from renderer.human import *
from renderer.toast import *
from renderer.button import *
from util.debugger import *
from util.key import *
from util.audio import *
from level.follower import *
from level.pathfinder import *

from renderer.debug.goaleditor import *
from renderer.debug.polyeditor import *
from renderer.debug.raycastdbg import *

def setup():
  global scene, tick, last_input, heldKeys, lastScene
  global tile_size, typedKey, mspt, last_ticks, mspt_overhead, last_tick_overhead, last_tick_end, mspt_total
  global water_polys, score, tid, runningTids, difficulty
  scene = "main"
  last_input = millis()
  tick = 0
  heldKeys = []
  tile_size = 32
  typedKey = None
  lastScene = "dummy"
  difficulty = "hard"
  tid = 0
  runningTids = []
  
  mspt = 0
  last_ticks = []
  mspt_overhead = 0
  last_tick_overhead = []
  last_tick_end = millis()
  mspt_total = 0

  water_polys = []
  score = 0

  size(1920 - 200, 1080 - 202)
  setupRenderers()
  initDebugger()

  initFollower()
  initAudio()

  print(__cwd__)

  loadMinecraftFont()
  setInterval(calculatePaths, 50)
  #playBrainRot("https://cdn.badbird.dev/assets/brainrot/parkour.webm", 10, 40)
  #playBrainRot("https://cdn.badbird.dev/assets/brainrot/subway.webm", 1550, 40)
  return

def draw():
  global mspt, last_ticks, mspt_overhead, last_tick_overhead, last_tick_end, total_ms, mspt_total # Overhead mspt is the entire time taken to render the frame, not just the game logic
  start = millis()

  overhead = start - last_tick_end
  last_tick_overhead.append(overhead)
  if len(last_tick_overhead) > 10:
    last_tick_overhead.pop(0)
  mspt_overhead = sum(last_tick_overhead) / len(last_tick_overhead)

  #textAlign(CENTER, CENTER)
  clear()
  update()
  drawScene()
  drawToasts()
  drawFPS()
  updateButtons()
  keyRenderEnd()

  ms = millis() - start
  last_ticks.append(ms)
  if len(last_ticks) > 10:
    last_ticks.pop(0)
  mspt = sum(last_ticks) / len(last_ticks)

  mspt_total = mspt + mspt_overhead

  last_tick_end = millis()
  return


def mouseReleased():
  print("mouse down")
  print(mouseX, mouseY)
  goalEditorMouseClicked()
  polyEditorMouseClicked()
  rayCastDbgMouseClicked()
  buttonsHandleClick()

  playAudio("vine-boom")
