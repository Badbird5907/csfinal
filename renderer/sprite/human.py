from Processing3 import *
from util.random import *
from util.key import *
from util.bb import *
from util.ticker import *
from util.polygon import *
from util.audio import *

from renderer.key import *
from renderer.toast import *


def loadSkins(min, max, folder):
  variants = ["back", "front", "side"]
  skins = []
  for id in range(min, max):
    dict = {}
    for variant in variants:
      base = folder + str(id) + "/"
      base_file = base + variant + ".png"
      walk1_file = base + variant + "_walk_1.png"
      walk2_file = base + variant + "_walk_2.png"
      dict[variant] = [loadImage(base_file), loadImage(walk1_file), loadImage(walk2_file)]
      skins.append(dict)
  return skins

def initHumanRenderer():
  global humans, human_skincache, uniqHumanId, enemy_skincache
  humans = {}
  human_skincache = []
  uniqHumanId = 0
  human_skincache = loadSkins(1, 19, "assets/humans/split/")
  enemy_skincache = loadSkins(1, 3, "assets/enemies/")  
  return

def createEntity(x, y, enemy = False):
  global uniqHumanId
  # sequential id
  randid = uniqHumanId
  uniqHumanId += 1
  randskin = randInt(1, 19) if not enemy else randInt(1, 3)
  dict = {
    "pos": (x, y),
    "skin": randskin,
    "facing": randArr(["front", "back", "left", "right"]),
    "state": "idle", # idle / run
    #"run_state": False,
    "follow": False,
    "pf_debug_color": (randInt(0, 255), randInt(0, 255), randInt(0, 255)),
    "last_follow_ms": millis(),
    "last_wander_ms": millis(),
    "next_wander_ms": randInt(3500, 7000),
    "id": randid,
    "hidden": False,
    "enemy": enemy,
    "enemy_last_atk_ms": millis(),
    "enemy_next_atk_ms": randInt(1200, 1900),
    "enemy_fade_start": -1,
  }
  humans[randid] = dict
  print("Human created at " + str(x) + ", " + str(y) + " with id " + str(randid) + " and debug color " + str(dict["pf_debug_color"]))
  return randid

def removeEntity(id):
  global humans
  if id in humans:
    #del humans[id]
    if humans[id]["enemy"]:
      humans[id]["enemy_fade_start"] = millis()
    else:
      humans[id]["hidden"] = True
  return

def isHumanAtWater(human):
  if not "water_polys" in globals():
    return False
  global water_polys
  for poly in water_polys:
    if isInsidePolygon(human["pos"], poly):
      return True
  return False


def getSkins(id, enemy = False):
  if enemy:
    global enemy_skincache
    return enemy_skincache[id - 1]
  global human_skincache # { 1: { back: [img, img, img]... }}
  return human_skincache[id - 1]

def getSpriteId(human):
  if not human["enemy"] and (human["state"] == "idle" or millis() - human["last_follow_ms"] > 500):
    return 0
  if human["enemy"] and not human["hidden"] and human["enemy_fade_start"] != -1:
    return 0
  if (human["follow"] or human["enemy"]) and "speed" in human:
    # animate faster depending on move speed (2, 1.5, 1)
    if human["speed"] == 1: # slow
      return getTick() % 60 < 30
    elif human["speed"] == 1.5: # medium
      return getTick() % 30 < 15
    #elif human["speed"] == 2: # fast
    else: # fast
      return getTick() % 20 < 10
  if getTick() % 60 < 30:
    return 2
  return 1

def drawEntity(id):
  global humans, pX, pY, pbbMax, debug_bb
  if id not in humans:
    return
  human = humans[id]
  if human["hidden"] and not human["enemy"]:
    return
  #print(human)
  pos = human["pos"]
  skin = human["skin"]
  facing = human["facing"]
  skins = getSkins(skin, human["enemy"])
  if skins == None:
    print("Human " + str(id) + " has no skin (" + str(skin) + ")")
    return
  sid = getSpriteId(human)
  tint(255, 255)
  if human["enemy"] and human["enemy_fade_start"] != -1:
    fade_duration = 1000
    if millis() - human["enemy_fade_start"] > fade_duration:
      human["hidden"] = True
      return
    alpha = map(millis() - human["enemy_fade_start"], 0, fade_duration, 255, 0)
    # print("alpha: " + str(alpha))
    tint(255, alpha)
  bbMin = (pX, pY)
  bbMax = (pX + 100, pY + 100) #(pX + pbbMax[0], pY + pbbMax[1])
  if False and debug_bb:
    stroke(0, 255, 0)
    noFill()
    rect(bbMin[0], bbMin[1], pbbMax[0], pbbMax[1])
  if (human["enemy"] and human["enemy_fade_start"] == -1):
    enemyAtkBBMin = (pX - 50, pY - 50)
    enemyAtkBBMax = (pX + 150, pY + 150)
    if debug_bb:
      drawBB(enemyAtkBBMin, enemyAtkBBMax, (0, 255, 255))
    if (isInsideBB(enemyAtkBBMin, enemyAtkBBMax, pos)):
      tint(255, 0, 0)
      if (isKeyTyped("x")):
        removeEntity(id)
        global extra_score, difficulty, hp
        extra_score += 5 if difficulty == "hard" else (2 if difficulty == "medium" else 1)
        # 25% chance to add 1 hp on easy, 15% on medium, 10% on hard
        if (randInt(1, 100) <= (25 if difficulty == "easy" else (15 if difficulty == "medium" else 10))):
          hp += 1
  if facing == "front":
    image(skins["front"][sid], pos[0], pos[1])
  elif facing == "back":
    image(skins["back"][sid], pos[0], pos[1])
  elif facing == "right":
    image(skins["side"][sid], pos[0], pos[1])
  elif facing == "left":
    # flip the image
    pushMatrix()
    translate(pos[0] + skins["side"][0].width, pos[1])
    scale(-1, 1)
    image(skins["side"][sid], 0, 0)
    popMatrix()
  #print("Human drawn at " + str(pos[0]) + ", " + str(pos[1]) + " with id " + str(id))

  # check if the human is inside the bounding box
  if (isInsideBB(bbMin, bbMax, pos)):
    if not human["enemy"]:
      renderKeyAnimated(pos[0], pos[1] + 32, "SPACE", 0.5)
      if (getKeyTyped() == " "):
        global calc_paths
        if "max_humans_following" in globals():
          global max_humans_following
          if not human["follow"] and max_humans_following > 0 and len(getHumansFollowing()) >= max_humans_following:
            print("Showing toast")
            createToast("You can only have " + str(max_humans_following) + " humans following at a time", 2000)
            return
        human["follow"] = not human["follow"]
        if id in calc_paths:
          calc_paths[id]["path"] = []
        if (not human["follow"]):
          human["state"] = "idle"
        print("Human " + str(id) + " following player: " + str(human["follow"]))
    else:
      if human["enemy_fade_start"] != -1:
        return
      # enemy
      lastAtkMs = human["enemy_last_atk_ms"]
      nextAtkMs = human["enemy_next_atk_ms"] # 1200 - 1900
      if millis() - lastAtkMs > nextAtkMs:
        human["enemy_last_atk_ms"] = millis()
        human["enemy_next_atk_ms"] = randInt(1200, 1900)
        print("Enemy attacking player")
        global hp, last_atk, meme_muted
        hp -= 1
        last_atk = millis()
        playAudio("hurt" if meme_muted else "classic_hurt")
  return

def getHumansFollowing():
  global humans
  following = []
  for id in humans:
    if humans[id]["hidden"]:
      continue
    if humans[id]["follow"]:
      following.append(id)
  return following

def drawAllHumans():
  global humans
  for id in humans:
    if humans[id]["hidden"]:
      continue
    #print("Drawing human " + str(id))
    drawEntity(id)
  return

def getAllEnemies():
  global humans
  enemies = []
  for id in humans:
    if humans[id]["hidden"] or humans[id]["enemy_fade_start"] != -1:
      continue
    if humans[id]["enemy"]:
      enemies.append(id)
  return enemies