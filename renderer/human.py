from Processing3 import *
from util.random import *
from util.key import *
from util.bb import *
from util.ticker import *

from renderer.key import *

from renderer.toast import *

from util.polygon import *

def initHumanRenderer():
  global humans, human_skincache, uniqHumanId
  humans = {}
  human_skincache = []
  uniqHumanId = 0
  variants = ["back", "front", "side"]
  for id in range(1, 21):
    dict = {}
    for variant in variants:
      base = "assets/humans/split/" + str(id) + "/"
      base_file = base + variant + ".png"
      walk1_file = base + variant + "_walk_1.png"
      walk2_file = base + variant + "_walk_2.png"
      dict[variant] = [loadImage(base_file), loadImage(walk1_file), loadImage(walk2_file)]
    human_skincache.append(dict)
  return

def createHuman(x, y):
  global uniqHumanId
  # sequential id
  randid = uniqHumanId
  uniqHumanId += 1
  randskin = randInt(1, 21)
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
  }
  humans[randid] = dict
  print("Human created at " + str(x) + ", " + str(y) + " with id " + str(randid) + " and debug color " + str(dict["pf_debug_color"]))
  return randid

def removeHuman(id):
  global humans
  if id in humans:
    #del humans[id]
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


def getSkins(id):
  global human_skincache # { 1: { back: [img, img, img]... }}
  return human_skincache[id - 1]

def getSpriteId(human):
  if human["state"] == "idle" or millis() - human["last_follow_ms"] > 500:
    return 0
  if human["follow"] and "speed" in human:
    # animate faster depending on move speed (2, 1.5, 1)
    if human["speed"] == 1: # slow
      return getTick() % 60 < 30
    elif human["speed"] == 1.5: # medium
      return getTick() % 30 < 15
    elif human["speed"] == 2: # fast
      return getTick() % 20 < 10
  if getTick() % 60 < 30:
    return 2
  return 1

def drawHuman(id):
  global humans, pX, pY, pbbMax, debug_bb
  if id not in humans or humans[id]["hidden"]:
    return
  human = humans[id]
  #print(human)
  pos = human["pos"]
  skin = human["skin"]
  facing = human["facing"]
  skins = getSkins(skin)
  if skins == None:
    print("Human " + str(id) + " has no skin (" + str(skin) + ")")
    return
  sid = getSpriteId(human)
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
  bbMin = (pX, pY)
  bbMax = (pX + 100, pY + 100) #(pX + pbbMax[0], pY + pbbMax[1])
  if False and debug_bb:
    stroke(0, 255, 0)
    noFill()
    rect(bbMin[0], bbMin[1], pbbMax[0], pbbMax[1])
  if (isInsideBB(bbMin, bbMax, pos)):
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
    drawHuman(id)
  return