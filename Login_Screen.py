# This is a login screen for Coffee OS
import tkinter as tk
from tkinter import messagebox
from User_accounts import create_account
from create_account_window import CreateAccountWindow

# ------- USERS --------
from User_accounts.auth import verify_password
from User_accounts.storage import load_users

# -------- Theme --------
BG = "#2b2b2b"
FG = "#ffffff"
ACCENT = "#c7a17a"

class LoginWindow:
    def __init__(self, root, success_callback):
        self.root = root
        self.success_callback = success_callback

        self.root.title("Login - Cafe OS")
        self.root.geometry("500x450")
        self.root.configure(bg=BG)

        tk.Label(root, text="Cafe Login", bg=BG, fg=FG, font=("Arial", 16)).pack(pady=20)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Entry(root, textvariable=self.username, bg=BG, fg=FG).pack(pady=5)
        tk.Entry(root, textvariable=self.password, show="*", bg=BG, fg=FG).pack(pady=5)

        tk.Button(root, text="Login", bg=ACCENT, command=self.login).pack(pady=20)
        tk.Button(root, text="Create Account", bg=ACCENT, command=self.open_create_account).pack(pady=5)

    def open_create_account(self):
        CreateAccountWindow(self.root)

    def login(self):

        username = self.username.get()
        password = self.password.get()

        users = load_users()

        for user in users:
            if user["username"] == username:
                if verify_password(password, user["password_hash"]):
                    self.root.destroy()
                    self.success_callback()
                    return

        messagebox.showerror("Error", "Invalid username or password!")