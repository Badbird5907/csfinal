from util.key import *
from util.audio import *

def initPlayerControl(spawnX, spawnY):
  global pX, pY, facing, velX, velY, pbbMax, last_walk_audio
  pX = spawnX
  pY = spawnY
  facing = "front"
  velX = 0
  velY = 0
  pbbMax = (0, 0)
  last_walk_audio = -1
def playerControlTick(endGameFunc = None):
  global pX, pY, facing, velX, velY, last_walk_audio, hp
  if (endGameFunc != None and hp <= 0):
    endGameFunc()
    return
  pXBefore = pX
  pYBefore = pY
  mov = 0.5
  if (isKeyPressed('a')):
    velX -= mov
    facing = "back"
  if (isKeyPressed('s')):
    #facing = "down"
    velY += mov
  if (isKeyPressed('w')):
    #facing = "up"
    velY -= mov
  if (isKeyPressed('d')):
    velX += mov
    facing = "front"

  # apply velocity
  pX += velX
  pY += velY
  # apply friction
  velX *= 0.9
  velY *= 0.9
  velX = round(velX, 4)
  velY = round(velY, 4)
  if (abs(velX) == 0.0005 and abs(velY) == 0.0005): # fix edge case where velocity rests at 0.0005
    velX = 0
    velY = 0

  if (round(pXBefore) != round(pX) or round(pYBefore) != round(pY)):
    global otter_state
    otter_state = "run"
    if (millis() - last_walk_audio > 2900):
      playAudio("grass")
      last_walk_audio = millis()
  else:
    otter_state = "idle"
    stopAudio("grass")
  
  # check out of bounds
  # TODO: dynamic bounds
  if (pX < 0):
    pX = 0
  if (pX > 1718 - 100):
    pX = 1718 - 100
  if (pY < 0):
    pY = 0
  if (pY > 877 - 100):
    pY = 877 - 100
  
  # zoom in on bg
  # edit: nvm this is rendered on the cpu lol
  #pushMatrix()
  #translate(-pX, -pY)
  #image(lvl_bg, 0, 0, width * 2, height * 2)
  #popMatrix()