# pyright: reportMissingImports=false
import tkinter as tk
from random import randint
from time import sleep
import threading
from playsound import playsound
from tinydb import TinyDB, Query
from tinydb.operations import decrement
from connector import updateAccountBalance

from utils.playSound import playSoundEffect

import configs.constants as constants
from connector import generateCoupon

accountDB = TinyDB("database/account.json")
couponDB = TinyDB("database/coupon.json")

def lotteryWindow(parent, c):
  newWindow = tk.Toplevel(parent)
  newWindow.title("Lottery")
  newWindow.resizable(False, False)
  newWindow.configure(background="white")

  # Lottery result control variable
  lotteryResult = tk.IntVar(newWindow, 0)

  # Ticket balance
  ticketFrame = tk.Frame(newWindow, height=20, width=70, bg="white")
  ticketFrame.pack(pady=10, padx=10, anchor="e")
  tk.Label(ticketFrame, image=c.ticket, bg="white").pack(side="left")
  tk.Label(ticketFrame, textvariable=c.ticketBalance, bg="white").pack(side="right")

  frame = tk.Frame(newWindow, bg="#373C40", padx=8, pady=8)
  frame.pack(fill="x")

  grid = tk.Frame(frame, bg="white")
  grid.grid(sticky="news")

  # When the lottery is drawn, highlight the current / active frame
  highlight = "#FFCC4D"

  # Lottery result
  lotteryOutput = tk.StringVar(newWindow, "Click play to start")

  # Default frame color
  contrasts = ["#C45DDD", "#57B8FF", "#FF6666", "#24FE3A", "#6B71FF"]

  # Lottery frames
  panes = [
    tk.Label(grid, bg=contrasts[0], height=12, width=12, text="", font="Helvetica 11 bold", fg="white"),
    tk.Label(grid, bg=contrasts[1], height=12, width=12, text="", font="Helvetica 11 bold", fg="white"),
    tk.Label(grid, bg=contrasts[2], height=12, width=12, text="", font="Helvetica 11 bold", fg="white"),
    tk.Label(grid, bg=contrasts[3], height=12, width=12, text="", font="Helvetica 11 bold", fg="white"),
    tk.Label(grid, bg=contrasts[4], height=12, width=12, text="", font="Helvetica 11 bold", fg="white")
  ]

  # Lottery winnings
  lotteries = ["a\nCoupon", "a\nFree Burger", "75\nCoins", "a\nCoupon", "20 Coins"]

  # Draw lottery frames
  for i in range(len(panes)):
    panes[i].grid(row=0, column=i)

  # Lottery sound effects
  def playSound(): playsound("assets/sounds/tick.wav")
  def playWin(): playsound("assets/sounds/win.wav")

  # Valudate lottery winnings and redeem rewards
  def validateLottery(result):
    if result == 0:
      generateCoupon(25)
    elif result == 1:
      print("Here is your free burger")
    elif result == 2:
      newBalance = c.coinBalance.get() + 5
      updateAccountBalance(c, newBalance)
    elif result == 3:
      generateCoupon(10)
    elif result == 4:
      newBalance = c.coinBalance.get() + 15
      updateAccountBalance(c, newBalance)

  # Animate the lottery as it is spinning
  def animate(delay, result):
    for x in range(5):
      lotteryResult.set(int(result))
      panes[x].configure(bg=highlight)
      # Play tick sound
      playSoundEffect(7)
      sleep(delay)
      # Highlight current pane
      panes[x].configure(bg=contrasts[x])

  def spin():
    panes[lotteryResult.get()].configure(text="")
    # Randomize lottery winning
    result = randint(0, 4)

    # Spin
    for _ in range(4): animate(0.02, result)
    for _ in range(2): animate(0.1, result)
    for _ in range(1): animate(0.3, result)
    for _ in range(result): animate(0.3, result)

    # After the lottery is drawn, highlight the current frame
    panes[lotteryResult.get()].configure(bg=highlight)

    # Display lottery winning
    playSoundEffect(8)
    panes[lotteryResult.get()].configure(text=str(lotteries[lotteryResult.get()]))
    lotteryOutput.set(f"You just won {lotteries[lotteryResult.get()]}")
    validateLottery(result)

  # When a user clicks the play button, one ticket is deducted
  def spendLotteryTicket():
    if c.ticketBalance.get() > 0:
      playSoundEffect(7)
      sleep(1)
      c.ticketBalance.set(c.ticketBalance.get() - 1)
      accountDB.update(decrement("lotteryTickets"), Query().id == 1)
      threading.Thread(target=spin).start()

  # Prize Header
  tk.Label(newWindow, text="Prize", bg="white", fg="red", font=("Helvetica 20 bold")).pack(pady=(10, 0))

  # Prize
  tk.Label(
    newWindow,
    textvariable=lotteryOutput,
    bg="white",
    font=("Helvetica 20 bold"),
    fg=constants.TEXT_COLOR
  ).pack(expand=True, fill="both")

  # Play button
  tk.Button(
    newWindow,
    command=spendLotteryTicket,
    text="Play Lottery",
    bg=constants.SKY_BG, activebackground=constants.SKY_HOVER, fg="white",
    activeforeground="white",
    font=constants.COPY_FONT,
    height=1, pady=10, bd=0,
    cursor="hand1",
  ).pack(fill="x", side="bottom")

  newWindow.transient(parent)
  newWindow.grab_set()
