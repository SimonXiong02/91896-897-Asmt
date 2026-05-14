import json
import os

FILE_NAME = "users.json"

def load_users():
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "w") as file:
        return json.load(file)
    
def save_users(users):
    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)