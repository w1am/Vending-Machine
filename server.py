#!/usr/bin/env python3
import socket
import pickle
from tinydb import TinyDB
from datetime import datetime, date
from tinydb.operations import increment
from configs.constants import PORT, HOST

couponDB     = TinyDB("database/coupon.json")
productDB    = TinyDB("database/product.json")
accountDB    = TinyDB("database/account.json")
transationDB = TinyDB("database/transaction.json")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
socket_client, (host, port) = server.accept()
print(f'🚀 Server is now running on port {PORT} 🚀')

while True:
  data = socket_client.recv(1024)
  if not data: break
  response = pickle.loads(data)

  if response["type"] == "createTransaction":
    balance = response["balance"]
    coupon = response["coupon"]
    couponID = response["couponID"]
    subtotal = response["subtotal"]
    cart = response["cart"]
    paymentType = response["paymentType"]

    subtotal = subtotal - (subtotal * (int(coupon[4:]) / 100)) if coupon else subtotal

    # Calculate the new card payment balance and return the changes if payment method is cash.
    newBalance = balance - subtotal

    # Proceed if user user has enough money 
    if subtotal <= balance:
      # Decrement stock
      for product in cart.values():
        productDB.update({
          "quantity": product["quantity"] - product["amount"]
        }, doc_ids=[product["id"]])

      # Update Balance
      if paymentType == "card":
        accountDB.update({ "balance": round(newBalance, 2) }, doc_ids=[1])

      # Delete coupon
      if coupon:
        couponDB.remove(doc_ids=[couponID])

      # Log trasaction
      transactionID = transationDB.insert({
        "timestamp": str(date.today()),
        "subtotal": round(response["subtotal"], 2),
        "coupon": coupon,
        "discount": round(subtotal * (int(coupon[4:]) / 100) if coupon else 0, 2),
        "cart": cart,
        "change": round(newBalance, 2)
      })

      socket_client.send(pickle.dumps({
        "success": True,
        "balance": round(newBalance, 2),
        "products": productDB.all(),
        "transactionID": transactionID
      }))
    else:
      socket_client.send(pickle.dumps({
        "success": False,
        "message": "Not Enough\nMoney"
      }))

  if response["type"] == "getCoupons":
    coupons = couponDB.all()
    data = {}
    if coupons:
      data = {
        "success": True,
        "message": None,
        "size": len(coupons),
        "coupons": coupons
      }
    else:
      data = {
        "success": False,
        "message": "You don't have any coupons with you. Play the lottery to increase your chances of winning.",
        "size": 0,
        "coupons": []
      }
    socket_client.send(pickle.dumps(data))

  if response["type"] == "getInventory":
    products = productDB.all()

    labels  = []
    sizes   = []
    colors  = []

    # arguments required for matlibplot library 
    # When the stock is low, it is red; when it is moderately low, it is orange; and when the stock is under control, it is green.
    for product in productDB:
      labels.append(product["name"])
      sizes.append(product["quantity"])
      if product["quantity"] < 10:
        colors.append("red")
      elif product["quantity"] in range(10, 20):
        colors.append("orange")
      else:
        colors.append("#55b70b")

    data = {}
    if products:
      data = {
        "success": True,
        "message": None,
        "labels": tuple(labels),
        "sizes": sizes,
        "colors": colors
      }
    else:
      data = {
        "success": False,
        "message": "Can't fetch inventory",
        "labels": labels,
        "sizes": sizes,
        "colors": colors
      }
    socket_client.send(pickle.dumps(data))

  if response["type"] == "updateAccountBalance":
    success = accountDB.update({"balance": round(response["newBalance"], 2)}, doc_ids=[1])
    socket_client.send(pickle.dumps({ "success": True if success else False }))

  if response["type"] == "updateTicketBalance":
    success = accountDB.update(increment("lotteryTickets"), doc_ids=[1])
    socket_client.send(pickle.dumps({ "success": True if success else False }))

  if response["type"] == "generateCoupon":
    today = datetime.now()

    couponDB.insert({
      'coupon': response["coupon"],
      'timestamp': str(today) 
    })
