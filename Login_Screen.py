# This is a login screen for Coffee OS
import tkinter as tk
from tkinter import messagebox
# from User_accounts import create_account

# ------- USERS --------
USERS = {
    "admin": "1234",
    "staff": "noob1234"
}


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

        tk.Entry(root, textvariable=self.username).pack(pady=5)
        tk.Entry(root, textvariable=self.password, show="*").pack(pady=5)

        tk.Button(root, text="Login", bg=ACCENT, command=self.login).pack(pady=20)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in USERS and USERS[user] == pwd:
            self.root.destroy()
            self.success_callback()
        else:
            messagebox.showerror("Error", "Invalid login!")