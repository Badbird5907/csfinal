def easeOutExpo(x):
  return 1 - pow(2, -10 * x)

def easeInExpo(x):
  return pow(2, 10 * (x - 1))

def easeOutQuad(x):
  return 1 - (1 - x) * (1 - x)

def easeInOutQuad(x):
  if x < 0.5:
    return 2 * x * x
  else:
    return 1 - pow(-2 * x + 2, 2) / 2