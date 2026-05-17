import tkinter as tk
from tkinter import messagebox
from User_accounts import create_account
from menu_config import *


class CreateAccountWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Create Account")
        self.window.geometry("500x450")
        self.window.configure(bg=BG)

        tk.Label(self.window, text="Create Account", bg=BG, fg=FG, font=("Arial", 16)).pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self.window, text="Username", bg=BG, fg=FG).pack()
        tk.Entry(self.window, textvariable=self.username_var, bg=BG, fg=FG).pack(pady=5)

        tk.Label(self.window, text="Password", bg=BG, fg=FG).pack()
        tk.Entry(self.window, textvariable=self.password_var, show="*", bg=BG ,fg=FG).pack(pady=5)

        tk.Button(self.window, text="Create", bg=ACCENT, command=self.create).pack(pady=20)

    def create(self):

        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("Missing", "Please fill all fields")
            return

        try:
            message = create_account(username, password)
            messagebox.showinfo("Success", message)
            self.window.destroy()

        except ValueError as e:
            message.showerror("Error", str(e))