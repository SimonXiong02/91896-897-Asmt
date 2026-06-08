
# * ---- The module that grant users the privege to create new accounts ---- *
import tkinter as tk
from tkinter import messagebox
from User_accounts import create_account
from menu_config import *


class CreateAccountWindow:
    # * ---- Initializes the Create Account Window UI elements ---- *
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Create Account")
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg=BG)

        center_frame = tk.Frame(self.window, bg=BG, padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.window, text="Create Account", bg=BG, fg=FG, font=("Arial", 30)).pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        tk.Label(center_frame, text="Username", bg=BG, fg=ACCENT, font=("Arial", 16)).pack()
        tk.Entry(center_frame, textvariable=self.username_var, bg=BG, fg=FG, font=("Arial", 20)).pack(pady=5)

        tk.Label(center_frame, text="Password", bg=BG, fg=ACCENT, font=("Arial", 16)).pack()
        tk.Entry(center_frame, textvariable=self.password_var, show="*", bg=BG ,fg=FG, font=("Arial", 20)).pack(pady=5)

        tk.Label(center_frame, text="Confirm Password", bg=BG, fg=ACCENT, font=("Arial", 16)).pack(pady=5)
        tk.Entry(center_frame, textvariable=self.confirm_password_var, show="*", bg=BG, fg=FG, font=("Arial", 20)).pack(pady=5)

        tk.Button(center_frame, text="Create", bg=ACCENT, command=self.create, font=("Arial", 16)).pack(pady=20)

    # * ---- Validates the accounts ---- *
    def create(self):

        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = (self.confirm_password_var.get())

        # * ---- Check if user entered all the fields ---- *
        if not username or not password:
            messagebox.showwarning("Missing", "Please fill all fields")
            return

        # * ---- Check if user entered the right password ---- *
        try:
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return

            # * ---- Closes the login menu while the create account window is open ---- *
            create_account(username, password)
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))