from renderer.key import *
from renderer.sprite.otter import *
from util.bb import *
from util.debugger import *
from util.key import *
from level.player_control import *
from renderer.button import *

from renderer.sprite.human import *
from renderer.key import *
from util.polygon import *

from level.pathfinder import *
from level.follower import *

def setupEnd():
  initPlayerControl(1920/2, 1080/2)
  global lvl_bg, level_audio
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  global grid, calc_paths
  calc_paths = []
  grid = construct_grid()
  level_audio = "end"
  return

def cleanupEnd():
  global humans
  humans = {}
  return

def drawEnd():
  playerControlTick() # cause why not
  global lvl_bg, debug_bb, humans, grid, pX, pY, score
  image(lvl_bg, 0, 0)
  
  fill(0)
  # center of the screen
  text("Game Over", 1920/2 - 100, 1080/2 - 100)
  text("Score: " + str(score), 1920/2 - 100, 1080/2 + 50)

  fill(0,0,0)
  tickFollower()
  drawOtter(pX, pY, 0.5)
  return