
# * ---- This module is the checkout functionality of coffeeOS ---- *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import uuid
import random
import json
import os

# * ---- Imports the reportlab module's tools ---- *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

# * ---- Imports the appearance config ---- *
from menu_config import *

# * ---- Creates the pdf inside the json ---- *
def create_pdf_receipt(receipt):

    with open("receipts/receipt_database.json", "r") as file:
        data = json.load(file)

    pdf_name = (
        "receipts/receipt_history.pdf"
    )

    doc = SimpleDocTemplate(pdf_name)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("CoffeeOS Receipt History", styles["Title"]))

    content.append(Spacer(1, 20))

    for receipt in data["receipts"]:

        info_table = Table(
            [[
                f"Receipt ID: {receipt['receipt_id']}",
                f"GST: {receipt['gst']:.0f}"
            ]]
            )

        content.append(info_table)

        content.append(Paragraph(f"Customer: {receipt['username']}", styles["Normal"]))

        content.append(Paragraph(f"Created: {receipt['timestamp']}", styles["Normal"]))

        content.append(Spacer(1, 5))

        for item in receipt["items"]:

            content.append(
                Paragraph(
                    f"{item['item']} x{item['quantity']} - "
                    f"${item['line_total']:.2f}",
                    styles["Normal"]
                )
            )

        content.append(Spacer(1, 10))

        content.append(Paragraph(f"Total: ${receipt['total']:.2f}", styles["Normal"]))

        content.append(Spacer(1, 10))

        content.append(Paragraph(f"Tax(15%): ${receipt['tax']:.2f}", styles["Normal"]))

        content.append(Paragraph(f"Total + Tax: ${receipt['total_plus_tax']:.2f}", styles["Heading2"]))

        content.append(Paragraph(f"Cash Entered: ${receipt['cash_entered']:.2f}", styles["Normal"]))

        content.append(Paragraph(f"Change: ${receipt['change']:.2f}", styles["Heading3"]))

        content.append(Paragraph("-----------------------------------------------------------------------------------------------------------------------------------", styles["Normal"]))

        content.append(Spacer(1, 15))

    doc.build(content)

# * ---- Displays receipt when the user finishes their order ---- *
def show_receipt_window(receipt):

    receipt_window = tk.Toplevel()

    receipt_window.title("Receipt")

    receipt_window.geometry("600x700")

    text = tk.Text(receipt_window, font=("Arial", 11))

    text.pack(fill="both", expand=True)

    text.insert("end", "===== CoffeeOS Receipt =====\n\n")

    text.insert("end", f"Receipt ID: {receipt['receipt_id']}\n")

    text.insert("end", f"User: {receipt['username']}\n")

    text.insert("end", f"Date: {receipt['timestamp']}\n\n")

    text.insert("end", "Items\n")

    text.insert("end", "-" * 40 + "\n")

    for item in receipt["items"]:
        text.insert(
            "end",
            f"{item['item']} "
            f"x{item['quantity']} "
            f"${item['line_total']:.2f}\n"
        )

    text.insert("end", "\n" + "-" * 40 + "\n")

    text.insert("end", f"Total: ${receipt['total']:.2f}\n")

    text.insert("end", f"Tax: ${receipt['tax']:.2f}\n")

    text.insert("end", f"Total + Tax: ${receipt['total_plus_tax']:.2f}\n")

    text.insert("end", f"Cash Received: ${receipt['cash_entered']:.2f}\n")

    text.insert("end", f"Change: ${receipt['change']:.2f}\n")

    text.config(state="disabled")


class CheckoutWindow:
    # * ---- Initializes the checkout window UI elements ---- *
    def __init__(self, parent, cart, username, total, complete_callback):

        self.parent = parent
        self.cart = cart
        self.username = username
        self.total = total
        self.complete_callback = complete_callback

        self.window = tk.Toplevel(parent)

        self.window.protocol("WM_DELETE_WINDOW", self.close_checkout)

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

    # * ---- A function that completely closes the checkout window when the user finishes their purchase ---- *
    def close_checkout(self):

        self.parent.deiconify()

        self.window.destroy()

    # * ---- Validates that users can't enter 0 as the first number and cannot enter more than 2 decimal places ---- *
    def validate_cash(self, value):


        if value == "":
            return True

        try:
            float(value)

            if value.startswith("0") and len(value) > 1 and value[1] != ".":
                return False

            if value == "0":
                return False

            if "." in value:
                decimal_point = value.split(".")[1]

                if len (decimal_point) > 2:
                    return False

            return True

        except ValueError:
            return False


    # * ---- updates the change ---- *
    def update_change(self, *args):
        try:
            cash = float(self.cash_var.get())

            # * ---- Display change in the checkout window ---- *
            change = max(0, round(cash - self.total, 2))

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



        # * ---- Displays change in currency in receipt ---- *
        change = round(cash - self.total, 2)

        # * ---- Layout the json format ---- *
        os.makedirs("receipts", exist_ok=True)

        receipt_id = str(uuid.uuid4())[:8]

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        cash = float(self.cash_var.get())

        total = self.total

        tax = round(total * TAX_RATE, 2)

        gst = random.randint(1, 900000)

        total_plus_tax = round(total + tax, 2)

        receipt = {
            "receipt_id": receipt_id,
            "username": self.username,
            "timestamp": timestamp,
            "items": [],
            "total": total,
            "tax": tax,
            "gst": gst,
            "total_plus_tax": total_plus_tax,
            "cash_entered": cash,
            "change": change
        }

        for item, qty, line_total in self.cart:

            receipt["items"].append({
                "item": item,
                "quantity": qty,
                "line_total": line_total
            })

        # * ---- Prints out the receipt database ---- *
        data_base = "receipts/receipt_database.json"


        if os.path.exists(data_base):
            with open(data_base, "r") as file:
                receipt_history = json.load(file)

        else:
            receipt_history = {
                "receipts": []
            }

        receipt_history["receipts"].append(receipt)

        # * ---- Prints the receipt as pdf ---- *
        with open(data_base, "w") as file:
            json.dump(
                receipt_history,
                file,
                indent=4
            )

        create_pdf_receipt(receipt)

        messagebox.showinfo("Success", "Payment Complete")

        show_receipt_window(receipt)

        self.complete_callback()
        self.close_checkout()

# * ---- Class containing the essential code for validating and clearing cart ---- *
class CartControl:

    @staticmethod
    def cart_validation(cart, clear_callback):
        clear_callback()

    # * ---- Clears Cart ---- *
    @staticmethod
    def clear_cart(cart, tree, update_total):
        cart.clear()

        for row in tree.get_children():
            tree.delete(row)

        update_total()