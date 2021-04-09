# pyright: reportMissingImports=false
import configs.screen as screen
from utils.loader import loading

# Determine the product from the code and show it on the screen
def processCode(c, code):
  products = c.products

  loading(c)
  # Get product using the code from user
  selected = products[screen.BUTTON_CODES[code]]
  # Confirmation text
  c.screenMessage.set(selected.name.get() + "\n" + "Continue?")
  c.setSelected(selected)
  c.stage = screen.CONFIRM
