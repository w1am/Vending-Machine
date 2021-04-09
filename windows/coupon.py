# pyright: reportMissingImports=false
import tkinter as tk
from time import sleep
from datetime import datetime
from functools import partial
from connector import getCoupons
import configs.constants as constants

COUPON_NAME = 0
EXPIRY_DATE = 1
BUTTON      = 2

class CouponEntry(tk.Label):
  def __init__(self, parent, i, *args, **kwargs):
    tk.Label.__init__(
      self,
      parent,
      borderwidth=2,
      bg="white" if i%2==0 else constants.TABLE_BG,
      relief="ridge",
      pady=8,
      width=24,
      *args,
      **kwargs
    )

def couponWindow(parent, c):
  newWindow = tk.Toplevel(parent)
  newWindow.title("Coupons")
  newWindow.resizable(False, False)
  newWindow.configure(background="white")

  # Retrieve all of the coupons from the server
  response = getCoupons()
  if response["success"]:
    coupons = response["coupons"]

    # Coupons size
    tk.Label(newWindow, text=str(f"coupons"), font=constants.HEADER, bg="white", padx=8, pady=10, anchor="w").pack(fill="x")

    # Scrollbar
    canvas = tk.Canvas(newWindow, width=620, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(newWindow, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda _: canvas.configure(scrollregion = canvas.bbox("all")))

    # Grid for coupon entries
    grid = tk.Frame(canvas)
    canvas.create_window((0,0), window=grid, anchor="nw")

    # Apply coupon on next purchase
    def applyCoupon(coupon):
      c.coupon = coupon
      sleep(0.4)
      newWindow.destroy()
      newWindow.update()

    # Loop through all of the coupons and enter the results into the grid
    for index, coupon in enumerate(coupons):
      now = datetime.now()
      previous = datetime.strptime(coupon["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
      daysPassed = (now-previous).days
      if 10 - daysPassed > 0:
        for j in range(3):
          # Coupon name column
          if j == COUPON_NAME:
            CouponEntry(grid, index, text=coupons[index]["coupon"]).grid(row=index, column=0, sticky="news")
          # Days left column
          elif j == EXPIRY_DATE:
            CouponEntry(grid, index, text=f"Expires in {10 - daysPassed} days").grid(row=index, column=1, sticky="news")
          # Apply on next purchase column
          elif j == BUTTON:
            tk.Button(
              grid,
              text="Use on next purchase",
              command=partial(applyCoupon, coupon),
              borderwidth=2,
              relief="ridge",
              bg=constants.COUPON_BG,
              activebackground=constants.COUPON_HOVER,
              fg=constants.COUPON_LABEL_BG,
              activeforeground=constants.COUPON_LABEL_HOVER,
              cursor="hand1",
              pady=8
            ).grid(row=index, column=2, sticky="news")
  else:
    tk.Label(
      newWindow,
      text=response["message"],
      bg="white"
    ).pack(expand=True, fill="both", padx=20, pady=20)

  newWindow.transient(parent)
  newWindow.grab_set()
