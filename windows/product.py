# pyright: reportMissingImports=false
import tkinter as tk
from tinydb import TinyDB
from windows.popup import popupWindow

productDB = TinyDB("database/product.json")

def productsWindow(c, parent):
  saveImage = tk.PhotoImage(file="assets/icons/save.png")

  newWindow = tk.Toplevel(parent)
  newWindow.title("Products")
  newWindow.resizable(False, False)
  newWindow.configure(background="white")

  tk.Label(newWindow, text="Change the field values to update your goods.", bg="white", anchor="w", padx=10, pady=8).pack(fill="x")
  
  frame = tk.Frame(newWindow, bg="white")
  frame.pack(expand=True)

  # Label grid
  labelGrid = tk.Frame(frame, bg="white")
  labelGrid.grid(sticky="news")

  keys = ["name", "quantity", "price"]

  # Table headers
  for index, key in enumerate(keys):
    tk.Label(
      labelGrid,
      text=str(key.capitalize()),
      width=24,
      bg="#DEDEDE",
      pady=10,
      borderwidth=2,
      relief="ridge",
      anchor="w"
    ).grid(row=0, column=index, sticky="w")

  grid = tk.Frame(frame, bg="white")
  grid.grid(sticky="news")

  # Product entries to keep track of any changes 
  productEntries = {}
  
  # Display the products information in a table
  for index, product in enumerate(c.products):
    fields = {}
    for j in range(3):
      entry = tk.Entry(grid, bg="white" if index%2 == 0 else "#DEDEDE", width=24, borderwidth=2, relief="ridge")
      entry.grid(row=index, column=j, sticky="news", ipady=8)
      fields[keys[j]] = entry
      if   j == 0: entry.insert(0, product.name.get())
      elif j == 1: entry.insert(0, product.quantity.get())
      elif j == 2: entry.insert(0, product.price.get())
    productEntries[product.id] = fields


  # Read the updated values from the entries and update them in the database accordingly
  def onSave():
    products = c.products
    for key, field in enumerate(productEntries.values(), start=1):
      try:
        products[key-1].name.set(field["name"].get())
        productDB.update({ "name": field["name"].get() }, doc_ids=[key])

        products[key-1].quantity.set(int(field["quantity"].get()))
        productDB.update({ "quantity": int(field["quantity"].get()) }, doc_ids=[key])

        products[key-1].price.set(float(field["price"].get()))
        productDB.update({ "price": float(field["price"].get()) }, doc_ids=[key])
      except ValueError: pass
    popupWindow(newWindow, "Products updated successfully!")

  tk.Button(
    newWindow,
    command=onSave,
    text="Save Changes",
    image=saveImage,
    compound="left",
    bg="#2780B4",
    activebackground="#2d88bc",
    fg="white",
    activeforeground="white",
    border=0,
    cursor="hand1",
    height=3,
    pady=20,
    font=("Helvetica 10 bold")
  ).pack(fill="x")

  newWindow.transient(parent)
  newWindow.grab_set()
  parent.wait_window(newWindow)
