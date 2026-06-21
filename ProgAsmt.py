
# * ---- This is a coffee menu framework ---- *
import tkinter as tk # * ---- Imports the GUI ---- *
from tkinter import ttk, messagebox # * ---- Imports the message box and more ---- *
from datetime import datetime
import uuid # * ---- Imports user id for every user ---- *
from cart_checkout import CartControl, CheckoutWindow # * ---- Imports the necessary module for checkouting the items ---- *
from Login_Screen import LoginWindow
from PIL import Image, ImageTk # * ---- Imports the module that allows icons to be displayed ---- *
from menu_config import * # * ---- Imports all the necessary things such as item prices, colour theme, tax rate, and more. ---- *

# * ------- COFFEE SYSTEM ------- *
class CoffeeOS:
    # * ---- Initializes the main program ---- *
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.icons = {}

        # * ---- Gets the icons from the menu_config module ---- *
        for item, path in ICONS.items():
            try:

                image = Image.open(path)

                image = image.resize((64, 64))

                self.icons[item] = ImageTk.PhotoImage(image)

            except Exception:
                self.icons[item] = None

        self.root.title("Cafe OS System")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)

        self.total_label = tk.Label(text="Total: $0.00", bg=CARD, fg=FG, font=("Arial", 30))
        self.total_label.pack(pady=5)

        self.cart = []
        self.build_ui()

    # * ---- Initializes UI elements of the main program ---- *
    def build_ui(self):
        left = tk.Frame(self.root, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(self.root, bg=CARD)
        right.pack(side="right", fill="y")

        notebook = ttk.Notebook(left)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # * ---- Builds a Frame for the nessercery UI buttons ---- *
        for category, items in MENU.items():
            tab = tk.Frame(notebook, bg=BG)
            notebook.add(tab, text=category)

            row = 0
            col = 0

            # * ---- Builds buttons for different items including their base prices and icons ---- *
            for item, price in items.items():
                btn = tk.Button(
                    tab,
                    text=f"{item}\n${price}",
                    bg=CARD,
                    fg=FG,
                    width=120,
                    height=120,
                    image=self.icons.get(item),
                    compound="top",
                    command=lambda i=item, p=price: self.display_price(i, p)
                )
                btn.bind("<Button-3>", lambda event, i=item, p=price: self.display_price(event, i , p))
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col > 2:
                    col = 0
                    row += 1

        control_frame = tk.Frame(right, bg=CARD)
        control_frame.pack(pady=5)

        self.size_var = tk.StringVar(value="Medium")
        self.qty_var = tk.IntVar(value=1)

        # * ---- Creates a item tree for listing the item's properties ---- *
        self.tree = ttk.Treeview(
            self.root,
            columns=("Item", "Size", "Qty", "Price"),
            show="headings",
            height=15
            )

        self.tree.heading("Item", text="Item")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Price", text="Price")
        self.tree.pack(padx=10, pady=10)

        # * ---- Binds the button for opening the display_price menu ---- *
        self.tree.bind("<Double-Button-1>", self.change_item_propertires)

        # * ---- Adds two buttons for checkout and clearing the items in cart ---- *
        tk.Button(right, text="Checkout", bg=ACCENT, command=self.checkout).pack(fill="x", padx=10, pady=5)
        tk.Button(right, text="Clear", bg=FG, command=self.clear_cart).pack(fill="x", padx=10, pady=5)

        # * ---- Adds another two buttons for loging out and quiting the program ---- *
        tk.Button(right, text="Logout", bg=ACCENT, fg="black", command=self.logout).pack(fill="x", padx=10, pady=5)
        tk.Button(right, text="Quit", bg=ACCENT, fg="black", command=self.quit_program).pack(fill="x", padx=10, pady=5)

    # * ---- Gives users the freedom the preview the price of each item by their size variants ---- *
    def display_price(self, item, price):

        # * ---- Define and set the menu ---- *
        menu = tk.Menu(self.root, tearoff=0)

        # * ---- Defines the sizes ---- *
        small = (price * SIZES["Small"])
        medium = (price * SIZES["Medium"])
        large = (price * SIZES["Large"])

        # * ---- Adds a space between the title and the items ---- *
        menu.add_command(label=f"{item}")
        menu.add_separator()

        # * ---- Layout configuration ---- *
        menu.add_command(label=f"Small  - ${small:.2f}", command=lambda: self.item_selection(item, "Small", small))
        menu.add_command(label=f"Medium  - ${medium:.2f}", command=lambda: self.item_selection(item, "Medium", medium))
        menu.add_command(label=f"Large  - ${large:.2f}", command=lambda: self.item_selection(item, "Large", large))

        # * ---- Enables the window pop ---- *
        menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())

    # * ---- Allows user to add items in different sizes ---- *
    def item_selection(self, item, size, price):

        for i, (cart_item, cart_size, qty, total) in enumerate(self.cart):
            if cart_item == item and cart_size == size:

                self.cart[i] = (
                    cart_item,
                    cart_size,
                    qty + 1,
                    total + price
                )

                self.refresh_cart()

                return

        self.cart.append((item, size, 1, price))

        self.refresh_cart()

    # * ---- Refreshes the cart and values ---- *
    def refresh_cart(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item, size, qty, total in self.cart:
            self.tree.insert("", "end", values=(item, size, qty, f"{total:.2f}"))

        total_price = sum(total for item, size, qty, total in self.cart)

        self.total_label.config(text=f"Total: ${total_price:.2f}")

    # * ---- Grants users the priveilage to edit their item's quantity and size ---- *
    def change_item_propertires(self, event):

        selection = self.tree.selection()

        if not selection:
            return

        item_id = selection[0]
        index = self.tree.index(item_id)

        item, size, qty, total = self.cart[index]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Item")
        edit_window.geometry("500x300")

        tk.Label(edit_window, text=item, font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(edit_window, text="Size:").pack()

        size_var = tk.StringVar(value=size)
        size_combo = ttk.Combobox(edit_window, textvariable=size_var, values=list(SIZES.keys()), state="readonly")
        size_combo.pack(pady=5)

        tk.Label(edit_window, text=item, font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(edit_window, text="Quantity:").pack()

        qty_var = tk.IntVar(value=qty)
        qty_spin = tk.Spinbox(edit_window, from_=1, to=99, textvariable=qty_var, width=5)
        qty_spin.pack(pady=5)

        # * ---- Saves the user changes ---- *
        def save_changes():

            new_qty = int(qty_var.get())
            new_size = size_var.get()

            together_price = total / (qty * SIZES[size])

            new_total = together_price * SIZES[new_size] * new_qty

            self.cart[index] = (item, new_size, new_qty, new_total)
            self.refresh_cart()

            edit_window.destroy()

        tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

    # * ---- Updates the total amount of currency ---- *
    def update_total(self):
        total = sum(p for _, _, p in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    # * ---- A checkout port update ---- *
    def checkout(self):

        # * ---- Validates if the user had entered any items into the cart ---- *
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add an item before checkout.")
            return

        total = sum(price for _, _, _, price in self.cart)

        self.root.withdraw() # * ---- Hide the main menu while the checkout window is open ---- *

        CheckoutWindow(self.root, self.cart, self.username, total, self.validate_item)

    # * ---- Completes the full order ---- *
    def validate_item(self):
        CartControl.cart_validation(self.cart, self.clear_cart)

    # * ---- Add option for users to clear cart at their will ---- *
    def clear_cart(self):
        CartControl.clear_cart(self.cart, self.tree, self.update_total)

# * -------- QUITS THE PROGRAM -------- *
    def quit_program(self):
        self.root.destroy()

# * -------- START THE OPERATION SYSTEM -------- *
    def start_os(self, username):
        root = tk.Tk()
        self.username = username

        CoffeeOS(root, username)
        root.mainloop()

# * -------- ALLOWS USERS TO LOGOUT -------- *
    def logout(self):
        self.root.destroy()

        login_root = tk.Tk()

        LoginWindow(login_root, self.start_os)
        login_root.mainloop()

# * -------- START THE CORE OF THE PROGRAM -------- *
def main_app(username):
    root = tk.Tk()
    app = CoffeeOS(root, username)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root, main_app)
    login_root.mainloop()