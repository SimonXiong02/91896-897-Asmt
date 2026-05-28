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
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg=BG)

        center_frame = tk.Frame(self.window, bg=BG, padx=50, pady=50)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Checkout", bg=BG, fg=FG, font=("Arial", 20)).pack(pady=20)
        tk.Label(center_frame, text=f"Total: ${total:.2f}", bg=BG, fg=FG, font=("Arial", 18)).pack(pady=10)

        self.cash_var = tk.StringVar()
        self.cash_var.trace_add("write", self.update_change)

        tk.Label(center_frame, text="Cash Received", bg=BG, fg=FG, font=("Arial", 18)).pack()
        tk.Entry(center_frame, textvariable=self.cash_var, bg="white", fg="black", font=("Arial", 20)).pack(pady=10, ipadx=30)

        self.change_label = tk.Label(center_frame, text="Change: $0.00", bg=BG, fg=FG, font=("Arial", 15))
        self.change_label.pack(pady=10)

        tk.Button(center_frame, text="Process Payment", bg=ACCENT, command=self.process_payment, font=("Arial", 18)).pack(pady=20)


    def update_change(self, *args):
        try:
            cash = float(self.cash_var.get())

            change = cash - self.total

            self.change_label.config(text=f"Change: ${change:.2f}")

        except ValueError:
            self.change_label.config(text="Change: $0.00")

    def process_payment(self):
        try:
            cash = float(self.cash_var.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        if round(cash, 2) < round(self.total, 2):
            messagebox.showwarning("Not Enough", "Customer has not paid enough")
            return

        change = cash - self.total

        self.change_label.config(text=f"Change: ${change:.2f}")

        messagebox.showinfo("Success", "Payment Complete")

        self.complete_callback()
        self.window.destroy()

class PrintReceipt:

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

        clear_callback()

    @staticmethod
    def clear_cart(cart, tree, update_total):
        cart.clear()

        for row in tree.get_children():
            tree.delete(row)

        update_total()