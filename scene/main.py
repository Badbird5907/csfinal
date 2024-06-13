from Processing3 import *

from renderer.button import *

def setupMain():
  global lvl_bg
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  return

def cleanupMain():
  global humans
  humans = {}
  return

def drawMain():
  global lvl_bg, debug_bb, humans, grid, pX, pY, score
  image(lvl_bg, 0, 0)
  
  fill(0)
  textSize(32)
  txt = "Otter Game"
  width = textWidth(txt)
  text(txt, 1920/2 - width, 1080/2 - 100)
  drawTextButton(1920/2 - 100, 1080/2, "Start Game")
  return