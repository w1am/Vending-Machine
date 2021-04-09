import tkinter as tk

import configs.constants as constants
from tinydb import TinyDB, Query

from components.product import ProductList, ProductItem
from components.balance import Balance
from components.keypad import Keypad
from components.toolbar import Toolbar
from utils.typewriter import typerwriter

import configs.screen as screen

productDB = TinyDB("database/product.json")
accountDB = TinyDB("database/account.json")

sounds = {
  1: "assets/sounds/clear.wav",
  2: "assets/sounds/click.wav",
  3: "assets/sounds/chime.wav",
  4: "assets/sounds/fail.wav",
  5: "assets/sounds/coin.wav",
  6: "assets/sounds/receipt.wav"
}

#  ------- Controller -------
class Controller(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.container = tk.Frame(self, bg=constants.BACKGROUND_COLOR)
    self.container.pack()

    coinBalance = accountDB.get(Query().id == 1)["balance"]
    ticketBalance = accountDB.get(Query().id == 1)["lotteryTickets"]

    self.products = []

    self.selected = None
    self.amount   = 0
    self.subtotal = tk.DoubleVar(self.container, 0)
    self.basket   = {}
    self.stage = screen.CODE

    self.coin         = tk.PhotoImage(file="assets/icons/coin.png")
    self.ticket       = tk.PhotoImage(file="assets/icons/ticket.png")
    self.chartImage   = tk.PhotoImage(file="assets/icons/chart.png")
    self.productImage = tk.PhotoImage(file="assets/icons/product.png")
    self.lotteryImage = tk.PhotoImage(file="assets/icons/lottery.png")

    self.cart          = tk.IntVar(self.container, 0)
    self.coinBalance   = tk.DoubleVar(self.container, coinBalance)
    self.ticketBalance = tk.IntVar(self.container, ticketBalance)
    self.screenMessage = tk.StringVar(self.container, "")

    self.locked = False
    self.coupon = None

    # Start with a welcome message
    typerwriter(self, ["Welcome to the\nvending machine"])

    for product in productDB.all():
      self.products.append(ProductItem(
        self,
        product.doc_id,
        product["name"],
        product["image"],
        product["quantity"],
        product["price"]
      ))

    self.productList = ProductList(self.container, self)
    self.productList.pack(side="left", expand=1, fill="both", padx=(0, 4))

    self.display = tk.Frame(self.container, bg="white")
    self.display.pack(side="right", expand=1, fill="both", padx=(4, 0))

    self.balance = Balance(self.display, self)
    self.balance.pack(pady=(8,0), padx=8, fill="x")

    self.keypad = Keypad(self.display, self,)
    self.keypad.pack(fill="x", padx=8, pady=8)
    self.toolbar = Toolbar(self.display, self)

  # Update subtotal
  def updateSubtotal(self, new): self.subtotal.set(round(self.subtotal.get() + new, 2))

  # Number of the same product 
  def setAmount(self, new): self.amount = int(new)

  # Save current product choice
  def setSelected(self, new): self.selected = new

  # Lock keypad
  def toggleLock(self, state): self.locked = state

def main():
  root = Controller()
  root.title("Vending Machine")
  # Set default font to Helvetica
  root.option_add("*Font", "Helvetica")
  # Deisable resize
  root.resizable(False,False)
  root.configure(bg=constants.BACKGROUND_COLOR)
  root.configure(pady=8, padx=8)
  root.mainloop()

if __name__ == "__main__":
  main()
