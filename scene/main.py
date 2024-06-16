from Processing3 import *

from renderer.button import *
from renderer.key import *
from util.audio import *
from util.key import *

def setupMain():
  global lvl_bg, level_audio
  lvl_bg = loadImage("assets/levels/intro/bg.png")
  level_audio = "rick"
  return

def cleanupMain():
  global humans
  humans = {}
  stopAudio("rick")
  return

def drawMain():
  global lvl_bg, debug_bb, humans, grid, pX, pY, score, difficulty, meme_muted
  
  image(lvl_bg, 0, 0)
  
  fill(0)
  textSize(32)
  txt = "Otter Game"
  width = textWidth(txt)
  text(txt, 1920/2 - width, 1080/2 - 100)
  w = getTxtButtonWidth("Start Game")
  drawTextButton("difficulty-btn", 1920/2 - width + 20, 1080/2, difficulty.capitalize(), None, w)
  drawTextButton("start-game-btn", 1920/2 - width + 20, 1080/2 + 50, "Start Game")
  if (isButtonClicked("start-game-btn")):
    print("clicked start game")
    global scene
    scene = "intro"
  if (isButtonClicked("difficulty-btn")):
    print("clicked difficulty")
    if (difficulty == "easy"):
      difficulty = "medium"
    elif (difficulty == "medium"):
      difficulty = "hard"
    else:
      difficulty = "easy"
  return