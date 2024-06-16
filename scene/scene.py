from scene.game import *
from scene.intro import *
from scene.blank import *
from scene.end import *
from scene.main import *
from util.audio import *
def drawScene():
  scenes = {
    "intro": {
      "setup": setupIntro,
      "main": drawIntro,
      "cleanup": cleanupIntro
    },
    "game": {
      "setup": setupGame,
      "main": drawGame,
      "cleanup": cleanupGame
    },
    "blank": {
      "setup": setupBlank,
      "main": drawBlank,
      "cleanup": cleanupBlank
    },
    "end": {
      "setup": setupEnd,
      "main": drawEnd,
      "cleanup": cleanupEnd
    },
    "main": {
      "setup": setupMain,
      "main": drawMain,
      "cleanup": cleanupMain
    }
  }
  global scene, lastScene, level_audio, meme_muted
  if scene != lastScene:
    scenes[scene]["setup"]()
    if not meme_muted and level_audio != None:
      playAudio(level_audio).loop()
    if lastScene != "dummy": # cleanup previous scene
      if level_audio != None:
        stopAudio(level_audio)
      scenes[lastScene]["cleanup"]()
    lastScene = scene
    global humans, calc_paths
    humans = {}
    calc_paths = []
  scenes[scene]["main"]()
  if (level_audio != None):
    renderKey(width - 140, height - 50 - getKeyOffset(), "m", meme_muted)
    textSize(16)
    fill(0)
    text("Meme On" if meme_muted else "Meme Off", width - 100, height - 50)
    if (isKeyTyped("m")):
      meme_muted = not meme_muted
      if meme_muted:
        stopAudio(level_audio)
      else:
        playAudio(level_audio).loop()
  return