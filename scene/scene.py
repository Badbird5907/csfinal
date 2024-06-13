from scene.game import *
from scene.intro import *
from scene.blank import *
from scene.end import *
from scene.main import *
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
  global scene, lastScene
  if scene != lastScene:
    scenes[scene]["setup"]()
    # cleanup previous scene
    if lastScene != "dummy":
      scenes[lastScene]["cleanup"]()
    lastScene = scene
    global humans, calc_paths
    humans = {}
    calc_paths = []
  scenes[scene]["main"]()
  return