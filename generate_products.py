import os
from tinydb import TinyDB
from random import uniform, randint

DATABASE = "database/product.json"

os.remove(DATABASE)
db = TinyDB(DATABASE)

colors = [
  'red', 'blue', 'purple',
  'green', 'orange', 'pink',
  'yellow', '#EF4B4C', '#4AA976'
]

products = os.listdir('./assets/products')

for product in products:
  productName = product.split(".")[0]
  db.insert({
    'name': productName.split("-")[0].capitalize() + " " + productName.split("-")[1].capitalize(),
    'image': f"assets/products/{product}",
    'quantity': randint(0, 90),
    'price': round(uniform(3.99, 5.99), 2),
  })
