# pyright: reportMissingImports=false
import tkinter as tk
from functools import partial
import configs.constants as constants
from windows.inventory import inventoryWindow
from windows.product import productsWindow
from windows.lottery import lotteryWindow

# Toolbar button class for re-use
class ToolbarButton(tk.Button):
  def __init__(self, parent, *args, **kwargs):
    tk.Button.__init__(
      self,
      parent,
      border=0,
      cursor="hand1",
      pady=8,
      fg="white",
      activeforeground="white",
      compound="left",
      *args,
      **kwargs
    )

class Toolbar:
  def __init__(self, parent, c):
    self.container = tk.Frame(parent, height=20, bg="white")
    self.container.pack(pady=(8,0), padx=8, fill="x")
 
    # Inventory button
    ToolbarButton(
      self.container,
      text="Inventory",
      command=partial(inventoryWindow, parent),
      image=c.chartImage,
      bg=constants.INVENTORY_BG,
      activebackground=constants.INVENTORY_HOVER,
    ).pack(fill="x", pady=(0, 4))
 
    # Products button
    ToolbarButton(
      self.container,
      text="Products",
      command=partial(productsWindow, c, parent),
      image=c.productImage,
      bg=constants.PRODUCTS_BG,
      activebackground=constants.PRODUCTS_HOVER,
    ).pack(fill="x", pady=(0, 4))

    # Lottery button
    ToolbarButton(
      self.container,
      text="Lottery",
      command=partial(lotteryWindow, parent, c),
      image=c.lotteryImage,
      bg=constants.LOTTERY_BG,
      activebackground=constants.LOTTERY_HOVER,
    ).pack(fill="x", pady=(0, 4))
