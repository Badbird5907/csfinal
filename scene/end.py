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
  # initPlayerControl(1920/2, 1080/2)
  global lvl_bg, level_audio
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  #global grid, calc_paths
  #calc_paths = []
  # grid = construct_grid()
  level_audio = "end"
  return

def cleanupEnd():
  global humans
  humans = {}
  return

def drawEnd():
  # playerControlTick() # cause why not
  global lvl_bg, debug_bb, humans, grid, pX, pY, score
  image(lvl_bg, 0, 0)
  
  fill(0)
  # center of the screen
  text("Game Over", 1920/2 - 100, 1080/2 - 100)
  score_txt = "Score: " + str(score)
  score_width = textWidth(score_txt)
  text(score_txt, 1920/2 - (score_width/2 + 45), 1080/2 - 50)
  w = getTxtButtonWidth("Main Menu")
  drawTextButton("play-again-btn", 1920/2 - w + 30, 1080/2, "Main Menu", None, w)
  if (isButtonClicked("play-again-btn")):
    global scene, extra_score#, humans, calc_paths
    scene = "main"
    extra_score = 0
    #humans = {}
    #calc_paths = []
    return

  fill(0,0,0)
  # tickFollower()
  global otter_state
  otter_state = 1
  drawSleep(600, 450, True)
  return