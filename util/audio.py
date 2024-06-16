add_library('minim')

def loadAudio(file):
  global audioCache, minim
  if False:
    return minim.loadFile("assets/audio/" + file + ".mp3")
  if file not in audioCache: # broken??
    audioCache[file] = minim.loadFile("assets/audio/" + file + ".mp3")
  return audioCache[file]
def initAudio():
  global audioCache, minim
  audioCache = {}
  minim = Minim(this)
  audiofiles = ["vine-boom", "rick", "splash_in", "clock_1", "grass"]
  for file in audiofiles:
    loadAudio(file)

def playAudio(file):
  audio = loadAudio(file)
  audio.rewind()
  audio.play()
  return audio

def stopAudio(file):
  audio = loadAudio(file)
  audio.pause()
  return audio