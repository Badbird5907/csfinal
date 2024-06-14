from Processing3 import *
from util.bb import *

def initButtonRenderer():
  global buttonSprites, buttons, clicked_buttons
  buttonSprites = {}
  buttons = {}
  clicked_buttons = {}
  return

def getTxtButtonWidth(txt):
  textSize(20)
  return textWidth(txt) + 40

def updateButtons():
  global buttons, mspt_total, clicked_buttons
  new_buttons = {}
  for button in buttons: 
    if millis() - buttons[button]["timestamp"] < 250 + mspt_total:
      new_buttons[button] = buttons[button]
  buttons = new_buttons
  ids = []
  for button in clicked_buttons:
    if millis() - clicked_buttons[button]["timestamp"] > 250 + mspt_total: # if it isn't handled in 250ms
      ids.append(button)
  if len(ids) > 0:
    new_clicked_buttons = {}
    for button in clicked_buttons:
      if button not in ids:
        new_clicked_buttons[button] = clicked_buttons[button]
    clicked_buttons = new_clicked_buttons
  return

def buttonsHandleClick(): # handle release
  global buttons, clicked_buttons
  mouse = (mouseX, mouseY) 
  for button in buttons:
    btn = buttons[button]
    if (isInsideBB(btn["min"], btn["max"], mouse)):
      print("clicked", button)
      clicked_buttons[button] = {
        "id": button,
        "timestamp": millis()
      }

def isButtonClicked(id):
  global clicked_buttons
  if (id in clicked_buttons):
    # remove it
    del clicked_buttons[id]
    return True
  return False

def drawTextButton(id, x,y, txt, height=None,width=None):
  global buttons
  textSize(20)
  if height == None:
    height = 45
  if width == None:
    width = getTxtButtonWidth(txt)

  # button bounds
  min = (x, y)
  max = (x + width, y + height)
  buttons[id] = {
    "id": id,
    "min": min,
    "max": max,
    "txt": txt,
    "timestamp": millis()
  }
  mouse = (mouseX, mouseY)
  if (isInsideBB(min, max, mouse)):
    fill(0, 255, 0)
    #cursor(HAND)
  else:
    fill(255, 255, 255)
    #cursor(ARROW)
  
  rect(x, y, width, height)
  fill(0, 0, 0)
  # text(txt, x + 20, y + 30)
  # draw in the center of the button
  text(txt, x + (width - textWidth(txt)) / 2, y + 30)
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
  mouse = (mouseX, mouseY)
  if (isInsideBB(min, max, mouse)):
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