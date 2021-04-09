# pyright: reportMissingImports=false
import threading
import tkinter as tk
from functools import partial

import configs.screen as screen
import configs.constants as constants

from connector import finishAndPay, updateTicketBalance
from components.display import Display
from windows.cart import cartWindow
from wrappers.keypad import lockerWrapper

from utils.pressKey import pressKey
from utils.processCode import processCode
from utils.playSound import playSoundEffect
from utils.errorMessageResolver import errorMessageResolver
from utils.getButtonColor import getButtonColor, getButtonHover

# ***** Note *****
# Over the course of a transaction, there are three levels. The first step is the CODE stage,
# in which the consumer enters the product code from the shelf. Following selection, the system
# advances to stage 2 (AMOUNT), which asks the consumer for an amount of the same commodity.
# Then there's stage 4 (CONFIRM), which requests confirmation from the user before progressing to stage 3.
# Finally, in stage 3 (PAY), the client may choose his or her preferred payment form.

class Keypad(tk.Frame):
  def __init__(self, parent, c):
    tk.Frame.__init__(self, parent, bg="white")
    self.code       = ""
    self.buttons    = screen.BUTTONS
    self.products   = c.products

    # Messages and user inputs are printed on this screen.
    Display(self, c).pack(fill="x")

    # Calculator grid
    self.calculatorView = tk.Frame(self)
    self.calculatorGrid = tk.Frame(self.calculatorView)
    self.calculatorView.pack()
    self.calculatorGrid.grid()

    config = {
            "parent": parent,
        "controller": c,
      "continueIcon": tk.PhotoImage(file="assets/icons/continue.png"),
        "checkImage": tk.PhotoImage(file="assets/icons/tick.png"),
           "payIcon": tk.PhotoImage(file="assets/icons/payIcon.png"),
       "payCashIcon": tk.PhotoImage(file="assets/icons/payCash.png"),
       "payCardIcon": tk.PhotoImage(file="assets/icons/payCard.png"),
        "cancelIcon": tk.PhotoImage(file="assets/icons/cancel.png"),
        "couponIcon": tk.PhotoImage(file="assets/icons/coupon.png")
    }

    @lockerWrapper
    def onSubmit(c):
      playSoundEffect(3)

      # When no code is entered, return to cart window 
      if c.screenMessage.get() == "Enter Code" and c.stage == screen.CODE:
        cartWindow(config)
        return

      # Validate code entered by user for the 3 stages

      # ***** STAGE 1: CODE *****
      if c.stage == screen.CODE:
        code = c.screenMessage.get()
        try:
          screen.BUTTON_CODES[code]
          self.code = code
          c.screenMessage.set("Enter Amount")
          c.stage = screen.AMOUNT
          c.toggleLock(False)
        except KeyError:
          threading.Thread(target=errorMessageResolver, args=(c, "Invalid Code",)).start()
          playSoundEffect(4)

      # ***** STAGE 2: CODE *****
      elif c.stage == screen.AMOUNT:
        amount = c.screenMessage.get()
        if amount.isdigit():
          c.setAmount(int(amount))
          threading.Thread(target=processCode, args=(c, self.code, )).start()
        else:
          threading.Thread(target=errorMessageResolver, args=(c, "Invalid Amount",)).start()
          playSoundEffect(4)

      # ***** STAGE 3: CONFIRM *****
      elif c.stage == screen.CONFIRM:
        # Check if there are enough products to match the client's needs
        if c.selected.quantity.get() - c.amount >= 0:
          # If the product is already in the basket/cart, it should be modified. Otherwise, place the object in your basket.
          try:
            if c.basket[c.selected.id]:
              previous = c.basket[c.selected.id]["price"] * c.basket[c.selected.id]["amount"]
              c.updateSubtotal(previous*-1)
              c.updateSubtotal(c.selected.price.get() * c.amount)

              previousCart = c.basket[c.selected.id]["amount"]
              c.cart.set((c.cart.get()-previousCart) + c.amount)
          except KeyError:
            c.updateSubtotal(c.selected.price.get() * c.amount)
            c.cart.set(c.cart.get() + c.amount)

          # Add product to basket
          c.basket[c.selected.id] = {
                  "id": c.selected.id,
                "name": c.selected.name.get(),
                "price": c.selected.price.get(),
            "quantity": c.selected.quantity.get(),
              "amount": c.amount
          }

          # Reset amount for next purchase
          c.setAmount(0)
          cartWindow(config)
          c.screenMessage.set("Enter Code")

          c.toggleLock(False)
        else:
          # When there is insufficient inventory, display an out of stock message
          threading.Thread(target=errorMessageResolver, args=(c, "Out of Stock",)).start()
          playSoundEffect(4)
          c.toggleLock(False)
        c.stage = screen.CODE

      # ***** STAGE 4: PAY (Cash transaction only) *****
      # Note: Card payments are made directly via the receipt window. Users are not required to enter payment details.
      elif c.stage == screen.PAY_CASH:
        # The server handles all transaction procedures. This involves things like dealing
        # with changes and updating the balance.
        c.toggleLock(True)
        cash = c.screenMessage.get()
        try:
          success = finishAndPay(c, float(cash), "cash")
          if success:
            # The server returns results, which are then edited on the client side.
            response = updateTicketBalance()
            if response["success"]: c.ticketBalance.set(c.ticketBalance.get() + 1)
        except ValueError:
          threading.Thread(target=errorMessageResolver, args=(c, "Invalid Cash",)).start()
          playSoundEffect(4)

    # Generate the buttons on the screen 
    for row in range(len(self.buttons)):
      for col in range(4):
        button = self.buttons[row][col]
        tk.Button(
          self.calculatorGrid,
          command=partial(pressKey, c, parent, button),
          bg=getButtonColor(button),
          fg=constants.BUTTON_TEXT_COLOR,
          font=constants.BUTTON_FONT,
          activebackground=getButtonHover(button),
          activeforeground=constants.BUTTON_TEXT_COLOR,
          state="disabled" if button == "" else "normal",
          width=3,
          height=2,
          text=button,
          cursor="arrow" if button == "" else "hand1",
          padx=10,
          pady=4
        ).grid(row=row, column=col, sticky="news")

    # Continue button
    self.calculator_button = tk.Button(
      self,
      cursor="hand1",
      command=partial(onSubmit, c),
      bg=constants.CALCULATOR_CONFIRM_BUTTON,
      font=constants.CALCULATOR_FONT,
      activebackground=constants.CALCULATOR_HOVER_COLOR,
      activeforeground="white",
      text="Continue",
      height=2,
      fg="white"
    )
    self.calculator_button.pack(fill="x")
