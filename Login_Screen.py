# This is a login screen for Coffee OS

# ----- General -----
import tkinter as tk
from tkinter import messagebox
from User_accounts import create_account
from create_account_window import CreateAccountWindow

# ----- USERS -----
from User_accounts.auth import verify_password
from User_accounts.storage import load_users

# ----- Theme -----
from menu_config import *

class LoginWindow:
    def __init__(self, root, success_callback):
        self.root = root
        self.success_callback = success_callback

        self.root.title("Login - Cafe OS")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)

        center_frame = tk.Frame(root, bg=BG, padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Cafe Login", bg=BG, fg=FG, font=("Arial", 30)).pack(pady=20)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.username_label = tk.StringVar()
        self.password_label = tk.StringVar()

        self.username_label.set("Username")
        self.password_label.set("Password")

        # Username input
        tk.Label(center_frame, textvariable=self.username_label, bg=BG, fg=ACCENT, font=("Arial", 16)).pack(pady=5)
        tk.Entry(center_frame, textvariable=self.username, bg=BG, fg=FG, font=("Arial", 20)).pack(pady=5)

        # Password input
        tk.Label(center_frame, textvariable=self.password_label, bg=BG, fg=ACCENT, font=("Arial", 16)).pack(pady=5)
        tk.Entry(center_frame, textvariable=self.password, show="*", bg=BG, fg=FG, font=("Arial", 20)).pack(pady=5)

        tk.Button(center_frame, text="Login", bg=ACCENT, command=self.login, font=("Arial", 16)).pack(pady=20)
        tk.Button(center_frame, text="Create Account", bg=ACCENT, command=self.open_create_account, font=("Arial", 16)).pack(pady=5)

    def open_create_account(self):
        self.root.withdraw()

        create_window = CreateAccountWindow(self.root)

        self.root.wait_window(create_window.window)
        self.root.deiconify()

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