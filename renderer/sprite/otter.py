from Processing3 import *
from util.ticker import *

def initOtter():
  idle_anims = 4 # 1-4
  idle_alt_anims = 9 # 1-11
  sleep_anims = 6 # 1-6
  run_anims = 3 # 1-3
  global idle_imgs, current_img, idle_state
  global sleep_imgs, sleep_state, otter_state
  global run_imgs, run_state
  current_img = None
  idle_state = 0
  sleep_state = 0
  otter_state = "idle"
  run_state = 0

  idle_imgs = []
  for i in range(idle_anims):
    idle_imgs.append(loadImage("assets/otter/otter_idle_" + str(i + 1) + ".png"))
  for i in range(idle_alt_anims):
    idle_imgs.append(loadImage("assets/otter/otter_idle_alt_" + str(i + 1) + ".png"))
  
  sleep_imgs = []
  for i in range(sleep_anims):
    sleep_imgs.append(loadImage("assets/otter/otter_sleep_" + str(i + 1) + ".png"))

  run_imgs = []
  for i in range(run_anims):
    run_imgs.append(loadImage("assets/otter/otter_run_" + str(i + 1) + ".png"))

def drawImage(img, x, y):
  global facing, otter_scale, pbbMax, last_atk
  w = img.width * otter_scale
  h = img.height * otter_scale
  pbbMax = (w, h)
  # show hurt (tint red) for 250ms if last_atk is less than 250ms ago
  if millis() - last_atk < 250:
    tint(255, 0, 0)
  else:
    noTint()
  if facing == "front":
    image(img, x, y, w, h)
  elif facing == "back":
    pushMatrix()
    translate(w + x, 0)
    scale(-1, 1)
    image(img, 0, y, w, h)
    popMatrix()
  elif facing == "up":
    # rotate 90 degrees
    pushMatrix()
    translate(x, y + h)
    rotate(-PI / 2)
    image(img, 0, 0, w, h)
    popMatrix()
  elif facing == "down":
    # rotate 90 degrees
    pushMatrix()
    translate(x + w, y)
    rotate(PI / 2)
    image(img, 0, 0, w, h)
    popMatrix()

  global debug_bb
  if debug_bb:
    # bounding box
    stroke(255, 0, 0)
    noFill()
    rect(x, y, w, h)
    # draw a circle at the actual point (x,y)
    fill(255, 0, 0)
    ellipse(x, y, 10, 10)
  
  noTint()


def drawIdle(x,y):
  global idle_imgs, current_img, idle_state, last_input, facing
  if facing == "up" or facing == "down":
    facing = "front"

  # if the last input is over 10 seconds ago, switch to sleep
  if millis() - last_input > 10000:
    global sleep_rand_last
    sleep_rand_last = millis()
    drawSleep(x,y)
    return

  if isInterval(20) or current_img == None:
    idle_state += 1
    if idle_state >= len(idle_imgs) - 1:
      idle_state = 0
    current_img = idle_imgs[idle_state]
  drawImage(current_img, x, y)
  return

def drawSleep(x,y):
  global sleep_imgs, current_img, sleep_state, sleep_rand_last

  # every 30 seconds, randomly switch to idle
  if millis() - sleep_rand_last > 15000:
    global last_input
    last_input = millis()
    drawIdle(x,y)
    return
  
  if isInterval(20) or current_img == None:
    sleep_state += 1
    if sleep_state >= len(sleep_imgs) - 1:
      sleep_state = 0
    current_img = sleep_imgs[sleep_state]
  drawImage(current_img, x, y)
  return

def drawRun(x,y):
  global run_imgs, current_img, run_state

  if isInterval(10) or current_img == None:
    run_state += 1
    if run_state >= len(run_imgs) - 1:
      run_state = 0
    current_img = run_imgs[run_state]
  drawImage(current_img, x, y)
  return

def drawOtter(x,y, scale): # scale = 0-1 (0.5 is half size, 1 is full size)
  global otter_state, otter_scale
  otter_scale = scale

  if otter_state == "idle":
    drawIdle(x,y)
  elif otter_state == "run":
    drawRun(x,y)
