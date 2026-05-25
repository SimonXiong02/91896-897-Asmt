# This module is the checkout functionality of coffeeOS
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import uuid

from menu_config import *

class CheckoutWindow:
    def __init__(self, parent, total, complete_callback):

        self.total = total
        self.complete_callback = complete_callback

        self.window = tk.Toplevel(parent)

        self.window.title("Checkout")
        self.window.geometry("350x300")
        self.window.configure(bg=BG)

        tk.Label(self.window, text="Checkout", bg=BG, fg=FG, font=("Arial", 18)).pack(pady=20)
        tk.Label(self.window, text=f"Total: ${total:.2f}", bg=BG, fg=FG, font=("Arial", 14)).pack(pady=10)

        self.cash_var = tk.StringVar()

        tk.Label(self.window, text="Cash Received", bg=BG, fg=FG).pack()
        tk.Entry(self.window, textvariable=self.cash_var, bg="white", fg="black").pack(pady=10, ipadx=30)

        self.change_label = tk.Label(self.window, text="Change: $0.00", bg=BG, fg=FG, font=("Arial", 12))
        self.change_label.pack(pady=10)

        tk.Button(self.window, text="Process Payment", bg=ACCENT, command=self.process_payment).pack(pady=20)

    def process_payment(self):
        try:
            cash = float(self.cash_var.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        if cash < self.total:
            messagebox.showwarning("Not Enough", "Customer has not paid enough")
            return

        change = cash- self.total

        self.change_label.config(text=f"Change: ${change:.2f}")

        messagebox.showerror("Success", "Payment Complete")

        self.complete_callback()
        self.window.destroy()

class OrderManager:

    @staticmethod
    def checkout(cart, clear_callback):
        if not cart:
            messagebox.showwarning("Empty", "No items in cart")
            return

        order_id = str(uuid.uuid4())[:8]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        receipt = (
            f"Order ID: {order_id}\n"
            f"Time: {now}\n\n"
        )

        total = 0


        for item, qty, price in cart:

            receipt += (
                f"{item} x{qty} - ${price:.2f}\n"
            )

            total += price

        receipt += f"\nTotal: ${total:.2f}\n"


        with open(f"receipt_{order_id}.txt", "w") as file:
            file.write(receipt)

        messagebox.showinfo("Success", "Order complete!")

        clear_callback()

    @staticmethod
    def clear_cart(cart, tree, update_total):
        cart.clear()

        for row in tree.get_children():
            tree.delete(row)

        update_total()