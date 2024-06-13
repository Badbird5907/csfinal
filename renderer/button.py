from Processing3 import *
from util.bb import *

def initButtonRenderer():
  global buttonSprites
  buttonSprites = {}
  return

def getTxtButtonWidth(txt):
  textSize(20)
  return textWidth(txt) + 40

def drawTextButton(x,y, txt, height=None,width=None):
  textSize(20)
  if height == None:
    height = 45
  if width == None:
    width = getTxtButtonWidth(txt)

  # button bounds
  min = (x, y)
  max = (x + width, y + height)
  if (isMouseHovering(min, max)):
    fill(0, 255, 0)
    cursor(HAND)
  else:
    fill(255, 255, 255)
    cursor(ARROW)
  
  rect(x, y, width, height)
  fill(0, 0, 0)
  text(txt, x + 20, y + 30)
  return

def __getButtonSprite(name):
  global buttonSprites
  if name in buttonSprites:
    return buttonSprites[name]
  # load
  img = loadImage("assets/buttons/" + name + ".png")
  buttonSprites[name] = img
  return img

def getHoverScale(min, max):
  global currentHover, currentHoverTime
  if (isMouseHovering(min, max)):
    currentHover = True
    currentHoverTime += 1
    return 1 + (currentHoverTime / 10)
  currentHover = False
  currentHoverTime = 0
  return 1

def drawImageButton(x,y, img, hoverImg=None, height=None,width=None):
  sprite = __getButtonSprite(img)
  width = sprite.width
  height = sprite.height
  # button bounds
  min = (x, y)
  max = (x + width, y + height)
  scale = getHoverScale(min, max)
  if hoverImg != None:
    hoverSprite = __getButtonSprite(hoverImg)
    image(hoverSprite, x, y, hoverSprite.width * scale, hoverSprite.height * scale)
  else:
    image(sprite, x, y, sprite.width * scale, sprite.height * scale)
  return