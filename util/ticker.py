def update():
  global tick
  tick += 1
  if tick >= 60:
      tick = 0

def isInterval(interval):
  global tick
  return tick % interval == 0

def getTick():
  global tick
  return tick