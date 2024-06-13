from Processing3 import * # __cwd__

from java.lang import ProcessBuilder #!compiler_ignore

def playBrainRot(video, left = -1, top = -1):
  moreargs = ""
  if not left == -1:
    moreargs += " -left " + str(left)
  if not top == -1:
    moreargs += " -top " + str(top)
  cwd = __cwd__.replace("\\", "/")
  if cwd[-1] == ".": cwd = cwd[:-1] # remove weird edge case??
  # read ps1 and concatenate every line with ; to get around the script execution policy
  with open(cwd + "/assets/brainrot.ps1", "r") as f:
    cmd = f.readlines()
    cmd = ";".join(cmd)
  cmd = cmd.replace("%cwd%", cwd).replace("%vid%", video).replace("%moreargs%", moreargs)
  print(cmd)
  # execute the ps1 script
  args = [ "powershell.exe","-Command",cmd]
  ProcessBuilder(args).inheritIO().start()