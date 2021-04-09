import tkinter as tk

class Balance(tk.Frame):
  def __init__(self, parent, c):
    tk.Frame.__init__(self, parent, height=20, bg="white")

    # Coin balance
    self.balanceFrame = tk.Frame(self, height=20, width=70, bg="white")
    self.balanceFrame.pack(pady=(0, 4), side="right")

    tk.Label(self.balanceFrame, image=c.coin, bg="white").pack(side="left")
    tk.Label(self.balanceFrame, textvariable=c.coinBalance, bg="white").pack(side="right")

    # Lottery ticket balance
    self.ticketFrame = tk.Frame(self, height=20, width=70, bg="white")
    self.ticketFrame.pack(pady=(0, 4), side="left")

    tk.Label(self.ticketFrame, image=c.ticket, bg="white").pack(side="left")
    tk.Label(self.ticketFrame, textvariable=c.ticketBalance, bg="white").pack(side="right")
