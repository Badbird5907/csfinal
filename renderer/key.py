from Processing3 import *
def initKeyRenderer():
  global keySprites
  keySprites = {}
  return
def renderKey(x,y, key_name, pressed, _scale = 1):
  global keySprites
  if (pressed):
    file = "assets/keys/" + key_name.upper() + "_pressed.png"
  else:
    file = "assets/keys/" + key_name.upper() + ".png"
  if not file in keySprites:
    keySprites[file] = loadImage(file)
  img = keySprites[file]
  w = img.width * _scale
  h = img.height * _scale
  image(img, x, y, w, h)
  return

def renderKeyAnimated(x, y, key_name, scale = 1):
  global tick
  renderKey(x,y,key_name, (tick % 60) < 30, scale)

def getKeyOffset():
  return 25