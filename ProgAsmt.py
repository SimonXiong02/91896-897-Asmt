# This is a coffee menu framework

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
from Login_Screen import LoginWindow


# ---- Theme ----
BG = "#2b2b2b"
FG = "#ffffff"
ACCENT = "#c7a17a"
CARD = "#3a3a3a"

# ---- Cafe Menu ----
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

# ---- Options ----
SIZES = {
    "Small": 1.0,
    "Medium": 1.3,
    "Large": 1.6
}

# ---- Tax Rate ----
TAX_RATE = 0.15


# ------- COFFEE SYSTEM -------
class CoffeeOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe OS System")
        self.root.geometry("1000x600")
        self.root.configure(bg=BG)

        self.total_label = tk.Label(text="Total: $0.00", bg=CARD, fg=FG, font=("Arial", 16))
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
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col > 2:
                    col = 0
                    row += 1

        tk.Label(right, text="Order", bg=CARD, fg=FG, font=("Arial", 16)).pack(pady=10)

        control_frame = tk.Frame(right, bg=CARD)
        control_frame.pack(pady=5)

        self.size_var = tk.StringVar(value="Medium")
        self.qty_var = tk.IntVar(value=1)

        ttk.Combobox(control_frame, textvariable=self.size_var, values=list(SIZES.keys()), width=10).grid(row=0, column=0, padx=5)
        ttk.Spinbox(control_frame, from_=1, to=10, textvariable=self.qty_var, width=5).grid(row=0, column=1, padx=5)

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

    def select_item(self, item, base_price):
        size = self.size_var.get()
        qty = self.qty_var.get()

        price = base_price * SIZES[size] * qty
        self.cart.append((item, qty, price))

        self.tree.insert("", "end", values=(f"{item} ({size})", qty, f"${price:.2f}"))
        self.update_total()

    def update_total(self):
        total = sum(p for _, _, p in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items in cart")
            return

        confirm = messagebox.askyesno("Alert", "do you want to have a receipt")

        if confirm:

            order_id = str(uuid.uuid4())[:8]
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            receipt = f"Order ID: {order_id}\nTime: {now}\n\n"

            for item, qty, price in self.cart:
                receipt += f"{item} x{qty} - ${price:.2f}\n"

            total = sum(p for _, _, p in self.cart)
            receipt += f"\nTotal: ${total:.2f}\n"

            with open(f"receipt_{order_id}.txt", "w") as f:
                f.write(receipt)

            messagebox.showinfo("Success", "Order complete!")
            self.clear_cart()

    def clear_cart(self):
        self.cart.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.update_total()

# -------- START THE OPERATION SYSTEM ---------
def main_app():
    root = tk.Tk()
    app = CoffeeOS(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root, main_app)
    login_root.mainloop()