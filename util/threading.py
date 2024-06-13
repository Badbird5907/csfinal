from java.lang import Thread #!compiler_ignore

def sleep(ms):
  Thread.sleep(ms)

# execute a function every x milliseconds
def setInterval(func, ms, name = "interval"):
  global tid, runningTids
  tid += 1
  def wrapper():
    while True:
      global tid, runningTids
      if tid in runningTids:
        func()
        sleep(ms)
      else:
        break
  Thread(wrapper, name).start()
  runningTids.append(tid)
  return tid

def killThread(tid):
  # thread.interrupt()
  global runningTids
  runningTids.remove(tid)

def getThreadName():
  return Thread.currentThread().getName()
