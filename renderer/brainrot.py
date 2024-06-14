from Processing3 import * # __cwd__

from java.lang import ProcessBuilder #!compiler_ignore
from java.net import URL #!compiler_ignore
from java.io import File, BufferedInputStream #!compiler_ignore
import hashlib
import os


def processPowershellScript(path):
  cwd = __cwd__.replace("\\", "/")
  if cwd[-1] == ".": cwd = cwd[:-1] # remove weird edge case??
  # read ps1 and concatenate every line with ; to get around the script execution policy
  with open(cwd + path, "r") as f:
    cmd = f.readlines()
    cmd = ";".join(cmd)
  cmd = cmd.replace("%cwd%", cwd)
  return cmd

def execCmd(cmd):
  args = [ "powershell.exe","-Command",cmd]
  #print("Executing: " + " ".join(args))
  return ProcessBuilder(args).inheritIO().start()

def download(url, path, sha256 = None):
  cmd = processPowershellScript("/assets/dl.ps1")
  cmd = cmd.replace("%url%", url).replace("%output%", path)
  if sha256 == None:
    cmd = cmd.replace("%sha256%", "")
  else:
    cmd = cmd.replace("%sha256%", sha256)
  execCmd(cmd).waitFor()
def playBrainRot(video, left = -1, top = -1):
  ffplay_sha256 = "BD8F20BB9E6F966F23DAA9AFD4D4C731D14DD25CA677027188A1F39AE74242A9"
  # check if assets/ffplay.exe exists
  if not os.path.exists(__cwd__ + "/assets/ffplay.exe"):
    print("ffplay.exe not found, downloading...")
    download("https://cdn.badbird.dev/assets/brainrot/ffplay.exe", __cwd__ + "/assets/ffplay.exe", ffplay_sha256)
  moreargs = ""
  if not left == -1:
    moreargs += " -left " + str(left)
  if not top == -1:
    moreargs += " -top " + str(top)
  cmd = processPowershellScript("/assets/brainrot.ps1").replace("%vid%", video).replace("%moreargs%", moreargs)
  execCmd(cmd)
  