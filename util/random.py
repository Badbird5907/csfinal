from java.util import Random #!compiler_ignore

def randInt(min, max):
  return Random().nextInt(max - min) + min

def randFloat(min, max):
  return Random().nextFloat() * (max - min) + min

def randArr(arr):
  return arr[randInt(0, len(arr))]

def rd():
  return Random().nextFloat()