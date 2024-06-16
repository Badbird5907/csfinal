from renderer.key import *
from renderer.sprite.otter import *
from util.bb import *
from util.debugger import *
from util.key import *
from level.player_control import *
from renderer.button import *

from renderer.sprite.human import *
from renderer.key import *

from level.pathfinder import *
from level.follower import *

def setupIntro():
  initPlayerControl(1920/2, 1080/2)
  global lvl_bg, intro_water_img, hp
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  intro_water_img = loadImage("assets/levels/intro/water.png")
  global intro_state
  intro_state = 0
  global grid, calc_paths
  calc_paths = []
  grid = construct_grid()
  hp = 9999
  return

def cleanupIntro():
  global humans
  humans = {}
  return

def drawIntro():
  playerControlTick()
  global lvl_bg, debug_bb, intro_state, humans, intro_water_img, grid
  image(lvl_bg, 0, 0)

  fill(0,0,0)
  start = (1920/2 - 260, 1080/2 - 100)
  water_bb_min = (162, 478)
  water_bb_max = (423, 708)
  if (intro_state == 0):
    text("Welcome to the Otter Game!", start[0] + 20, start[1])
    text("Press", start[0], start[1] + 50)
    offset = getKeyOffset()
    renderKeyAnimated(start[0] + 90, start[1] + offset, "W")
    renderKeyAnimated(start[0] + 130, start[1] + offset, "A")
    renderKeyAnimated(start[0] + 170, start[1] + offset, "S")
    renderKeyAnimated(start[0] + 210, start[1] + offset, "D")
    text("to move!", start[0] + 260, start[1] + 50)
    if (isKeyPressed("w") or isKeyPressed("a") or isKeyPressed("s") or isKeyPressed("d")):
      intro_state = 1
      createEntity(1920/2, 1080/2 + 100)
  elif (intro_state == 1):
    text("These are humans", start[0] + 70, start[1])
    text("Press ", start[0], start[1] + 50)
    offset = getKeyOffset()
    renderKeyAnimated(start[0] + 90, start[1] + offset, "SPACE")
    text(" to make them follow you!", start[0] + 160, start[1] + 50)
    if (len(getHumansFollowing()) > 0):
      intro_state = 2
  elif (intro_state == 2):
    image(intro_water_img, 0, 0)
    text("This is water", start[0] + 70, start[1])
    text("Try leading them there!", start[0], start[1] + 50)
    if debug_bb:
      stroke(255, 0, 0)
      noFill()
      rect(water_bb_min[0], water_bb_min[1], water_bb_max[0] - water_bb_min[0], water_bb_max[1] - water_bb_min[1])  
    for id in humans:
      human = humans[id]
      if human["hidden"]:
        continue
      pos = human["pos"]
      #print(pos, water_bb_min, water_bb_max)
      if isInsideBB(water_bb_min, water_bb_max, pos):
        intro_state = 3
  elif (intro_state == 3):
    image(intro_water_img, 0, 0)
    text("Great!", start[0] + 100, start[1])
    text("Now Press ", start[0] - 50, start[1] + 50)
    offset = getKeyOffset()
    renderKeyAnimated(start[0] + 90, start[1] + offset, "SPACE")
    text(" again to make them stop following!", start[0] + 160, start[1] + 50)
    if (len(getHumansFollowing()) == 0):
      intro_state = 4
      for id in humans:
        removeEntity(id)
      createEntity(1920/2, 1080/2 + 100, True)
      createEntity(1920/2 - 75, 1080/2 + 100, True)
  elif (intro_state == 4):
    image(intro_water_img, 0, 0)
    text("These are enemies", start[0] + 70, start[1])
    text("They will try to catch you!", start[0], start[1] + 50)
    text("Press ", start[0] + 30, start[1] + 100)
    renderKeyAnimated(start[0] + 120, start[1] + getKeyOffset() + 50, "x")
    text(" to kill them!", start[0] + 160, start[1] + 100)
    if (len(getAllEnemies()) == 0):
      intro_state = 5
  elif (intro_state == 5):
    image(intro_water_img, 0, 0)
    text("That's it!", start[0] + 100, start[1])
    text("Enjoy the game!", start[0] + 70, start[1] + 50)
    text("Press ", start[0] + 30, start[1] + 100)
    offset = getKeyOffset()
    renderKeyAnimated(start[0] + 120, start[1] + offset + 50, "E")
    text(" to start!", start[0] + 160, start[1] + 100)
  renderKey(width - 140, height - 85 - getKeyOffset(), "e", False)
  text("Skip", width - 100, height - 85)
  if (isKeyPressed("e")):
      global scene
      scene = "game"
  tickFollower()
  drawOtter(pX, pY, 0.5)
  return