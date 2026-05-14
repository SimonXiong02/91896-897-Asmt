from users import User
from auth import hash_password
from storage import *

def create_account(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username:
            raise ValueError("Username already exists.")
        
    password_hash = hash_password(password)

    new_user = User(username, password_hash)

    users.append(new_user.to_dict())

    save_users(users)

    return "Account created successfully!"