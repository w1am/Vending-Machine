import threading
from playsound import playsound

sounds = {
  1: "assets/sounds/clear.wav",
  2: "assets/sounds/click.wav",
  3: "assets/sounds/chime.wav",
  4: "assets/sounds/fail.wav",
  5: "assets/sounds/coin.wav",
  6: "assets/sounds/receipt.wav",
  7: "assets/sounds/tick.wav",
  8: "assets/sounds/win.wav"
}

def playSoundEffect(choice):
  def play():
    playsound(sounds[choice])
  threading.Thread(target=play).start()
