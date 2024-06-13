from Processing3 import *
from util.threading import *


def tickScore():
  global st_func, score
  score = st_func()
  return
def setupScoreTracker(func):
  global st_thread, st_func
  st_func = func
  st_thread = setInterval(tickScore, 50, "scoreTracker")

def cleanupScoreTracker():
  global st_thread
  killThread(st_thread)

def drawScore():
  global score
  # draw score on top right of the screen
  fill(0)
  textSize(30)
  txt = "Score: " + str(score)
  text(txt, width - (textWidth(txt) + 10), 30)
  return