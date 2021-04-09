from time import sleep

def loading(c):
  c.toggleLock(True)
  for i in range(3):
    c.screenMessage.set("Processing" + (i+1)*".")
    sleep(0.2)
  c.toggleLock(False)

def blink(c, text):
  c.toggleLock(True)
  for _ in range(3):
    c.screenMessage.set(str(text))
    sleep(0.3)
    c.screenMessage.set("")
    sleep(0.2)
  c.screenMessage.set(text)
  c.toggleLock(False)
