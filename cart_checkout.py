
# * ---- This module is the checkout functionality of coffeeOS ---- *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import uuid

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from menu_config import *

class CheckoutWindow:
    # * ---- Initializes the checkout window UI elements ---- *
    def __init__(self, parent, total, complete_callback):

        self.total = total
        self.complete_callback = complete_callback

        self.window = tk.Toplevel(parent)

        self.window.title("Checkout")
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg=BG)

        center_frame = tk.Frame(self.window, bg=BG, padx=50, pady=50)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.window, text="Checkout", bg=BG, fg=FG, font=("Arial", 30)).pack(pady=20)
        tk.Label(center_frame, text=f"Total: ${total:.2f}", bg=BG, fg=FG, font=("Arial", 18)).pack(pady=10)

        self.cash_var = tk.StringVar()
        self.cash_var.trace_add("write", self.update_change)

        tk.Label(center_frame, text="Cash Received", bg=BG, fg=FG, font=("Arial", 18)).pack()
        tk.Entry(center_frame, textvariable=self.cash_var, bg="white", fg="black", font=("Arial", 20)).pack(pady=10, ipadx=30)

        self.change_label = tk.Label(center_frame, text="Change: $0.00", bg=BG, fg=FG, font=("Arial", 15))
        self.change_label.pack(pady=10)

        tk.Button(center_frame, text="Process Payment", bg=ACCENT, command=self.process_payment, font=("Arial", 18)).pack(pady=20)

    # * ---- updates the change ---- *
    def update_change(self, *args):
        try:
            cash = float(self.cash_var.get())

            change = cash - self.total

            self.change_label.config(text=f"Change: ${change:.2f}")

        except ValueError:
            self.change_label.config(text="Change: $0.00")

    # * ---- proceeds the payment ---- *
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

# * ---- Class containing the essential code for generating receipts ---- *
class PrintReceipt:

    @staticmethod
    def checkout(cart, clear_callback):
        if not cart:
            messagebox.showwarning("Empty", "No items in cart")
            return

        order_id = str(uuid.uuid4())[:8]

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        subtotal = 0

        # * ---- Receipt label configuration ---- *
        pdf_file = (
            f"{timestamp}_"
            f"{order_id}.pdf"
        )

        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()

        # * ---- Receipt details ---- *
        content = [
            Paragraph("CoffeeOS Receipt", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Receipt ID: {order_id}", styles["Normal"]),
            Paragraph(f"Created: {timestamp}", styles["Normal"]),
            Spacer(1, 12)
        ]

        for item, qty, price in cart:

            content.append(Paragraph(f"{item} x{qty} - ${price:.2f}", styles["Normal"]))

            subtotal += price

        tax = subtotal * TAX_RATE

        total = subtotal + tax

        # * ---- ordering the receipt structure ---- *
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Subtotal: ${subtotal:.2f}", styles["Normal"]))

        content.append(Paragraph(f"Tax ({TAX_RATE*100:.0f}%): ${tax:.2f}", styles["Normal"]))

        content.append(Paragraph(f"Total: ${total:.2f}", styles["Heading2"]))

        doc.build(content)

        clear_callback()

    # * ---- Clears Cart ---- *
    @staticmethod
    def clear_cart(cart, tree, update_total):
        cart.clear()

        for row in tree.get_children():
            tree.delete(row)

        update_total()