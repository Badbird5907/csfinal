from renderer.key import *
from renderer.sprite.otter import *
from util.bb import *
from util.key import *
from level.player_control import *
from renderer.button import *
from util.debugger import *
from level.pathfinder import *
from level.follower import *
from level.scoretracker import *
from level.timer import *
from util.audio import *

def game_countScore():
  global humans, difficulty, extra_score
  if (difficulty != "easy"):
    humansScore = 0
  for id in humans: # make sure there is no concurrent modification issues
    human = humans[id]
    if (human["hidden"] or human["enemy"]):
      continue
    # if the human x is > 850
    pos = human["pos"]
    if (pos[0] > 850):
      if (isHumanAtWater(human)):
        if (difficulty == "easy"):
          extra_score += 5
          removeEntity(id)
          playAudio("splash_in")
        else:
          humansScore += 10
  return humansScore + extra_score

def game_endGame():
  global scene
  scene = "end"
  return

def setupGame():
  initPlayerControl(1920/2, 1080/2)
  global lvl_bg, main_trees, grid, last_human_spawn, max_humans_following
  global water_polys, timer_seconds, difficulty, hp, last_enemy_spawn, enemy_spawn_rate
  lvl_bg = loadImage("assets/levels/1/bg.png")
  main_trees = loadImage("assets/levels/1/trees.png")
  initDebugger()
  last_human_spawn = -1
  max_humans_following = 3 if difficulty == "hard" else (5 if difficulty == "medium" else -1)
  last_enemy_spawn = millis()
  if difficulty == "hard":
    hp = 5
    enemy_spawn_rate = 4500
  elif difficulty == "medium":
    hp = 7
    enemy_spawn_rate = 6000
  else:
    hp = 9
    enemy_spawn_rate = 7500
  grid = construct_grid()
  water_polys = [[(864, 872), (1000, 640), (1128, 464), (1232, 248), (1448, 0), (1632, 0), (1576, 104), (1392, 312), (1280, 496), (1168, 688), (1048, 872), (864, 872)]]
  initTimer(60 * 2, game_endGame)
  setupScoreTracker(game_countScore)
  return


def cleanupGame():
  global water_polys
  water_polys = []
  cleanupScoreTracker()
  return

def drawGame():
  playerControlTick(game_endGame)
  global lvl_bg, main_trees, debug_bb, last_human_spawn, pX, pY, water_polys
  global meme_muted, last_enemy_spawn, enemy_spawn_rate
  image(lvl_bg, 0, 0)

  tickFollower()

  tree_bb = [((0, 0), (696, 208)), ((0, 208), (640, 312)), ((0, 312), (632, 432)), ((0, 432), (488, 472)), ((0, 472), (224, 552)), ((224, 472), (336, 520))]
  #[[(0, 0), (698, 205)],[(0, 205), (669, 310)],[(0, 310), (634, 436)],[(0, 436), (418, 548)] ]

  showDbgBBList(tree_bb)

  #inside = isInsidePolygon((pX, pY), water_poly)
  #print(inside)
  #color = (0, 0, 255) if inside else (255,0,0)
  showDbgPolyBB(water_polys)


  should_tint = isInsideBBList(tree_bb, (pX, pY))

  if should_tint:
    tint(255, 128)

  image(main_trees, 0, 0)
  noTint()

  if (millis() - last_human_spawn > 5000):
    # create a random human in the tree area
    hX = random(0, 669)
    hY = random(205, 310)
    createEntity(hX, hY)
    last_human_spawn = millis()
  
  if (millis() - last_enemy_spawn > enemy_spawn_rate):
    # create a random enemy in the tree area
    hX = random(0, 1000)
    hY = random(205, 400)
    createEntity(hX, hY, True)
    last_enemy_spawn = millis()
  
  drawTimer()
  drawScore()

  textSize(16)


  drawOtter(pX, pY, 0.5)
  return