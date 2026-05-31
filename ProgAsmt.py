# This is a coffee menu framework

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
from cart_checkout import PrintReceipt, CheckoutWindow
from Login_Screen import LoginWindow
from menu_config import *


# ------- COFFEE SYSTEM -------
class CoffeeOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe OS System")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)

        self.total_label = tk.Label(text="Total: $0.00", bg=CARD, fg=FG, font=("Arial", 30))
        self.total_label.pack(pady=5)

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
                btn.bind("<Button-3>", lambda event, i=item, p=price: self.show_price_preview(event, i , p))
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col > 2:
                    col = 0
                    row += 1

        control_frame = tk.Frame(right, bg=CARD)
        control_frame.pack(pady=5)

        self.size_var = tk.StringVar(value="Medium")
        self.qty_var = tk.IntVar(value=1)

        ttk.Combobox(control_frame, textvariable=self.size_var, values=list(SIZES.keys()), state="readonly", width=10).grid(row=0, column=0, padx=5)
        ttk.Spinbox(control_frame, from_=0, to=100, textvariable=self.qty_var, validate="key", state="readonly",width=5).grid(row=0, column=1, padx=5)

        self.tree = ttk.Treeview(
            self.root,
            columns=("Item", "Qty", "Price"),
            show="headings",
            height=15
            )

        self.tree.heading("Item", text="Item")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Price", text="Price")
        self.tree.pack(padx=10, pady=10)

        tk.Button(right, text="Checkout", bg=ACCENT, command=self.checkout).pack(fill="x", padx=10, pady=5)
        tk.Button(right, text="Clear", command=self.clear_cart).pack(fill="x", padx=10)

        tk.Button(right, text="Logout", bg=ACCENT, fg="white", command=self.logout).pack(fill="x", padx=10, pady=5)

    def select_item(self, item, base_price):

        size = self.size_var.get()
        qty = self.qty_var.get()

        added_price = (
            base_price *
            SIZES[size] *
            qty
        )

        item_name = f"{item} ({size})"

        # Check if iten already exists
        for index, (cart_item, cart_qty, cart_price) in enumerate(self.cart):

            if cart_item == item_name:

                new_qty = cart_qty + qty
                new_price = cart_price + added_price

                self.cart[index] = (
                    cart_item,
                    new_qty,
                    new_price
                )

                for row in self.tree.get_children():

                    values = self.tree.item(row)["values"]

                    if values[0] == item_name:

                        self.tree.item(row, values=(item_name, new_qty, f"${new_price:.2f}"))
                        break

                self.update_total()
                return

        # Add new item if not found
        self.cart.append((item_name, qty, added_price))
        self.tree.insert("", "end", values=(item_name, qty, f"${added_price:.2f}"))

        self.update_total()

    def show_price_preview(self, event, item, base_price):
        menu = tk.Menu(self.root, tearoff=0)

        small = (base_price * SIZES["Small"])
        medium = (base_price * SIZES["Medium"])
        large = (base_price * SIZES["Large"])

        menu.add_command(label=f"{item}")
        menu.add_separator()

        menu.add_command(label=f"Small  - ${small:.2f}")
        menu.add_command(label=f"Medium  - ${medium:.2f}")
        menu.add_command(label=f"Large  - ${large:.2f}")

        menu.tk_popup(event.x_root, event.y_root)

    def update_total(self):
        total = sum(p for _, _, p in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        total = sum(price for _, _, price in self.cart)
        CheckoutWindow(self.root, total, self.complete_order)

    def complete_order(self):
        PrintReceipt.checkout(self.cart, self.clear_cart)

    def clear_cart(self):
        PrintReceipt.clear_cart(self.cart, self.tree, self.update_total)

    def start_os():
        root = tk.Tk()

        CoffeeOS(root)
        root.mainloop()

    def logout(self):
        self.root.destroy()

        login_root = tk.Tk()

        LoginWindow(login_root, self.start_os)
        login_root.mainloop()

# -------- START THE OPERATION SYSTEM ---------
def main_app():
    root = tk.Tk()
    app = CoffeeOS(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root, main_app)
    login_root.mainloop()