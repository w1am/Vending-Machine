# Stages
CODE    = 1
AMOUNT  = 2
CONFIRM = 3
PAY_CASH = 4

# Buttons
LOTTERY = "LO"
HELP = "HELP"
CLEAR   = "CLR"

BUTTONS = [
  ["A", "1", "2", "3"],
  ["B", "4", "5", "6"],
  ["C", "7", "8", "9"],
  [HELP, ".", "0", CLEAR]
]

# Button code combinations
BUTTON_CODES = { "A1": 0, "A2": 1, "A3": 2, "B1": 3, "B2": 4, "B3": 5, "C1": 6, "C2": 7, "C3": 8 }
PRODUCT_CODES = { 1: "A1", 2: "A2", 3: "A3", 4: "B1", 5: "B2", 6: "B3", 7: "C1", 8: "C2", 9: "C3" }
