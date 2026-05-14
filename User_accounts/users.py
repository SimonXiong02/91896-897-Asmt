# This is where the users are identified

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password_hash,
        }