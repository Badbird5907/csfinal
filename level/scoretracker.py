from Processing3 import *
from util.threading import *


def tickScore():
  global st_func, score
  score = st_func()
  return
def setupScoreTracker(func):
  global st_thread, st_func, heart_img
  st_func = func
  st_thread = setInterval(tickScore, 50, "scoreTracker")
  heart_img = loadImage("assets/heart.png")

def cleanupScoreTracker():
  global st_thread
  killThread(st_thread)

def drawScore():
  global score, heart_img, hp
  # draw score on top right of the screen
  fill(0)
  textSize(20)
  txt = "Score: " + str(score)
  tw = textWidth(txt)
  text(txt, width - (tw + 10), 30)

  heart_height = 32
  heart_width = 32
  hp_txt = str(hp)
  if (hp <= 3):
    fill(255, 0, 0)
  text(hp_txt, width - (tw - 25), 60)
  image(heart_img, width - (tw - 25) - heart_width - 5, 35, heart_width, heart_height)
  fill(0)
  return