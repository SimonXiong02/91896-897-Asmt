
# * ---- This module is the checkout functionality of coffeeOS ---- *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import uuid
import random
import json
import os

# * ---- Imports the reportlab module's tools ---- *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# * ---- Imports the appearance config ---- *
from menu_config import *

# * ---- Creates the pdf inside the json ---- *
def create_pdf_receipt(json_file):

    with open(json_file, "r") as file:
        data = json.load(file)

    pdf_name = (
        f"receipts/"
        f"{data['username']}_"
        f"{data['receipt_id']}.pdf"
    )

    doc = SimpleDocTemplate(pdf_name)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("CoffeeOS Receipt", styles["Title"]))

    content.append(Spacer(1, 10))

    info_table = Table(
        [[
            f"Receipt ID: {data['receipt_id']}",
            f"GST: {data['gst']:.0f}"
        ]]
        )

    content.append(info_table)

    content.append(Paragraph(f"Cashier: {data['username']}", styles["Normal"]))

    content.append(Paragraph(f"Created: {data['timestamp']}", styles["Normal"]))

    content.append(Spacer(1, 10))

    for item in data["items"]:

        content.append(
            Paragraph(
                f"{item['item']} x{item['quantity']} - "
                f"${item['line_total']:.2f}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Total: ${data['total']:.2f}", styles["Normal"]))

    content.append(Paragraph(f"Total (Tax included): ${data['total_plus_tax']:.2f}", styles["Heading2"]))

    content.append(Paragraph(f"Cash Received: ${data['cash_received']:.2f}", styles["Normal"]))

    content.append(Paragraph(f"Change: ${data['change']:.2f}", styles["Heading3"]))

    doc.build(content)

class CheckoutWindow:
    # * ---- Initializes the checkout window UI elements ---- *
    def __init__(self, parent, total, complete_callback):

        self.total = total
        self.complete_callback = complete_callback

        self.window = tk.Toplevel(parent)

        self.window.title("Checkout")
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg=BG)

        vcmd = (self.window.register(self.validate_cash), "%P")

        center_frame = tk.Frame(self.window, bg=BG, padx=50, pady=50)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.window, text="Checkout", bg=BG, fg=FG, font=("Arial", 30)).pack(pady=20)
        tk.Label(center_frame, text=f"Total: ${total:.2f}", bg=BG, fg=FG, font=("Arial", 18)).pack(pady=10)

        self.cash_var = tk.StringVar()
        self.cash_var.trace_add("write", self.update_change)

        tk.Label(center_frame, text="Cash Received", bg=BG, fg=FG, font=("Arial", 18)).pack()
        tk.Entry(center_frame, textvariable=self.cash_var, validate="key", validatecommand=vcmd, bg="white", fg="black", font=("Arial", 20)).pack(pady=10, ipadx=30)

        self.change_label = tk.Label(center_frame, text="Change: $0.00", bg=BG, fg=FG, font=("Arial", 15))
        self.change_label.pack(pady=10)

        tk.Button(center_frame, text="Process Payment", bg=ACCENT, command=self.process_payment, font=("Arial", 18)).pack(pady=20)

    # * ---- Validates that users can't enter 0 as the first number ---- *
    def validate_cash(self, value):

        if value == "":
            return True

        try:
            float(value)
        except ValueError:
            return False

        if value.startswith("0") and len(value) > 1 and value[1] != ".":
            return False

        if value == "0":
            return False

        return True

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

        # * ---- Displays change in currency ---- *
        change = cash - self.total

        self.change_label.config(text=f"Change: ${change:.2f}")

        os.makedirs("receipts", exist_ok=True)

        receipt_id = str(uuid.uuid4())[:8]

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        receipt_data = {
            "receipt_id": receipt_id,
            "username": self.username,
            "timestamp": timestamp,
            "items": items,
            "total": total,
            "tax": tax,
            "total(Tax included)": total_plus_tax,
            "cash_received": cash,
            "change": change
        }

        for item, qty, line_total in self.cart:

            receipt_data["items"].append({
                "item": item,
                "quantity": qty,
                "line_total": line_total
            })

        json_file = (
            f"receipts/"
            f"{timestamp}_{receipt_id}.json"
        )

        with open(json_file, "w") as file:
            json.dump(
                receipt_data,
                file,
                indent=4
            )

        create_pdf_receipt(json_file)

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

        # * ---- User specific uuid and date of receipt created ---- *
        order_id = str(uuid.uuid4())[:8]

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        total = 0

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

        # * ---- Main receipt details ---- *
        for item, qty, price in cart:

            content.append(Paragraph(f"{item} x{qty} - ${price:.2f}", styles["Normal"]))

            total += price

        tax = total * TAX_RATE

        gst = random.randint(1, 900000)

        total_plus_tax = total + tax

        # * ---- ordering the receipt structure ---- *
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Total: ${total:.2f}", styles["Normal"]))

        content.append(Paragraph(f"Tax ({TAX_RATE*100:.0f}%): ${tax:.2f}", styles["Normal"]))

        content.append(Paragraph(f"GST: {gst:.0f}", styles["Normal"]))

        content.append(Paragraph(f"Total(Tax included): ${total_plus_tax:.2f}", styles["Heading2"]))

        doc.build(content)

        clear_callback()

    # * ---- Clears Cart ---- *
    @staticmethod
    def clear_cart(cart, tree, update_total):
        cart.clear()

        for row in tree.get_children():
            tree.delete(row)

        update_total()