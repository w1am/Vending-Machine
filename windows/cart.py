# pyright: reportMissingImports=false
import tkinter as tk
from utils.typewriter import typerwriter
from windows.receipt import receiptWindow
from windows.coupon import couponWindow
from functools import partial
from tinydb import TinyDB

import configs.constants as constants

accountDB  = TinyDB("database/account.json")

messages = [
  "Sorry, we could not\nprovide you with\nyour choice today",
  "We hope to see\nyou soon again :)",
  "Have a good day!"
]

# Cart button class
class CartButton(tk.Button):
  def __init__(self, parent, *args, **kwargs):
    tk.Button.__init__(
      self,
      parent,
      fg=constants.BUTTON_LABEL,
      activeforeground=constants.BUTTON_LABEL,
      font=constants.COPY_FONT,
      cursor="hand1",
      bd=0,
      relief="flat",
      borderwidth=0,
      pady=10,
      compound="top",
      *args,
      **kwargs
    )

def cartWindow(config):
  c            = config["controller"]
  parent       = config["parent"]
  payIcon      = config["payIcon"]
  cancelIcon   = config["cancelIcon"]
  continueIcon = config["continueIcon"]
  couponIcon   = config["couponIcon"]

  newWindow = tk.Toplevel(parent)
  newWindow.title("Cart")
  newWindow.resizable(False, False)
  newWindow.geometry("660x470")
  newWindow.configure(background="white")

  # Sidebar
  sidebar = tk.Frame(newWindow, bg=constants.SIDEBAR_BG, padx=8, pady=10)
  sidebar.pack(side="left", fill="y")

  # Cart Header
  tk.Label(sidebar, fg=constants.TEXT_COLOR, bg=constants.SIDEBAR_BG, text="Cart", font=constants.HEADER, width=12).pack(pady=(0, 10))

  # Subtotal Header
  tk.Label(
    sidebar,
    fg=constants.TEXT_COLOR,
    font="Helvetica 12 bold",
    text=str(f"Subtotal: ${round(c.subtotal.get(), 2)}"),
    anchor="w",
    width=12,
    bg=constants.SIDEBAR_BG
  ).pack(side="bottom", fill="both")

  # Cart items
  if c.basket == {}:
    tk.Label(sidebar, text="Your cart is\ncurrently empty", bg=constants.SIDEBAR_BG, fg=constants.CART_FONT).pack(expand=True)
  else:
    for product in c.basket.values():
      cartItemFrame = tk.Frame(sidebar, bg=constants.SIDEBAR_BG)
      cartItemFrame.pack(fill="x", pady=(0, 2))

      infoFrame = tk.Frame(cartItemFrame, bg=constants.SIDEBAR_BG)
      infoFrame.pack(side="left")
      
      amountFrame = tk.Frame(cartItemFrame, bg=constants.SIDEBAR_BG)
      amountFrame.pack(side="right")

      tk.Label(infoFrame, bg=constants.SIDEBAR_BG, text=product["name"], anchor="w", font="Helvetica 10 bold").pack(fill="both")
      tk.Label(infoFrame, bg=constants.SIDEBAR_BG, text=str(f"${round(product['price'], 2)}"), anchor="w").pack(fill="both")

      tk.Label(amountFrame, text=str(f"x{product['amount']}"), bg=constants.SIDEBAR_BG).pack()

  # Buttons frame
  buttonsFrame = tk.Frame(newWindow, bg="white")
  buttonsFrame.pack(fill="both", expand=True, side="right")

  # Top Frame
  top = tk.Frame(buttonsFrame)
  top.pack(fill="both", expand=True)

  # Bottom Frame
  bottom = tk.Frame(buttonsFrame)
  bottom.pack(fill="both", expand=True)

  # Reset cart states on cancel
  def cancel():
    # When a user cancels an event, a farewell message is shown.
    if c.cart.get() > 0:
      typerwriter(c, messages)

      c.basket = {}
      c.subtotal.set(0)
      c.cart.set(0)
      c.coupon = None

    newWindow.destroy()
    newWindow.update()

  # When the user clicks the pay button, a receipt window opens
  def pay():
    receiptWindow(config, parent, c)
    newWindow.destroy()
    newWindow.update()

  # Destroy the current window and enable the user to continue shopping
  def addAnother():
    newWindow.destroy()
    newWindow.update()

  # Add another button
  CartButton(
    top,
    text="Add Another",
    command=addAnother,
    bg=constants.ADD_ANOTHER_BG,
    activebackground=constants.ADD_ANOTHER_HOVER,
    image=continueIcon
  ).pack(side="left", fill="both", expand=True)

  # Finish and Pay button
  CartButton(
    top,
    text="Finish and Pay",
    command=pay,
    bg=constants.PAY_BUTTON_BG,
    activebackground=constants.PAY_BUTTON_HOVER,
    image=payIcon
  ).pack(side="right", fill="both", expand=True)

  # Cancel Button
  CartButton(
    bottom,
    command=cancel,
    text="Cancel",
    bg=constants.CANCEL_BG,
    activebackground=constants.CANCEL_HOVER,
    image=cancelIcon
  ).pack(fill="both", expand=True)

  # Coupon Button
  CartButton(
    bottom,
    command=partial(couponWindow, newWindow, c),
    text="Apply Coupon Code",
    bg=constants.COUPON_BTN_BG,
    activebackground=constants.COUPON_BTN_HOVER,
    image=couponIcon
  ).pack(fill="both", expand=True)

  newWindow.transient(parent)
  newWindow.grab_set()
