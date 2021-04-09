# pyright: reportMissingImports=false
from time import sleep
import threading
from utils.loader import blink 

def typerwriter(c, messages):
  def startType():
    c.screenMessage.set("")
    c.toggleLock(True)
    for message in messages:
      for char in message:
        c.screenMessage.set(c.screenMessage.get() + char)
        sleep(0.08)
      if len(messages) > 0: sleep(1)
      c.screenMessage.set("")
    blink(c, messages[-1])
    sleep(1)
    c.screenMessage.set("Enter Code")
    c.toggleLock(False)
  threading.Thread(target=startType).start()
