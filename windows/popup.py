import tkinter as tk

# Popup window to display warning messages
def popupWindow(parent, message):
  newWindow = tk.Toplevel(parent)
  newWindow.geometry("350x100")
  newWindow.resizable(False, False)
  newWindow.configure(background="white")

  tk.Label(newWindow, text=message, bg="white").pack(fill="both", expand=True)

  newWindow.transient(parent)
  newWindow.grab_set()
  parent.wait_window(newWindow)
