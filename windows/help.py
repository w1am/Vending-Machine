# pyright: reportMissingImports=false
import tkinter as tk
import configs.constants as constants

def helpWindow(parent):
  newWindow = tk.Toplevel(parent)
  newWindow.title("Help")
  newWindow.resizable(False, False)
  newWindow.configure(background="white") 

  frame = tk.Frame(newWindow, bg="white")
  frame.pack(padx=15)
  tk.Label(frame, bg="white", text="How To Use Vending Machine", font=constants.HEADER).pack(pady=(20,8))
  tk.Label(frame, bg="white", text="1. Enter the code of the item you wish to buy", anchor="w").pack(fill="x")
  tk.Label(frame, bg="white", text="2. Enter amount", anchor="w").pack(fill="x")
  tk.Label(frame, bg="white", text="3. Select payment method", anchor="w").pack(fill="x")
  tk.Label(frame, bg="white", text="4. Take your change", anchor="w").pack(fill="x")

  def close():
    newWindow.destroy()
    newWindow.update()

  # Play button
  tk.Button(
    newWindow,
    command=close,
    text="Okay",
    bg=constants.SKY_BG, activebackground=constants.SKY_HOVER, fg="white",
    activeforeground="white",
    font=constants.COPY_FONT,
    height=1, pady=10, bd=0,
    cursor="hand1",
  ).pack(fill="x", side="bottom", pady=(20,0))

  newWindow.transient(parent)
  newWindow.grab_set()
