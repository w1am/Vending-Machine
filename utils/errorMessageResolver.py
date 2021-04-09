# pyright: reportMissingImports=false
import configs.screen as screen
from utils.loader import blink

# This procedure is called if an error occurs. For instance, an out-of-stock error,
# an  number error, or a button error.
def errorMessageResolver(c, message):
  subtotal = c.subtotal.get()
  discount = round(subtotal * (int(c.coupon["coupon"][4:]) / 100) if c.coupon else 0, 2)
  charge = round(subtotal - discount, 2)
  blink(c, message)
  if c.stage == screen.CODE: c.screenMessage.set("Enter Code")
  if c.stage == screen.AMOUNT: c.screenMessage.set("Enter Amount")
  if c.stage == screen.PAY_CASH: c.screenMessage.set(f"Please Insert Cash\n${str(charge)}")
