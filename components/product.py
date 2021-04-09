# pyright: reportMissingImports=false
import tkinter as tk
import configs.constants as constants
import configs.screen as screen
from PIL import Image, ImageTk 

class ProductList(tk.Frame):
  def __init__(self, parent, c):
    tk.Frame.__init__(self, parent, bg="red", width=375, height=600)
    # Products from database
    self.products = c.products

    # 3x3 product grid
    self.productGrid = tk.Frame(self, bg="white", width=375, height=600)
    self.productGrid.grid()

    # 3 rows in total
    for index in range(3):
      # Each row consists of 3 products / columns
      row = self.products[index*3:(index*3) + 3]
      for col, product in enumerate(row):
        # Product picture
        tk.Label(self.productGrid, image=product.image, bd=0).grid(row=index, column=col)

        # Product code
        tk.Label(
          self.productGrid,
          bg="white",
          text=str(screen.PRODUCT_CODES[product.id]),
          font="Helvetica 11 bold"
        ).grid(row=index, column=col, sticky="s", pady=(0,55))

        # Price / Label frame
        tk.Frame(self.productGrid, width=125, height=50, bg="#ECECEC").grid(row=index, column=col, sticky="s")

        # Price
        priceFrame = tk.Frame(self.productGrid, bg="#ECECEC", width=70, height=20)
        priceFrame.grid(row=index, column=col, sticky="sw", pady=(0, 22), padx=10)
        tk.Label(priceFrame, text="$", font=constants.PRICE_FONT, bg="#ECECEC").grid(row=index, column=col, sticky="w")
        price = tk.Label(priceFrame, textvariable=product.price, fg=constants.TEXT_COLOR, font=constants.PRICE_FONT, bg="#ECECEC")
        price.grid(row=index, column=col, sticky="e", padx=(12, 0))

        # Label
        name = tk.Label(self.productGrid, bg="#ECECEC", textvariable=product.name, font=("Helvetica 9"))
        name.grid(row=index, column=col, sticky="sw", pady=(0, 6), padx=10)

        # Quantity Frame
        quantityFrame = tk.Frame(self.productGrid, bg="white", width=70, height=20)
        quantityFrame.grid(row=index, column=col, sticky="nw", pady=(8, 0), padx=10)

        # Quantity
        tk.Label(quantityFrame, text="Qty:", bg="white").grid(row=index, column=col, sticky="w")
        quantity = tk.Label(quantityFrame, bg="white", textvariable=product.quantity)
        quantity.grid(row=index, column=col, sticky="e", padx=32)
        

# Class for product item
class ProductItem:
  def __init__(self, root, id_, name, path, quantity=0, price=0):
    self.id       = id_
    self.name     = tk.StringVar(root, str(name))
    self.image    = ImageTk.PhotoImage(Image.open(path))
    self.price    = tk.DoubleVar(root, price)
    self.quantity = tk.IntVar(root, int(quantity))
