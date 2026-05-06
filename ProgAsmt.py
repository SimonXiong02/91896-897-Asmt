# This is a coffee menu framework

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
from Login_Screen import *


USERS = {
    "admin": "1234",
    "staff": "noob1234"
}

BG = "#2b2b2b"
FG = "#ffffff"
ACCENT = "#c7a17a"
CARD = "#3a3a3a"

MENU = {
    "Coffee": {
        "Espresso": 3.0,
        "Americano": 3.5,
        "Flat White": 4.2,
        "Latte": 4.5,
        "Cappuccino": 4.0,
        "Mocha": 5.0
    },
    "Tea": {
        "Green Tea": 3.0,
        "Black Tea": 2.8,
        "Chai Latte": 4.2
    },
    "Food": {
        "Croissant": 3.5,
        "Muffin": 3.0,
        "Sandwich": 6.5
    }
}

SIZES = {
    "Small": 1.0,
    "Medium": 1.3,
    "Large": 1.6
}

TAX_RATE = 0.15


# ------- COFFEE SYSTEM -------
class CoffeeOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe OS System")
        self.root.geometry("1000x600")
        self.root.configure(bg=BG)

        self.cart = []
        self.build_ui()

    def build_ui(self):
        left = tk.Frame(self.root, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(self.root, bg=CARD)
        right.pack(side="right", fill="y")

        notebook = ttk.Notebook(left)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for category, items in MENU.items():
            tab = tk.Frame(notebook, bg=BG)
            notebook.add(tab, text=category)

            row = 0
            col = 0

            for item, price in items.items():
                btn = tk.Button(
                    tab,
                    text=f"{item}\n${price}",
                    bg=CARD,
                    fg=FG,
                    width=15,
                    height=3,
                    command=lambda i=item, p=price: self.select_item(i, p)
                )
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col > 2:
                    col = 0
                    row += 1



if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()