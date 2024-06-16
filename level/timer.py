from Processing3 import *
from util.audio import *

def initTimer(seconds, endFunc):
  global timer_seconds, timer_end, timer_end_func, clock_played
  timer_seconds = seconds
  timer_end = millis() + timer_seconds * 1000
  timer_end_func = endFunc
  clock_played = millis()
  return
def padZero(num):
  if (num < 10):
    return "0" + str(num)
  return str(num)

def drawTimer():
  global timer_seconds, timer_end, timer_end_func, clock_played
  timer_seconds = (timer_end - millis()) // 1000
  if (timer_seconds < 0):
    timer_seconds = 0
    if (timer_end_func):
      timer_end_func()
      timer_end_func = None
  fill(0)
  textSize(30)
  minutes = timer_seconds // 60
  seconds = timer_seconds % 60
  if (minutes == 0):
    if (seconds < 10):
      if (seconds % 2 == 0 or seconds == 0):
        fill(255,0,0)
      if (seconds == 0):
        stopAudio("clock_1")
    if (seconds == 10 and millis() - clock_played > 1100):
      playAudio("clock_1")
      clock_played = millis()
  txt = padZero(minutes) + ":" + padZero(seconds)
  # draw this on the center top of the screen
  text(txt, width // 2 - textWidth(txt) // 2, 30)
  return