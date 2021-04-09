# pyright: reportMissingImports=false
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from connector import getInventory
import configs.constants as constants
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

def plot(window):
  # Get inventory from server
  response = getInventory()

  # Draw the bar chart
  plt.rcdefaults()
  fig, ax = plt.subplots()
  fig.set_size_inches(20, 10, forward=True)

  y_pos = np.arange(len(response["labels"]))

  # Add chart labels and sizes
  ax.barh(y_pos, response["sizes"], xerr=None, align='center', color=response["colors"])
  ax.set_yticks(y_pos)
  ax.set_yticklabels(response["labels"])
  ax.invert_yaxis()
  ax.set_xlabel('Stock')
  ax.set_title('Track your inventory')

  canvas = FigureCanvasTkAgg(fig, master = window)  
  canvas.draw()

  canvas.get_tk_widget().pack()

def inventoryWindow(parent):
  newWindow = tk.Toplevel(parent)
  newWindow.title("Inventory")
  newWindow.geometry("1000x500")
  newWindow.configure(background="white", pady=10, padx=20)

  # Inventory Header
  tk.Label(newWindow, text="Inventory", bg="white", font=constants.HEADER, fg=constants.TEXT_COLOR).pack()

  # Plot pie chart
  plot(newWindow)

  newWindow.transient(parent)
  newWindow.grab_set()
  parent.wait_window(newWindow)
