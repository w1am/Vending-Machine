# pyright: reportMissingImports=false
import configs.constants as constants
import configs.screen as screen

def getButtonColor(button):
  if button == screen.CLEAR:
    return constants.BUTTON_CLEAR_COLOR
  elif button == screen.HELP:
    return constants.HELP_CLEAR_COLOR
  else:
    return constants.BUTTON_DEFAULT_COLOR

def getButtonHover(button):
  if button == screen.CLEAR:
    return constants.BUTTON_CLEAR_HOVER
  elif button == screen.HELP:
    return constants.HELP_CLEAR_HOVER
  else:
    return constants.BUTTON_DEFAULT_HOVER
