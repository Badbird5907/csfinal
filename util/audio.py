add_library('minim')

def loadAudio(file):
  global audioCache, minim
  if True:
    return minim.loadFile("assets/audio/" + file + ".mp3")
  if file not in audioCache: # broken??
    audioCache[file] = minim.loadFile("assets/audio/" + file + ".mp3")
  return audioCache[file]
def initAudio():
  global audioCache, minim
  audioCache = {}
  minim = Minim(this)
  loadAudio("vine-boom")
  print(this)

def playAudio(file):
  audio = loadAudio(file)
  audio.play()