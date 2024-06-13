from renderer.key import *
from renderer.sprite.otter import *
from util.bb import *
from util.debugger import *
from util.key import *
from level.player_control import *
from renderer.button import *

from renderer.human import *
from renderer.key import *
from util.polygon import *

from level.pathfinder import *
from level.follower import *

def setupBlank():
  initPlayerControl(1920/2, 1080/2)
  global lvl_bg
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  global grid, calc_paths
  calc_paths = []
  grid = construct_grid()
  return

def cleanupBlank():
  global humans
  humans = {}
  return

def drawBlank():
  playerControlTick()
  global lvl_bg, debug_bb, humans, grid, pX, pY
  image(lvl_bg, 0, 0)

  polygon = [(800, 344), (568, 600), (1008, 656), (1272, 432), (1064, 208)]
  color = (255,0,0)
  inside = isInsidePolygon((pX, pY), polygon)
  # print(inside)
  if inside:
     color = (0, 0, 255)
  drawPolygon(polygon, color)

  fill(0,0,0)
  if (isKeyPressed("e")):
      global scene
      scene = "game"
  tickFollower()
  drawOtter(pX, pY, 0.5)
  return