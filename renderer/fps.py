from Processing3 import *

def drawFPS():
  global frames, dFrame, fps
  frames += 1
  if millis() - dFrame > 1000:
    #print(frames)
    fps = frames
    frames = 0
    dFrame = millis()
  fpsColor = (255, 255, 255)
  if fps > 55:
    fpsColor = (0, 255, 0)
  elif fps > 40:
    fpsColor = (255, 255, 0)
  else:
    fpsColor = (255, 0, 0)
  fill(fpsColor[0], fpsColor[1], fpsColor[2])
  textSize(20)
  text("FPS: " + str(fps), 10, 30)

def initFPS():
  global frames, dFrame, fps
  frames = 0
  fps = 0
  dFrame = millis()