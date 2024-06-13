from Processing3 import *

#from animate.easings import *

def initToastRenderer():
  global toastEdge, toastMiddle
  toastEdge = loadImage("assets/btn_edge.png")
  toastMiddle = loadImage("assets/btn_middle.png")
  global toasts
  toasts = []
  return

def createToast(text, duration):
  global toasts
  start = millis()
  end = start + duration
  toasts.append({"text": text, "duration": duration, "start": start, "end": end })
  return

def drawToasts():
  global toasts
  for t in toasts:
    if millis() > t["end"]:
      toasts.remove(t)
      continue
    drawToast(t["text"], millis() - t["start"], t["duration"])



def drawToast(txt, time, duration):
  global toastEdge, toastMiddle
  middle_length = 64
  textSize(20)
  txtSize = textWidth(txt)
  w = txtSize + 40
  numMiddle = int(w // middle_length) - 1
  # draw like <edge>[middle][middle]<edge>
  # <edge> is toastEdge
  # [middle] is toastMiddle
  # <edge> is toastEdge
  # draw first edge first
  x = (width - w) / 2
  y = height - 100
  fade = 255
  if time > duration - 500: # fade out
    fade = map(time, duration - 500, duration, 255, 0)
  elif time < 500: # fade in
    fade = map(time, 0, 500, 0, 255)
  tint(255, fade)
  image(toastEdge, x, y)
  x += toastEdge.width
  for i in range(numMiddle):
    image(toastMiddle, x, y)
    x += toastMiddle.width
  x += toastMiddle.width
  # draw toastEdge but flipped
  pushMatrix()
  translate(x - 1, y)
  scale(-1, 1)
  image(toastEdge, 0, 0)
  popMatrix()
  fill(255)
  text(txt, ((width - txtSize) / 2) + 15, height - 60)
  tint(255, 255)
  return

