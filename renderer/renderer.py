from renderer.sprite.otter import *
from renderer.fps import *
from renderer.button import *
from renderer.key import *
from renderer.human import *
from renderer.toast import *

def setupRenderers():
  initOtter()
  initFPS()
  initButtonRenderer()
  initKeyRenderer()
  initHumanRenderer()
  initToastRenderer()
  return