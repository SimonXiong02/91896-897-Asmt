# This module is the checkout functionality of coffeeOS
from tkinter import messagebox
from datetime import datetime
import uuid

class OrderManager:

    @staticmethod
    def checkout(cart, clear_callback):
        if not cart:
            messagebox.showwarning("Empty", "No items in cart")
            return

        confirm = messagebox.askyesno("Alert", "Do you want a receipt printed out?")

        if confirm:

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