# pyright: reportMissingImports=false
import tkinter as tk
import configs.constants as constants

# Field class
class Number(tk.Label):
  def __init__(self, parent, *args, **kwargs):
    tk.Label.__init__(
      self,
      parent,
      fg=constants.SCREEN_LABEL,
      bg=constants.SCREEN_BG,
      font=constants.BASKET_FONT,
      *args,
      **kwargs
    )

class Display(tk.Frame):
  def __init__(self, parent, c):
    tk.Frame.__init__(self, parent, bg="#373C40", padx=8, pady=8)
    # Screen shadow
    tk.Frame(self, bg="#8A9986", height=5).pack(fill="x")

    # Basket screen numbers
    self.basketFrame = tk.Frame(self, bg="#A6B8A2")
    self.basketFrame.pack(fill="x")
    Number(self.basketFrame, text="Cart:").pack(side="left", anchor="w", padx=(4, 0))
    Number(self.basketFrame, textvariable=c.cart).pack(side="left", anchor="e")

    Number(self.basketFrame, textvariable=c.subtotal).pack(side="right", anchor="e", padx=(0, 4))
    Number(self.basketFrame, text="Subtotal: $").pack(side="right", anchor="w")

    # Main screen numbers
    self.indicator = tk.Label(
      self,
      fg=constants.SCREEN_LABEL,
      bg=constants.SCREEN_BG,
      font=constants.SCREEN_FONT,
      textvariable=c.screenMessage,
      justify="center",
      height=4, width=14,
      border=4
    )
    self.indicator.pack(fill="x")
